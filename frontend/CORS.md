Development proxy & CORS

- Development: Vite is configured to proxy `/api` requests to `http://127.0.0.1:8000` (see `vite.config.ts`). This makes calls like `fetch('/api/drug_discovery')` go to your local backend without CORS errors.

- Backend: `main.py` (FastAPI) now enables CORS only when `ENV` is not `production`. Allowed origins are restricted to common local dev hosts (e.g. `http://localhost:5173`). In production set `ENV=production` (or ensure it's not `development`) to avoid broad CORS.

- Production: `vercel.json` already contains a rewrite from `/api/:path*` to your backend host. When deployed on Vercel, the frontend uses same-origin `/api/...` (Vercel proxies server-side), so CORS is not required in production.
