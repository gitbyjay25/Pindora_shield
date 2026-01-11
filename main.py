from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.drugs import router as text_router
from routes.checks import router as check_router
from routes.metrics import router as metrics_router

app = FastAPI(title="Pindora Shield API",description="Drug discovery and molecule generation API",version="1.0.0")

# Configure CORS only for development so production remains same-origin and secure.
# In production we expect the frontend to be served from the same origin (e.g. via Vercel rewrites to the API),
# so broad CORS is not enabled there.
import os
ENV = os.getenv("ENV", "development")
if ENV == "production":
    # No broad CORS in production (assume same-origin requests / server-side proxy)
    pass
else:
    # Allow local dev origins (Vite default port 5173 and a common fallback 3000)
    dev_origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=dev_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(text_router)
app.include_router(check_router)
app.include_router(metrics_router)