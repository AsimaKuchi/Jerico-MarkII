"""Backend health scan tests for JobMatch AI.

Covers:
- Public jobs API (list, pagination, filters, sort, single get, 404)
- Auth guard (401 without token)
- Authenticated endpoints via seeded MongoDB session
- AI resume optimization (one-page constraint)
- AI cover letter (word limit)
- Job scraping ingestion endpoints
"""
import os
import re
import asyncio
import datetime as dt

import pytest
import requests
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv("/app/backend/.env")
load_dotenv("/app/frontend/.env")

BASE_URL = os.environ["REACT_APP_BACKEND_URL"].rstrip("/")
MONGO_URL = os.environ["MONGO_URL"]
DB_NAME = os.environ["DB_NAME"]

SESSION_TOKEN = "qa-session-token-123"
USER_ID = "qa-user-1"

SAMPLE_RESUME = """QA User
qa@example.com | 555-0100 | linkedin.com/in/qa

EXPERIENCE
Software Engineer, Acme Corp (Jan 2020 - Present)
- Built scalable Python microservices handling 1M+ daily requests
- Led React frontend migration reducing bundle size by 35%
- Mentored 4 junior engineers and drove code review standards

Software Engineer, Widgets Inc (Jun 2018 - Dec 2019)
- Developed REST APIs in FastAPI with PostgreSQL backing store
- Implemented CI/CD pipelines using GitHub Actions and Docker

EDUCATION
B.S. Computer Science, State University (2014 - 2018)

SKILLS
- Languages: Python, JavaScript, TypeScript, SQL
- Frameworks: React, FastAPI, Django, Node.js
- Tools: Docker, Kubernetes, AWS, MongoDB, PostgreSQL
"""


# ---------------------------- fixtures ----------------------------
@pytest.fixture(scope="session", autouse=True)
def seed_qa_session():
    """Seed a QA user + session + profile directly in Mongo, then cleanup."""
    async def _seed():
        client = AsyncIOMotorClient(MONGO_URL)
        db = client[DB_NAME]
        expires_at = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=1)).isoformat()
        await db.users.update_one(
            {"user_id": USER_ID},
            {"$set": {
                "user_id": USER_ID,
                "name": "QA User",
                "email": "qa@example.com",
                "picture": "",
            }},
            upsert=True,
        )
        await db.user_sessions.update_one(
            {"session_token": SESSION_TOKEN},
            {"$set": {
                "session_token": SESSION_TOKEN,
                "user_id": USER_ID,
                "expires_at": expires_at,
            }},
            upsert=True,
        )
        await db.user_profiles.update_one(
            {"user_id": USER_ID},
            {"$set": {
                "user_id": USER_ID,
                "resume_text": SAMPLE_RESUME,
                "resume_format": "text",
                "skills": ["Python", "React", "SQL"],
                "experience_years": 5,
                "job_titles": ["Software Engineer"],
            }},
            upsert=True,
        )
        client.close()

    async def _cleanup():
        client = AsyncIOMotorClient(MONGO_URL)
        db = client[DB_NAME]
        await db.users.delete_one({"user_id": USER_ID})
        await db.user_sessions.delete_one({"session_token": SESSION_TOKEN})
        await db.user_profiles.delete_one({"user_id": USER_ID})
        client.close()

    asyncio.get_event_loop().run_until_complete(_seed())
    yield
    asyncio.get_event_loop().run_until_complete(_cleanup())


@pytest.fixture
def client():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


@pytest.fixture
def auth_client():
    s = requests.Session()
    s.headers.update({
        "Content-Type": "application/json",
        "Authorization": f"Bearer {SESSION_TOKEN}",
    })
    return s


# ---------------------------- Health / Root ----------------------------
class TestHealth:
    def test_api_root(self, client):
        r = client.get(f"{BASE_URL}/api/")
        assert r.status_code == 200, r.text

    def test_api_health(self, client):
        r = client.get(f"{BASE_URL}/api/health")
        assert r.status_code == 200

    def test_public_health(self, client):
        r = client.get(f"{BASE_URL}/api/public/health")
        assert r.status_code == 200


# ---------------------------- Public Jobs API ----------------------------
class TestPublicJobs:
    def test_list_jobs_basic(self, client):
        r = client.get(f"{BASE_URL}/api/public/jobs?limit=5")
        assert r.status_code == 200, r.text
        data = r.json()
        assert "jobs" in data and isinstance(data["jobs"], list)
        assert "pagination" in data
        p = data["pagination"]
        for k in ["page", "limit", "total", "total_pages", "has_next", "has_prev"]:
            assert k in p
        assert p["limit"] == 5

    def test_list_jobs_pagination(self, client):
        r = client.get(f"{BASE_URL}/api/public/jobs?page=2&limit=3")
        assert r.status_code == 200
        assert r.json()["pagination"]["page"] == 2

    def test_list_jobs_filter_remote(self, client):
        r = client.get(f"{BASE_URL}/api/public/jobs?remote_only=true&limit=5")
        assert r.status_code == 200
        for j in r.json()["jobs"]:
            assert j["is_remote"] is True

    def test_list_jobs_filter_source(self, client):
        r = client.get(f"{BASE_URL}/api/public/jobs?source=greenhouse&limit=5")
        assert r.status_code == 200
        for j in r.json()["jobs"]:
            assert j["source"] == "greenhouse"

    def test_list_jobs_query_and_sort(self, client):
        r = client.get(f"{BASE_URL}/api/public/jobs?query=engineer&sort_by=company&sort_order=asc&limit=5")
        assert r.status_code == 200

    def test_get_job_by_id_success(self, client):
        list_r = client.get(f"{BASE_URL}/api/public/jobs?limit=1")
        assert list_r.status_code == 200
        jobs = list_r.json()["jobs"]
        if not jobs:
            pytest.skip("No jobs in DB to fetch by id")
        jid = jobs[0]["id"]
        r = client.get(f"{BASE_URL}/api/public/jobs/{jid}")
        assert r.status_code == 200, r.text
        d = r.json()
        assert d["id"] == jid

    def test_get_job_by_id_404(self, client):
        r = client.get(f"{BASE_URL}/api/public/jobs/definitely_not_a_real_job_id_xyz")
        assert r.status_code == 404

    def test_sources(self, client):
        r = client.get(f"{BASE_URL}/api/public/sources")
        assert r.status_code == 200
        assert "sources" in r.json()

    def test_companies(self, client):
        r = client.get(f"{BASE_URL}/api/public/companies")
        assert r.status_code == 200


# ---------------------------- Auth guard ----------------------------
class TestAuthGuard:
    def test_applications_unauth(self, client):
        r = client.get(f"{BASE_URL}/api/applications")
        assert r.status_code == 401

    def test_profile_unauth(self, client):
        r = client.get(f"{BASE_URL}/api/profile")
        assert r.status_code == 401

    def test_auth_me_unauth(self, client):
        r = client.get(f"{BASE_URL}/api/auth/me")
        assert r.status_code == 401


# ---------------------------- Authenticated flows ----------------------------
class TestAuthenticated:
    def test_auth_me(self, auth_client):
        r = auth_client.get(f"{BASE_URL}/api/auth/me")
        assert r.status_code == 200, r.text
        d = r.json()
        assert d.get("user_id") == USER_ID
        assert d.get("email") == "qa@example.com"

    def test_profile_get(self, auth_client):
        r = auth_client.get(f"{BASE_URL}/api/profile")
        assert r.status_code == 200, r.text
        d = r.json()
        assert d.get("user_id") == USER_ID
        assert "resume_text" in d

    def test_applications_list(self, auth_client):
        r = auth_client.get(f"{BASE_URL}/api/applications")
        assert r.status_code == 200, r.text
        d = r.json()
        # Endpoint returns a list or dict with applications
        assert isinstance(d, (list, dict))

    def test_dashboard_stats(self, auth_client):
        r = auth_client.get(f"{BASE_URL}/api/dashboard/stats")
        assert r.status_code == 200, r.text


# ---------------------------- AI: Resume Optimization ----------------------------
class TestResumeOptimization:
    def test_optimize_resume_one_page(self, auth_client):
        job_desc = (
            "Senior Python Engineer - Build scalable microservices using FastAPI, "
            "React, PostgreSQL, Docker and Kubernetes. Must have experience with "
            "AWS, CI/CD pipelines, and mentoring engineers."
        )
        r = auth_client.post(
            f"{BASE_URL}/api/ai/optimize-resume",
            json={"job_description": job_desc},
            timeout=180,
        )
        assert r.status_code == 200, r.text
        d = r.json()
        assert "optimized_resume" in d
        optimized = d["optimized_resume"]
        assert isinstance(optimized, str) and len(optimized) > 20

        orig = SAMPLE_RESUME
        orig_lines = [ln for ln in orig.splitlines() if ln.strip()]
        opt_lines = [ln for ln in optimized.splitlines() if ln.strip()]
        orig_words = len(orig.split())
        opt_words = len(optimized.split())
        orig_chars = len(orig)
        opt_chars = len(optimized)

        print(
            f"[resume] orig lines={len(orig_lines)} words={orig_words} chars={orig_chars} | "
            f"opt lines={len(opt_lines)} words={opt_words} chars={opt_chars}"
        )

        # P0 length constraint: optimized must NOT be longer than original
        assert len(opt_lines) <= len(orig_lines), (
            f"Optimized has more non-empty lines ({len(opt_lines)}) than original ({len(orig_lines)})"
        )
        assert opt_words <= orig_words, (
            f"Optimized has more words ({opt_words}) than original ({orig_words})"
        )
        assert opt_chars <= int(orig_chars * 1.05), (
            f"Optimized chars {opt_chars} exceeds original {orig_chars} by >5%"
        )

        # Preserves section headers
        for header in ["EXPERIENCE", "EDUCATION", "SKILLS"]:
            assert header in optimized, f"Missing section header: {header}"

        # Should still contain some bullet markers
        assert "-" in optimized or "•" in optimized

        # No stray code fences
        assert not optimized.strip().startswith("```")


# ---------------------------- AI: Cover Letter ----------------------------
class TestCoverLetter:
    def test_generate_cover_letter(self, auth_client):
        r = auth_client.post(
            f"{BASE_URL}/api/ai/cover-letter",
            json={
                "job_title": "Senior Python Engineer",
                "company": "Acme AI",
                "job_description": "Build scalable Python microservices using FastAPI, React and PostgreSQL.",
            },
            timeout=180,
        )
        assert r.status_code == 200, r.text
        d = r.json()
        assert "cover_letter" in d
        cl = d["cover_letter"]
        assert isinstance(cl, str) and len(cl) > 100
        words = len(cl.split())
        print(f"[cover_letter] words={words}")
        assert words <= 500, f"Cover letter too long: {words} words"


# ---------------------------- Job scraping ingestion ----------------------------
class TestIngestion:
    def test_ingest_background_non_500(self, client):
        r = client.post(f"{BASE_URL}/api/public/jobs/ingest?background=true")
        assert r.status_code == 200, r.text
        assert r.json().get("status") in ("started", "complete")

    def test_greenhouse_companies_list(self, auth_client):
        r = auth_client.get(f"{BASE_URL}/api/jobs/greenhouse/companies")
        assert r.status_code == 200

    def test_jobs_search_non_500(self, auth_client):
        r = auth_client.post(
            f"{BASE_URL}/api/jobs/search",
            json={"query": "engineer", "location": "remote"},
            timeout=60,
        )
        # Should not be 500; may return empty jobs if no RAPIDAPI_KEY / errors
        assert r.status_code != 500, r.text
