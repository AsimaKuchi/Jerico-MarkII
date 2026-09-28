# Test Credentials

## Authentication
The app uses **Emergent-managed Google OAuth**. Automated Google login cannot be completed by test tools.

### Seeded test session (for automated UI/API testing)
Auth is validated via a `session_token` (cookie `session_token` OR `Authorization: Bearer <token>`) checked against Mongo collection `user_sessions`.

To test authenticated flows, seed directly in MongoDB (use `MONGO_URL` + `DB_NAME` from `/app/backend/.env`):

- **users**: `{ user_id: "ui-preview-user", name: "Alex Rivera", email: "alex@example.com", picture: "" }`
- **user_sessions**: `{ session_token: "ui-preview-token-777", user_id: "ui-preview-user", expires_at: <ISO ~1 day ahead> }`
- **user_profiles**: `{ user_id: "ui-preview-user", resume_text: "EXPERIENCE...", resume_format: "text", skills: [...], experience_years: 6, job_titles: ["Software Engineer"], preferred_locations: ["Toronto"] }`

**Currently seeded and active:** `session_token = ui-preview-token-777` (user_id `ui-preview-user`).

For UI: set a browser cookie `session_token=ui-preview-token-777` for the preview domain, then visit protected routes (`/dashboard`, `/jobs`, `/applications`, `/interview-prep`, `/profile`). For API: add header `Authorization: Bearer ui-preview-token-777`.

Clean up these 3 docs when finished if desired.
