"""Backend tests for CareerPaths endpoints (new)."""
import os
import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "").rstrip("/")
if not BASE_URL:
    # fallback to reading frontend/.env directly
    with open("/app/frontend/.env") as f:
        for line in f:
            if line.startswith("REACT_APP_BACKEND_URL="):
                BASE_URL = line.split("=", 1)[1].strip().rstrip("/")

TOKEN = "ui-preview-token-777"
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}


# --- Auth guard checks (no token -> 401) ---
@pytest.mark.parametrize("method,path", [
    ("GET", "/api/ai/career-paths/cached"),
    ("GET", "/api/paths/guidance?path_title=Data%20Analyst"),
    ("PUT", "/api/paths/guidance/skills"),
    ("POST", "/api/paths/guidance/plan"),
    ("POST", "/api/paths/guidance/ask"),
    ("GET", "/api/ai/learning-resources?skills=Tableau"),
])
def test_protected_requires_auth(method, path):
    body = {"path_title": "Data Analyst", "skill": "Tableau", "checked": True,
            "question": "hi"}
    r = requests.request(method, f"{BASE_URL}{path}", json=body, timeout=15)
    assert r.status_code in (401, 403), f"{method} {path} -> {r.status_code} {r.text[:120]}"


# --- GET cached career paths ---
def test_get_cached_career_paths():
    r = requests.get(f"{BASE_URL}/api/ai/career-paths/cached", headers=HEADERS, timeout=30)
    assert r.status_code == 200, r.text[:200]
    data = r.json()
    assert "recommended_paths" in data
    assert isinstance(data["recommended_paths"], list)
    assert len(data["recommended_paths"]) >= 1
    # ensure no ObjectId leak
    assert "_id" not in str(data)


# --- Guidance GET ---
def test_get_guidance():
    r = requests.get(f"{BASE_URL}/api/paths/guidance?path_title=Data%20Analyst",
                     headers=HEADERS, timeout=15)
    assert r.status_code == 200, r.text[:200]
    data = r.json()
    for k in ("skills_checked", "plan_30d", "qna"):
        assert k in data, f"missing {k}"


# --- Guidance skill toggle PUT ---
def test_put_guidance_skills_toggle():
    payload = {"path_title": "Data Analyst", "skill": "Tableau", "checked": True}
    r = requests.put(f"{BASE_URL}/api/paths/guidance/skills",
                     json=payload, headers=HEADERS, timeout=15)
    assert r.status_code == 200, r.text[:200]
    data = r.json()
    assert "skills_checked" in data
    assert "Tableau" in data["skills_checked"]

    # untoggle
    payload["checked"] = False
    r2 = requests.put(f"{BASE_URL}/api/paths/guidance/skills",
                      json=payload, headers=HEADERS, timeout=15)
    assert r2.status_code == 200
    assert "Tableau" not in r2.json().get("skills_checked", [])


# --- Learning resources ---
def test_learning_resources():
    r = requests.get(f"{BASE_URL}/api/ai/learning-resources?skills=Tableau,Python",
                     headers=HEADERS, timeout=30)
    assert r.status_code == 200, r.text[:200]
    data = r.json()
    assert "resources" in data or "summary" in data
    # resources should be a dict/list with entries for tableau or python
    body = str(data).lower()
    assert "tableau" in body or "python" in body


# --- Jobs for path (graceful, no 500) ---
def test_jobs_for_path_graceful():
    r = requests.get(f"{BASE_URL}/api/ai/career-paths/Data%20Analyst/jobs",
                     headers=HEADERS, timeout=45)
    assert r.status_code in (200, 404), f"unexpected {r.status_code}: {r.text[:200]}"
    if r.status_code == 200:
        data = r.json()
        assert isinstance(data, (list, dict))
