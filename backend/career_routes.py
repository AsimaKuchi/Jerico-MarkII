"""
career_routes.py - Career Paths feature (ported from CareerCopilot).

Endpoints (mounted under /api):
  GET    /ai/career-paths/cached              -- Return cached analysis (404 if none)
  POST   /ai/career-paths                     -- Analyze resume -> 3-5 career paths (cached 7 days)
  DELETE /ai/career-paths                     -- Clear cached analysis
  GET    /ai/learning-resources?skills=a,b    -- Curated learning resources for skill gaps
  GET    /ai/career-paths/{path_title}/jobs   -- Real job listings scored against the profile
  GET    /paths/guidance?path_title=          -- Saved guidance state for a path
  PUT    /paths/guidance/skills               -- Toggle a skill on the progress checklist
  POST   /paths/guidance/plan[?force=true]    -- Generate / return cached 30-day plan
  POST   /paths/guidance/ask                  -- Single-turn "ask the coach" for a path

Dependencies are injected via build_router() to avoid a circular import with server.py.
"""
from datetime import datetime, timezone
from typing import Any, Dict, Optional
import json
import re
import uuid

import httpx
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from learning_resources import LEARNING_RESOURCES


COACH_SYSTEM_PROMPT = """You are a Direct & Honest career mentor. Your job is to help the user
get unstuck about their career without coddling them.

CRITICAL RULES:
1. NO FLUFF. No "great question!" Get to substance immediately.
2. TREAT THE USER AS A COMPETENT ADULT. Don't soften bad news.
3. CALL OUT VAGUE THINKING. Vague answers get one sharp follow-up question, not validation.
4. EVERY MESSAGE ENDS WITH A QUESTION OR A CONCRETE CHALLENGE.
5. KEEP MESSAGES SHORT. 80-150 words MAX.
6. ECONOMIC REALITY MATTERS. Talk about salary, market demand and risk honestly.
Stay in character. No emojis. Plain conversational prose."""


class SkillToggleRequest(BaseModel):
    path_title: str
    skill: str
    checked: bool


class PlanRequest(BaseModel):
    path_title: str
    path_data: Optional[Dict[str, Any]] = None


class AskRequest(BaseModel):
    path_title: str
    question: str
    path_data: Optional[Dict[str, Any]] = None


def _skill_names(skills) -> list:
    """Skills may be plain strings or {name: ...} objects."""
    out = []
    for s in skills or []:
        if isinstance(s, dict):
            name = s.get("name") or s.get("skill")
            if name:
                out.append(str(name))
        elif s:
            out.append(str(s))
    return out


def _strip_json_fences(raw: str) -> str:
    clean = raw.strip()
    clean = re.sub(r"^```(?:json)?\s*", "", clean)
    clean = re.sub(r"\s*```$", "", clean)
    return clean.strip()


def _serialize_guidance(doc: dict) -> dict:
    if not doc:
        return {"skills_checked": [], "plan_30d": None, "qna": []}
    return {
        "skills_checked": doc.get("skills_checked", []),
        "plan_30d": doc.get("plan_30d"),
        "qna": doc.get("qna", []),
    }


def build_router(db, logger, EMERGENT_LLM_KEY, RAPIDAPI_KEY, get_current_user, evaluate_job_match) -> APIRouter:
    router = APIRouter()

    def _llm(session_id: str, system: str):
        from emergentintegrations.llm.chat import LlmChat
        return LlmChat(api_key=EMERGENT_LLM_KEY, session_id=session_id, system_message=system).with_model("openai", "gpt-5.2")

    # ------------------------------------------------------------------
    # Career path analysis
    # ------------------------------------------------------------------
    @router.get("/ai/career-paths/cached")
    async def get_cached_career_paths(request: Request):
        user = await get_current_user(request)
        cached = await db.career_analyses.find_one({"user_id": user.user_id}, {"_id": 0})
        if not cached or not cached.get("analysis"):
            raise HTTPException(status_code=404, detail="No cached analysis")
        return cached["analysis"]

    @router.post("/ai/career-paths")
    async def analyze_career_paths(request: Request):
        user = await get_current_user(request)
        profile = await db.user_profiles.find_one({"user_id": user.user_id}, {"_id": 0})
        if not profile:
            raise HTTPException(status_code=400, detail="Please complete your profile first")

        cached = await db.career_analyses.find_one({"user_id": user.user_id}, {"_id": 0})
        if cached:
            try:
                cached_date = datetime.fromisoformat(cached.get("created_at", ""))
                if (datetime.now(timezone.utc) - cached_date).days < 7:
                    return cached.get("analysis")
            except Exception:
                pass

        resume_text = profile.get("resume_text", "") or ""
        if len(resume_text) < 100:
            raise HTTPException(status_code=400, detail="Please upload your resume for career path analysis")

        skills = _skill_names(profile.get("skills", []))
        experience_years = profile.get("experience_years", 0)
        current_titles = profile.get("job_titles", [])
        education = profile.get("highest_education", "")
        seniority = profile.get("seniority_level", "")
        industries = profile.get("industries", [])
        location = (
            profile.get("address_city")
            or profile.get("address_state")
            or profile.get("address_country")
            or (profile.get("preferred_locations") or [""])[0]
            or ""
        )

        system = """You are an expert career advisor with deep knowledge of career transitions, salary data, and skill requirements.

Analyze a person's resume and suggest realistic career paths.

RULES:
1. Only suggest paths where they have 60%+ of required skills
2. Include 3-5 paths: current path advancement, adjacent moves, and 1-2 stretch roles
3. Base salary estimates on real market data (conservative, not optimistic)
4. Provide specific, actionable skill gaps

OUTPUT FORMAT (JSON only, no markdown):
{
  "current_path": {"title": "Business Analyst", "salary_avg": 75000, "market_demand": "high", "job_security": "stable", "growth_potential": "moderate"},
  "recommended_paths": [
    {
      "title": "Data Analyst",
      "match_score": 85,
      "category": "adjacent",
      "skills_you_have": ["SQL", "Excel", "Python"],
      "skills_to_learn": ["Tableau", "R", "Statistical Analysis"],
      "salary_range": {"min": 70000, "max": 95000, "avg": 85000},
      "salary_increase": "+$10k",
      "time_to_transition": "3-6 months",
      "market_demand": "high",
      "job_count_estimate": 1200,
      "difficulty": "moderate",
      "reasoning": "Your SQL and Python skills transfer directly.",
      "next_steps": ["Learn Tableau (free course, 20 hours)", "Build 2-3 portfolio projects", "Apply to junior Data Analyst roles"]
    }
  ]
}

CATEGORIES: "current" (advance in role), "adjacent" (easy transition), "stretch" (requires more effort)
MARKET DEMAND: "very_high", "high", "medium", "low"
TIME TO TRANSITION: "1-3 months", "3-6 months", "6-12 months", "1-2 years"
DIFFICULTY: "easy" (80%+ match), "moderate" (60-80%), "hard" (<60%)"""

        prompt = f"""Analyze this person's career and suggest realistic next career paths.

PROFILE:
- Years of Experience: {experience_years}
- Current/Target Titles: {', '.join(current_titles) if current_titles else 'Not specified'}
- Skills: {', '.join(skills[:30]) if skills else 'Not specified'}
- Education: {education or 'Not specified'}
- Seniority: {seniority or 'Not specified'}
- Industries: {', '.join(industries) if industries else 'Any'}
- Location: {location or 'Canada'}

RESUME (trimmed):
{resume_text[:4000]}

Suggest 3-5 realistic career paths with salary ranges for {location or 'Canadian market'}.
Return ONLY valid JSON, no markdown."""

        from emergentintegrations.llm.chat import UserMessage
        try:
            raw = await _llm(f"career_paths_{user.user_id}_{uuid.uuid4().hex[:8]}", system).send_message(UserMessage(text=prompt))
            result = json.loads(_strip_json_fences(raw))
            if "recommended_paths" not in result:
                raise ValueError("Missing recommended_paths")
        except ValueError as e:
            logger.error(f"Career paths parse error: {e}")
            raise HTTPException(status_code=500, detail="Failed to parse career analysis. Please try again.")
        except Exception as e:
            logger.error(f"Career path analysis error: {e}")
            raise HTTPException(status_code=500, detail="Analysis failed. Please try again.")

        now_iso = datetime.now(timezone.utc).isoformat()
        result["generated_at"] = now_iso
        result["user_location"] = location
        result["experience_years"] = experience_years
        await db.career_analyses.update_one(
            {"user_id": user.user_id},
            {"$set": {"user_id": user.user_id, "analysis": result, "created_at": now_iso}},
            upsert=True,
        )
        return result

    @router.delete("/ai/career-paths")
    async def clear_career_analysis(request: Request):
        user = await get_current_user(request)
        await db.career_analyses.delete_many({"user_id": user.user_id})
        return {"message": "Career analysis cache cleared"}

    # ------------------------------------------------------------------
    # Learning resources
    # ------------------------------------------------------------------
    @router.get("/ai/learning-resources")
    async def get_learning_resources(request: Request, skills: Optional[str] = None):
        await get_current_user(request)
        if not skills:
            return {
                "available_skills": sorted(LEARNING_RESOURCES.keys()),
                "total_resources": sum(len(r) for r in LEARNING_RESOURCES.values()),
            }
        skill_list = [s.strip() for s in skills.split(",") if s.strip()]
        resources_by_skill: Dict[str, list] = {}
        for skill in skill_list:
            if skill in LEARNING_RESOURCES:
                resources_by_skill[skill] = LEARNING_RESOURCES[skill]
                continue
            for res_skill, res_list in LEARNING_RESOURCES.items():
                if skill.lower() in res_skill.lower() or res_skill.lower() in skill.lower():
                    resources_by_skill[skill] = res_list
                    break

        total_hours = total_free = total_paid = 0
        for resources in resources_by_skill.values():
            for r in resources:
                total_hours += r.get("duration_hours", 0)
                if "free" in r.get("cost", "").lower():
                    total_free += 1
                else:
                    total_paid += 1
        return {
            "skills_requested": skill_list,
            "resources": resources_by_skill,
            "summary": {
                "total_skills": len(resources_by_skill),
                "total_resources": total_free + total_paid,
                "total_hours": total_hours,
                "free_resources": total_free,
                "paid_resources": total_paid,
                "estimated_completion": f"{total_hours // 40} weeks at 40 hrs/week" if total_hours >= 40 else f"{total_hours} hours",
            },
        }

    # ------------------------------------------------------------------
    # Jobs for a career path
    # ------------------------------------------------------------------
    @router.get("/ai/career-paths/{path_title}/jobs")
    async def get_jobs_for_career_path(request: Request, path_title: str, location: Optional[str] = None, min_match_score: int = 60):
        user = await get_current_user(request)
        profile = await db.user_profiles.find_one({"user_id": user.user_id}, {"_id": 0})
        if not profile:
            raise HTTPException(status_code=400, detail="Profile required")
        if not location:
            location = profile.get("address_city") or profile.get("address_state") or (profile.get("preferred_locations") or ["Canada"])[0]

        try:
            title_words = [w for w in path_title.split() if len(w) >= 3]
            title_regex = "|".join(re.escape(w) for w in title_words) if title_words else re.escape(path_title)
            query_filter: Dict[str, Any] = {"title": {"$regex": title_regex, "$options": "i"}}
            if location:
                query_filter["$or"] = [
                    {"location": {"$regex": re.escape(location.split(",")[0].strip()), "$options": "i"}},
                    {"is_remote": True},
                ]
            cached_jobs = await db.stored_jobs.find(query_filter, {"_id": 0}).sort("posted_at", -1).limit(60).to_list(60)

            jsearch_jobs = []
            if RAPIDAPI_KEY:
                try:
                    async with httpx.AsyncClient(timeout=15.0) as client:
                        resp = await client.get(
                            "https://jsearch.p.rapidapi.com/search",
                            params={"query": f"{path_title} {location}", "num_pages": "2"},
                            headers={"X-RapidAPI-Key": RAPIDAPI_KEY, "X-RapidAPI-Host": "jsearch.p.rapidapi.com"},
                        )
                        if resp.status_code == 200:
                            jsearch_jobs = resp.json().get("data", [])[:30]
                except Exception:
                    logger.warning("JSearch API unavailable for career-path job search")

            normalised = []
            for j in jsearch_jobs:
                normalised.append({
                    "job_id": j.get("job_id"),
                    "title": j.get("job_title"),
                    "company": j.get("employer_name"),
                    "location": f"{j.get('job_city') or ''}, {j.get('job_state') or ''}".strip(", "),
                    "description": (j.get("job_description") or "")[:500],
                    "apply_link": j.get("job_apply_link"),
                    "posted_at": j.get("job_posted_at_datetime_utc"),
                    "source": "aggregator",
                })

            seen, unique_jobs = set(), []
            for job in cached_jobs + normalised:
                jid = job.get("job_id") or (job.get("title", "") + job.get("company", ""))
                if jid not in seen:
                    seen.add(jid)
                    unique_jobs.append(job)

            matched = []
            for job in unique_jobs[:60]:
                loc = job.get("location") or ""
                job_for_match = {
                    "job_title": job.get("title"),
                    "employer_name": job.get("company"),
                    "job_description": job.get("description") or job.get("title", ""),
                    "job_city": loc.split(",")[0].strip(),
                    "job_state": loc.split(",")[-1].strip() if "," in loc else "",
                    "job_is_remote": "remote" in loc.lower(),
                }
                ev = evaluate_job_match(job_for_match, profile)
                if ev["score"] >= min_match_score:
                    matched.append({
                        "job": {
                            "job_id": job.get("job_id"),
                            "title": job.get("title"),
                            "company": job.get("company"),
                            "location": job.get("location"),
                            "apply_link": job.get("apply_link") or job.get("url"),
                            "posted_at": job.get("posted_at"),
                            "source": job.get("source", "ats_board"),
                        },
                        "match_score": ev["score"],
                        "match_recommendation": ev["recommendation"],
                        "strengths": ev["strengths"],
                        "gaps": ev["gaps"],
                        "grounded_strengths": ev.get("grounded_strengths", []),
                        "matched_skills": ev.get("matched_skills", []),
                        "ready_to_apply": ev["score"] >= 75,
                    })

            matched.sort(key=lambda x: x["match_score"], reverse=True)
            top = matched[:30]
            return {
                "career_path": path_title,
                "location": location,
                "total_jobs_found": len(unique_jobs),
                "qualified_jobs": len(matched),
                "jobs": top,
                "summary": {
                    "ready_to_apply_now": sum(1 for j in top if j["match_score"] >= 75),
                    "close_match": sum(1 for j in top if 65 <= j["match_score"] < 75),
                    "stretch_roles": sum(1 for j in top if j["match_score"] < 65),
                    "avg_match_score": round(sum(j["match_score"] for j in top) / len(top), 1) if top else 0,
                },
            }
        except Exception as e:
            logger.error(f"Career-path job search error: {e}")
            raise HTTPException(status_code=500, detail="Job search failed")

    # ------------------------------------------------------------------
    # Path guidance: skill checklist, 30-day plan, ask the coach
    # ------------------------------------------------------------------
    async def _path_data_from_analysis(user_id: str, path_title: str) -> dict:
        doc = await db.career_analyses.find_one({"user_id": user_id}, {"_id": 0, "analysis": 1}) or {}
        for p in (doc.get("analysis") or {}).get("recommended_paths", []) or []:
            if p.get("title") == path_title:
                return p
        return {}

    @router.get("/paths/guidance")
    async def get_path_guidance(request: Request, path_title: str):
        user = await get_current_user(request)
        doc = await db.path_guidance.find_one({"user_id": user.user_id, "path_title": path_title}, {"_id": 0})
        return _serialize_guidance(doc)

    @router.put("/paths/guidance/skills")
    async def toggle_path_skill(request: Request, body: SkillToggleRequest):
        user = await get_current_user(request)
        now_iso = datetime.now(timezone.utc).isoformat()
        key = {"user_id": user.user_id, "path_title": body.path_title}
        if body.checked:
            await db.path_guidance.update_one(
                key,
                {"$addToSet": {"skills_checked": body.skill}, "$set": {"updated_at": now_iso},
                 "$setOnInsert": {"user_id": user.user_id, "path_title": body.path_title, "created_at": now_iso}},
                upsert=True,
            )
        else:
            await db.path_guidance.update_one(key, {"$pull": {"skills_checked": body.skill}, "$set": {"updated_at": now_iso}})
        doc = await db.path_guidance.find_one(key, {"_id": 0, "skills_checked": 1}) or {}
        return {"skills_checked": doc.get("skills_checked", [])}

    @router.post("/paths/guidance/plan")
    async def generate_30d_plan(request: Request, body: PlanRequest):
        user = await get_current_user(request)
        force = request.query_params.get("force", "").lower() in ("1", "true", "yes")
        key = {"user_id": user.user_id, "path_title": body.path_title}

        existing = await db.path_guidance.find_one(key, {"_id": 0, "plan_30d": 1})
        if not force and existing and existing.get("plan_30d"):
            return existing["plan_30d"]

        path_data = body.path_data or await _path_data_from_analysis(user.user_id, body.path_title)
        if not path_data:
            raise HTTPException(status_code=400, detail="No path context available; regenerate career analysis first.")

        profile = await db.user_profiles.find_one({"user_id": user.user_id}, {"_id": 0}) or {}
        location = profile.get("address_city") or profile.get("address_country") or "their region"
        system = ("You are a direct, no-fluff career mentor producing a 30-day execution plan. "
                  "Be specific, time-bound and realistic for a working professional with ~6-10 hrs/week to invest. "
                  "Output VALID JSON ONLY - no markdown fences, no commentary.")
        prompt = f"""Build a 30-day game plan to position the user for: {body.path_title}

Path details:
- Current strengths: {', '.join(path_data.get('skills_you_have', []) or []) or 'not specified'}
- Skills to learn: {', '.join(path_data.get('skills_to_learn', []) or []) or 'not specified'}
- Difficulty: {path_data.get('difficulty', 'moderate')}
- Time-to-transition estimate: {path_data.get('time_to_transition', 'unknown')}
- User location (for networking realism): {location}

Return JSON with this exact shape:
{{
  "headline": "1 sentence north star for the 30 days",
  "weeks": [
    {{"week": 1, "focus": "short label", "tasks": ["concrete task with hours or deliverable", "another"]}},
    {{"week": 2, "focus": "...", "tasks": ["..."]}},
    {{"week": 3, "focus": "...", "tasks": ["..."]}},
    {{"week": 4, "focus": "...", "tasks": ["..."]}}
  ],
  "success_signal": "1 sentence: what proves the plan worked at end of 30 days"
}}

Rules:
- Each week has 3-5 tasks. Each task is one line and actionable.
- Include at least 1 learning task, 1 portfolio/practice task, and 1 networking/visibility task across the plan.
- Reference real platforms by name (Coursera, GitHub, LinkedIn, etc.) when helpful.
- Don't recommend quitting a job."""

        from emergentintegrations.llm.chat import UserMessage
        try:
            raw = await _llm(f"plan_{user.user_id}_{uuid.uuid4().hex[:8]}", system).send_message(UserMessage(text=prompt))
            plan = json.loads(_strip_json_fences(raw))
        except json.JSONDecodeError:
            logger.error("30d plan JSON parse failed")
            raise HTTPException(status_code=500, detail="Plan returned in unexpected format, try again")
        except Exception as e:
            logger.error(f"30d plan gen error: {e}")
            raise HTTPException(status_code=500, detail="Plan generation failed")

        now_iso = datetime.now(timezone.utc).isoformat()
        plan["generated_at"] = now_iso
        plan["path_title"] = body.path_title
        await db.path_guidance.update_one(
            key,
            {"$set": {"plan_30d": plan, "updated_at": now_iso},
             "$setOnInsert": {"user_id": user.user_id, "path_title": body.path_title, "created_at": now_iso}},
            upsert=True,
        )
        return plan

    @router.post("/paths/guidance/ask")
    async def ask_path_coach(request: Request, body: AskRequest):
        user = await get_current_user(request)
        q = (body.question or "").strip()
        if not q:
            raise HTTPException(status_code=400, detail="Empty question")
        if len(q) > 1500:
            raise HTTPException(status_code=400, detail="Question too long (max 1500 chars)")

        key = {"user_id": user.user_id, "path_title": body.path_title}
        path_data = body.path_data or await _path_data_from_analysis(user.user_id, body.path_title)
        existing = await db.path_guidance.find_one(key, {"_id": 0, "qna": 1}) or {}
        prior = (existing.get("qna") or [])[-6:]
        prior_text = ("\n\nPRIOR Q&A FOR THIS PATH:\n" + "\n".join(f"Q: {p['question']}\nA: {p['answer']}" for p in prior)) if prior else ""

        system = (COACH_SYSTEM_PROMPT
                  + "\n\nYou are answering a SPECIFIC question about ONE career path the user is exploring. "
                  + "Stay tightly on this path. Keep answer to 80-150 words. End with a question or concrete challenge.")
        prompt = f"""User is exploring: {body.path_title}

Path details:
- Match: {path_data.get('match_score', '?')}%
- Skills they have: {', '.join(path_data.get('skills_you_have', []) or ['unknown'])}
- Skills to learn: {', '.join(path_data.get('skills_to_learn', []) or ['unknown'])}
- Difficulty: {path_data.get('difficulty', 'unknown')}
- Salary range: {path_data.get('salary_range', {})}
{prior_text}

USER ASKED:
{q}

Respond as the direct mentor. Reference path details when relevant."""

        from emergentintegrations.llm.chat import UserMessage
        try:
            answer = (await _llm(f"path_ask_{user.user_id}_{uuid.uuid4().hex[:8]}", system).send_message(UserMessage(text=prompt))).strip()
        except Exception as e:
            logger.error(f"Path-ask coach error: {e}")
            raise HTTPException(status_code=500, detail="Coach failed to respond, try again")

        now_iso = datetime.now(timezone.utc).isoformat()
        entry = {"question": q, "answer": answer, "created_at": now_iso}
        await db.path_guidance.update_one(
            key,
            {"$push": {"qna": entry}, "$set": {"updated_at": now_iso},
             "$setOnInsert": {"user_id": user.user_id, "path_title": body.path_title, "created_at": now_iso}},
            upsert=True,
        )
        return entry

    return router
