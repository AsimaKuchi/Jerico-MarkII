# Port Kit: bring this fork's improvements into MyCareerCopilot (the older, more evolved version)

Decision (user, Dec 2025): **Option A** — continue from the older "MyCareerCopilot" session
(GitHub: AsimaKuchi/CareerCopilot, deployed at mycareercopilot.ca) and port THIS fork's two
improvements onto it. Everything else in the old version stays as-is.

The two improvements to port:
1. **Editorial UI redesign** ("Editorial Sharp" design system + dark left sidebar)
2. **One-page resume optimizer** that NEVER makes the resume longer than the original

Everything needed lives in this fork. Source files are listed per improvement below.

---

## 0. How to hand this over (user steps)

1. In THIS session, click **"Save to GitHub"** so this fork's code is in a repo (e.g. `AsimaKuchi/<this-fork>`).
2. Open (or fork) the older **MyCareerCopilot** session.
3. Paste the prompt in section 3 to the agent there, replacing `<THIS_FORK_REPO_URL>`.
4. Keep the repo public until that agent confirms it has fetched the files, then set it private.

---

## 1. Improvement A — Editorial UI redesign

### Design system (drop-in, compatible: old repo already uses Shadcn HSL vars + `hsl(var(--x))` in tailwind)
Copy from this fork verbatim:
- `frontend/src/index.css`            — tokens (bone `48 20% 95%`, ink `223 54% 5%`, lime `70 100% 50%`), `--radius: 0px`,
                                        fonts (Cormorant Garamond / Manrope / Space Mono), grain overlay, `.micro-label`,
                                        `.editorial-card`, `.editorial-offset(-lime)`, legacy class remaps (`glass-*`, `text-gradient`, `card-hover`)
- `frontend/src/App.css`              — slimmed component styles
- `frontend/tailwind.config.js`       — MERGE only: `fontFamily {serif,sans,mono}` and `colors.sidebar {DEFAULT,border,foreground,muted}`
- `design_guidelines.json`            — full blueprint (colors, type scale, component rules, per-page layouts)

### Sidebar shell
- Replace `frontend/src/components/Navbar.jsx` with this fork's version (fixed dark left `<aside>` w-64 on desktop,
  `data-testid=navbar`; mobile top bar `data-testid=navbar-mobile` + `mobile-menu-toggle`).
  ADAPT for the old app: keep its nav items (Dashboard, Find Jobs, Applications, Interview Prep, Career Paths, Profile, Support, Home),
  keep the "MyCareer CoPilot" branding/plane logo in the sidebar header, keep UpgradeModal / Pro badge hooks if present.
- Every page that renders `<Navbar/>` needs the content offset. In the old repo that is:
  `Applications, Billing, CareerCoach, CareerPaths, Dashboard, InterviewPrep, JobSearch, Pricing, Profile` (+ admin layout if it uses Navbar).
  Apply: `sed -i 's/min-h-screen bg-background/min-h-screen bg-background md:pl-64/g'` (and `bg-gray-50`/`bg-white` root wrappers → `bg-background md:pl-64`).

### Marketing pages
- `frontend/src/pages/LandingPage.jsx` and `HowItWorks.jsx` — take this fork's editorial versions as the layout base
  (asymmetric serif hero, lime underline, bordered stat strip, bordered feature grid, dark "why we skip" block, sticky step index).
  ADAPT copy/brand to MyCareerCopilot, keep `handleGoogleLogin` AND the old app's email/password entry (`/auth`), keep Pricing/Support links,
  keep all existing `data-testid`s (`header-signin-btn`, `get-started-btn`, `learn-more-btn`, `cta-get-started-btn`, `feature-card-*`, `review-*`, `step-*`, `home-btn`).

### App pages colour sweep (what this fork did; run per page instead of rewriting)
```
for f in <pages and non-ui components>; do
  sed -i -E 's/bg-gradient-to-[a-z]{1,2}/bg-foreground/g' "$f"
  sed -i -E 's/(from|to|via)-(indigo|purple|violet)-[0-9]{2,3}(\/[0-9]+)?//g' "$f"
  sed -i -E 's/bg-(indigo|purple|violet)-(50|100)/bg-muted/g' "$f"
  sed -i -E 's/bg-(indigo|purple|violet)-(300|400|500|600|700)(\/[0-9]+)?/bg-foreground/g' "$f"
  sed -i -E 's/hover:bg-(indigo|purple|violet)-(300|400|500|600|700)/hover:bg-foreground/g' "$f"
  sed -i -E 's/text-(indigo|purple|violet)-(300|400|500|600|700)/text-foreground/g' "$f"
  sed -i -E 's/text-(indigo|purple|violet)-(100|200)/text-background/g' "$f"
  sed -i -E 's/border-(indigo|purple|violet)-(100|200|300|400|500|600)(\/[0-9]+)?/border-foreground/g' "$f"
  sed -i -E 's/ring-(indigo|purple|violet)-[0-9]+/ring-foreground/g' "$f"
  sed -i -E 's/rounded-(xl|2xl|3xl|lg|md)/rounded-none/g' "$f"
  sed -i -E 's/shadow-(sm|md|lg|xl|2xl)/shadow-none/g' "$f"
  sed -i -E 's/\bbg-white\b/bg-background/g; s/bg-gray-(50|100|200)\b/bg-muted/g'  "$f"
  sed -i -E 's/border-gray-(100|200|300)\b/border-border/g; s/border-gray-500\b/border-foreground/g' "$f"
  sed -i -E 's/text-gray-(400|500|600|700|900)\b/text-muted-foreground/g; s/hover:bg-gray-(50|100)\b/hover:bg-muted/g' "$f"
done
```
Gotchas learned here: use `\b` / exact ranges so `bg-gray-500` doesn't become `bg-muted0`; keep semantic status colours
(emerald/amber/red for applied/pending/rejected); primary CTAs → `bg-primary text-primary-foreground hover:bg-foreground hover:text-background font-mono text-xs uppercase tracking-widest`.
Old-app extras to restyle the same way: `Auth.jsx, Billing.jsx, Pricing.jsx, Support.jsx, CareerCoach.jsx, legal/*, admin/*`,
`UpgradeModal, ProfileCompletion, NextStepsCard, FeaturePreviews, SkillsCombobox, FormattedJobDescription, InterviewPrepRenderer`.
Old branding logo SVG uses indigo-500 — recolour to ink (`#060A14`) with lime (`#D4FF00`) stream.

---

## 2. Improvement B — One-page resume optimizer (never longer than original)

Target: `backend/routes/ai_routes.py` → `optimize_resume` (currently ~line 45-135).
KEEP the old version's Stripe gating (`check_usage_limit` / `increment_usage`) around it.
REPLACE the system prompt + prompt + call with this fork's logic from `backend/server.py` (`optimize_resume`, search "CRITICAL LENGTH RULES"):

Rules to encode (user decision: never shorter than original; just never longer):
- Output has EXACTLY the same number of non-empty lines as the original; never add a line/bullet.
- Each rewritten line ≤ original line length; total words ≤ original words.
- Replace words with JD keywords — never append. No preamble, no code fences.
- Prompt includes computed `{len(orig_lines)} non-empty lines, {orig_words} words`.

Post-processing guard (copy from this fork):
```
_strip_fences(text)   # remove ``` fences
_too_long(text) = lines > orig_lines or words > orig_words or chars > orig_chars*1.05
1st call → if _too_long → one "tighten" retry → if still _too_long → return original_resume (guaranteed fit)
```
Also hardened here: in `generate_cover_letter` use `(user_doc or {}).get('name') or user.name` instead of `user_doc['name']`.

Regression tests to bring over: `backend/tests/test_health_scan.py` (resume constraint assertions) and
`backend/tests/test_career_paths.py` (already relevant to the old app's career routes).

---

## 3. Ready-to-paste prompt for the agent in the MyCareerCopilot session

> Port two improvements from my other fork at `<THIS_FORK_REPO_URL>` into this project, following the recipe in that repo's
> `memory/PORT_TO_MYCAREERCOPILOT.md` exactly:
> (1) the "Editorial Sharp" UI redesign — drop in its `frontend/src/index.css`, `App.css`, tailwind `fontFamily`+`sidebar` colours and
> `design_guidelines.json`; replace the top navbar with its dark left sidebar `Navbar.jsx` (keep OUR nav items, MyCareer CoPilot branding,
> Support link and Pro/Upgrade hooks); offset every page that renders Navbar with `md:pl-64`; rebuild Landing + How It Works on its editorial
> layout with OUR copy/auth links; run the colour/rounding sweep on all remaining pages and components (incl. Auth, Billing, Pricing, Support,
> CareerCoach, legal, admin, UpgradeModal). Do NOT change any data-testid or any auth/Stripe/admin logic.
> (2) its one-page resume optimizer: in `routes/ai_routes.py` `optimize_resume`, keep our Stripe usage gating but replace the prompt and add
> the `_strip_fences` / `_too_long` retry + fallback-to-original guard so the optimized resume is NEVER longer than the original
> (do not let the AI cut content). Also null-safe the cover-letter name access.
> Then run the frontend + backend testing agent and confirm nothing regressed.

---

## 4. Files in THIS fork that carry the improvements (for reference)
- Redesign: `frontend/src/index.css`, `frontend/src/App.css`, `frontend/tailwind.config.js`, `frontend/src/components/Navbar.jsx`,
  `frontend/src/pages/LandingPage.jsx`, `frontend/src/pages/HowItWorks.jsx`, restyled `Dashboard/JobSearch/Applications/InterviewPrep/Profile/CareerPaths.jsx`,
  `components/AnalyzeMatchDialog.jsx`, `components/PathGuidance.jsx`, `design_guidelines.json`
- Resume fix: `backend/server.py` (`optimize_resume`, `generate_cover_letter`), tests in `backend/tests/test_health_scan.py`
- Career Paths port (already exists in the old app natively — no need to port back): `backend/career_routes.py`, `backend/learning_resources.py`
