# JobMatch AI - Product Requirements Document

## Original Problem Statement
Build a website that helps users find jobs best suited for them based on what info they provide and automatically applies to them based off their approval. Also optimizes resumes to ATS standard based off each job, using their resume. Make a cover letter for each job and interview tips and prep.

## Core Principles (Quality-First)
- **Quality over volume**: Focus on high-quality, relevant job matches
- **Human-in-the-loop**: Users must review and approve every application before it's sent
- **Transparency**: System explains why jobs are recommended or skipped
- **Intelligent evaluation**: Roles evaluated based on relevance, industry, seniority, location, work authorization, and skill overlap

## User Choices
- **AI Provider**: OpenAI GPT-5.2 (via Emergent Universal Key)
- **Job Data Source**: JSearch API (RapidAPI) + Greenhouse + Lever (real-time scraping)
- **Authentication**: Google Social Login (Emergent OAuth)
- **Design**: Light theme with glassmorphism

## Architecture

### Tech Stack
- **Frontend**: React 19 + Tailwind CSS + Shadcn UI
- **Backend**: FastAPI (Python)
- **Database**: MongoDB
- **AI**: OpenAI GPT-5.2 via emergentintegrations
- **Job API**: JSearch (RapidAPI) + Greenhouse/Lever APIs
- **Auth**: Emergent Google OAuth

### Key Files
```
/app/backend/server.py          # Main API endpoints
/app/frontend/src/App.js        # Main React app with routing
/app/frontend/src/pages/        # All page components
/app/frontend/src/components/   # Shared components (Navbar)
```

## What's Been Implemented (January 25, 2025)

### MVP Features ✅
- **Landing Page**: Hero section, features showcase, CTAs with light theme
- **Google Auth**: Full OAuth flow with session management
- **Dashboard**: 
  - Stats cards, quick actions, profile completion guide
  - **NEW (Jan 25)**: "Your Saved Jobs" section showing jobs from last search
  - **NEW (Jan 25)**: "NEW" star badge on jobs not seen before
  - **NEW (Jan 25)**: "Find New Jobs" button to trigger fresh search
- **Profile Page**: 
  - Resume upload (PDF, DOCX, TXT)
  - Skills management
  - Job preferences
  - Salary expectations
  - Work Authorization (citizen, permanent_resident, work_permit, require_sponsorship)
  - Target Industries (max 3, with "open to any" option)
  - Seniority Level (entry, junior, mid, senior, lead, manager, director, executive)
- **Job Search**: 
  - Real-time search via JSearch API
  - **NEW**: Detailed match evaluation with:
    - Match score (0-100%)
    - Match recommendation (strong_match, good_match, review, weak_match, skip)
    - Strengths list
    - Gaps list
    - Match reasoning explanation
    - Skip reason (for not recommended jobs)
  - Expandable match analysis on job cards
  - Grayed out "skip" recommended jobs with disabled apply button
- **Applications**: Create, approve, reject, delete with status tracking
- **AI Features**:
  - Resume ATS optimization (GPT-5.2)
  - Cover letter generation (GPT-5.2)
  - Interview prep materials (GPT-5.2)

### Backend API Endpoints
- `POST /api/auth/session` - Exchange session_id for session_token
- `GET /api/auth/me` - Get current user
- `POST /api/auth/logout` - Logout user
- `GET/PUT /api/profile` - Profile management (includes new fields)
- `POST /api/profile/resume` - Resume upload
- `POST /api/jobs/search` - Search jobs with detailed match evaluation
- `POST /api/ai/optimize-resume` - ATS optimization
- `POST /api/ai/cover-letter` - Generate cover letter
- `POST /api/ai/interview-prep` - Generate interview prep
- `GET/POST /api/applications` - Application CRUD
- `PUT /api/applications/{id}/approve` - Approve application
- `PUT /api/applications/{id}/reject` - Reject application
- `GET /api/dashboard/stats` - Dashboard statistics

## Match Evaluation Algorithm
The job matching evaluates candidates against jobs using:
1. **Role Relevance** (+25 points): Title alignment with target positions
2. **Skills Match** (+20 points): Ratio of matching skills in job description
3. **Experience Level** (+15 points): Seniority alignment (junior/mid/senior/director)
4. **Location Match** (+15 points): Preferred locations or remote availability
5. **Industry Match** (+10 points): Target industries or "open to any"
6. **Work Authorization Check**: Filters jobs requiring sponsorship if user needs it
7. **Salary Check** (+5 points): Salary range meets minimum requirement

## Prioritized Backlog

### P0 - Critical (Completed ✅)
- ✅ Quality-First job matching with detailed evaluation
- ✅ Work authorization filter
- ✅ Industry and seniority matching
- ✅ Fallback search mechanism for multi-word queries (fixed Jan 25, 2025)

### P1 - High Priority (Next)
- [ ] Add Google Jobs as a search source (user approved)
- [ ] Interview Tips & Prep feature completion
- [ ] Email notifications for new job matches

### P2 - Medium Priority
- [ ] Implement Playwright-based Ashby scraper (currently non-functional)
- [ ] Expand Auto-Submit to support Lever/Ashby boards
- [ ] Fetch full job descriptions for better AI analysis
- [ ] Saved job searches
- [ ] Multiple resume versions
- [ ] Application notes and reminders

### P3 - Nice to Have
- [ ] LinkedIn integration
- [ ] Company research panel
- [ ] Salary negotiation tips
- [ ] Video interview practice

## Test Results (Latest: iteration_4.json - January 25, 2025)
- **Backend**: 100% success rate (18/18 tests passed)
- **Frontend**: All UI flows verified
- **Performance**: Job loading reduced from 35-60s to ~2s (parallel fetching)
- **Fixed P0 Bug**: Fallback search endpoint corrected in JobSearch.jsx
- **New Features**: Dashboard saved jobs, NEW star indicators, parallel fetching

## Database Schema

### users
- user_id: string
- email: string
- name: string
- picture: string (optional)
- created_at: datetime

### user_profiles
- user_id: string
- resume_text: string (optional)
- resume_filename: string (optional)
- resume_format: string (optional)
- skills: array[string]
- experience_years: int
- job_titles: array[string]
- preferred_locations: array[string]
- salary_min: int (optional)
- salary_max: int (optional)
- job_type: array[string]
- work_authorization: string (optional) - citizen, permanent_resident, work_permit, require_sponsorship
- industries: array[string] - max 3
- open_to_any_industry: boolean
- seniority_level: string (optional) - entry, junior, mid, senior, lead, manager, director, executive
- updated_at: datetime

### applications
- application_id: string
- user_id: string
- job_id: string
- job_title: string
- company: string
- location: string (optional)
- job_description: string
- optimized_resume: string (optional)
- cover_letter: string (optional)
- status: string - pending, approved, applied, rejected
- match_score: int
- created_at: datetime
- applied_at: datetime (optional)


## Design System (as of Dec 2025)
- **Aesthetic**: "Editorial Sharp" — full redesign away from the original purple/indigo glassmorphism (which read as generic/AI-slop).
- **Tokens**: warm bone background `#F5F4F0`, deep ink navy `#060A14`, single electric lime accent `#D4FF00`; sharp corners (`--radius: 0`), hairline 1px borders (no heavy shadows), subtle grain overlay.
- **Type**: Cormorant Garamond (serif display headings), Manrope (sans body), Space Mono (uppercase micro-labels / metrics).
- **Shell**: logged-in pages use a fixed dark left sidebar (`components/Navbar.jsx`, `data-testid=navbar`) + mobile top bar; content offset `md:pl-64`.
- **Blueprint**: `/app/design_guidelines.json`.

## STRATEGIC DECISION (Dec 2025) — Option A: switch base to the older "MyCareerCopilot" version
- The user's older session (GitHub `AsimaKuchi/CareerCopilot`, deployed at mycareercopilot.ca) is far more evolved:
  email/password + Google auth, CSRF/rate limits/audit logs, Stripe Free/Pro + Pricing/Billing, full admin dashboard,
  Chrome autofill extension v1.3.0 + Playwright autofill-bot, Career Coach chat, job comparison, SmartRecruiters/Pinpoint
  scrapers, Support/legal pages, Resend email, refactored `routes/` backend, code-splitting.
- Decision: continue development FROM the older version and port THIS fork's two unique improvements onto it:
  (1) the Editorial UI redesign, (2) the never-longer-than-original one-page resume optimizer.
- Handoff recipe + ready-to-paste prompt: `/app/memory/PORT_TO_MYCAREERCOPILOT.md`.
- This fork is therefore a DONOR codebase; treat further feature work here as low priority unless the user changes direction.

## Changelog

### 2025-12 — Career Paths feature ported from CareerCopilot (DONE, verified)
- Source: user's older GitHub version `AsimaKuchi/CareerCopilot`. Only the **Career Paths** page was ported (the separate Career Coach page, Stripe billing, admin pages were intentionally NOT ported).
- Backend: new module `/app/backend/career_routes.py` (`build_router(...)`, dependency-injected to avoid circular imports; mounted under `/api` in `server.py`) + `/app/backend/learning_resources.py` (46 skills / 60 curated courses). Endpoints: `GET/POST/DELETE /api/ai/career-paths`, `GET /api/ai/career-paths/cached`, `GET /api/ai/learning-resources`, `GET /api/ai/career-paths/{title}/jobs`, `GET /api/paths/guidance`, `PUT /api/paths/guidance/skills`, `POST /api/paths/guidance/plan`, `POST /api/paths/guidance/ask`. Adapted: removed Stripe usage gating, encryption layer and rate limiter; uses gpt-5.2. Collections: `career_analyses`, `path_guidance`.
- Frontend: `pages/CareerPaths.jsx`, `components/PathGuidance.jsx` (skill checklist, 30-day plan, ask-the-coach), `utils/apiFetch.js`; route `/career-paths`; sidebar nav item "Career Paths" (Compass, `nav-career-paths`). Restyled to the editorial system; coach-page links removed; entry screen is single-choice.
- Verified: backend 11/11 (`tests/test_career_paths.py`), frontend flows 100% (iteration_9). Real LLM analysis generated 5 paths for the seeded profile.

### 2025-12 — Full editorial UI redesign (DONE, verified)
- Rewrote CSS foundation (`index.css`, `App.css`) + `tailwind.config.js` with the new tokens, fonts, grain overlay, and editorial utility classes; remapped legacy classes (glass/gradient) to safe flat equivalents.
- Converted the top navbar into a dark editorial left sidebar (`Navbar.jsx`), preserving all nav-* / user-menu / logout testids.
- Fully rewrote `LandingPage.jsx` and `HowItWorks.jsx` in an asymmetric magazine layout (serif hero, lime accents, bordered strips, sticky step index). Auth flow (`handleGoogleLogin`) unchanged.
- Restyled Dashboard, JobSearch, Applications, InterviewPrep, Profile: sidebar offset + swapped hardcoded indigo/purple/gradients to ink+lime + neutralized rounded/shadow/gray utilities.
- Verified by testing agent (iteration_8): 100% for scope — all pages render, sidebar + navigation + auth + data load work, no console errors, mobile works, all data-testids intact.

### 2025-12 — One-page resume optimization (P0, DONE)
- `POST /api/ai/optimize-resume` enforces one-page constraint (never longer than original) via strict prompt rules + `_too_long()` retry + deterministic fallback to original. Cover-letter name-access hardened. Verified 24/24 backend tests (iteration_7).

### Still pending / backlog
- P1: Google Jobs as an extra source (SerpApi vs reuse JSearch key — awaiting user decision)
- P1: Playwright auto-fill for Greenhouse / Lever / Ashby
- P1: Refactor monolithic `server.py` into routes/services/models (awaiting full vs incremental decision)
- P2: Playwright-based Ashby scraper (placeholder); silence the /jobs aggregator console error
- P3: Full job descriptions, more aggregators, status tracking, monetization
