from __future__ import annotations
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd
from .ingest import refresh_live_data, FEEDS, OFFICIAL_PAGES
from .storage import get_live_items, latest_refresh, connect

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "reports.csv"

app = FastAPI(title="HantaWatch Real-Time API", version="2.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scheduler = BackgroundScheduler()


def load_reports():
    df = pd.read_csv(DATA_PATH)
    df = df.fillna("")
    return df.to_dict(orient="records")

@app.on_event("startup")
def startup():
    connect().close()
    if not scheduler.running:
        scheduler.add_job(refresh_live_data, "interval", hours=6, id="refresh_live_data", replace_existing=True)
        scheduler.start()

@app.get("/")
def root():
    return {"name": "HantaWatch", "mode": "real-time MVP", "docs": "/docs"}

@app.get("/api/reports")
def reports():
    return load_reports()

@app.get("/api/reports/summary")
def summary():
    data = load_reports()
    total_cases = sum(int(r.get("confirmed_cases") or 0) for r in data)
    total_deaths = sum(int(r.get("deaths") or 0) for r in data if str(r.get("deaths", "")).strip() != "")
    cfr = round((total_deaths / total_cases) * 100, 2) if total_cases else 0
    latest_date = max([r["report_date"] for r in data]) if data else None
    return {
        "total_confirmed_cases": total_cases,
        "total_deaths": total_deaths,
        "case_fatality_rate_percent": cfr,
        "latest_report_date": latest_date,
        "static_reports": len(data),
        "live_items": len(get_live_items(500)),
    }

@app.get("/api/live/items")
def live_items(limit: int = 50):
    return get_live_items(limit)

@app.post("/api/live/refresh")
def refresh_now():
    return refresh_live_data()

@app.get("/api/live/status")
def live_status():
    return {
        "latest_refresh": latest_refresh(),
        "refresh_interval_hours": 6,
        "feeds": FEEDS,
        "official_pages": OFFICIAL_PAGES,
        "note": "This MVP monitors official/public RSS feeds and official pages for hantavirus-related updates. It is not a clinical alerting system.",
    }
