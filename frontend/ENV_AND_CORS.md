Environment variables and CORS

1) Environment variables (Vite)
- Vite exposes env variables to client code only when they are prefixed with `VITE_`.
- Use `import.meta.env.VITE_API_URL` in client-side TypeScript/JavaScript.
- For server-side or Node (serverless functions), use `process.env.VITE_API_URL`.

Files created in this repo:
- `.env.development` — VITE_API_URL=http://localhost:8000
- `.env.staging` — VITE_API_URL=https://staging.example.com
- `.env.production` — VITE_API_URL=https://biogen.ai

2) Updating fetch calls
- Example client fetch:
  - `fetch(`${import.meta.env.VITE_API_URL}/api/drug_discovery`, { method: 'POST', body: JSON.stringify({...}) })`
- Server-side (proxy) fallback used in this project:
  - `const API_BASE = process.env.VITE_API_URL || (import.meta.env && import.meta.env.VITE_API_URL) || 'http://127.0.0.1:8000'`

3) CORS guidance
- If you use a dev proxy or server-side rewrites (recommended), your frontend and backend appear same-origin to the browser and CORS is not necessary.
- If you cannot use a proxy, configure the backend to return these headers for cross-origin requests (OPTIONS preflight and actual response):
  - `Access-Control-Allow-Origin: *` (or a specific origin)
  - `Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS`
  - `Access-Control-Allow-Headers: Content-Type, Accept, Authorization`

4) Testing matrix
- Local dev: `uvicorn main:app --reload --port 8000` + `cd frontend && npm run dev`.
- Staging: Build and deploy with `VITE_API_URL` set to staging backend.
- Production: Build with `VITE_API_URL` set to production backend or use same-origin proxy.

5) Notes
- Do not hard-code full URLs in frontend code; use the env var so the same code works across environments.
- Keep existing try/catch and JSON parsing — this change does not modify any existing UX error handling.
