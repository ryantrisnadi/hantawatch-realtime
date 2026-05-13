# HantaWatch Real-Time MVP 🐭🦠

HantaWatch is an educational public-health surveillance dashboard for hantavirus reports. Version 2 upgrades the original CSV-only prototype into a real-time MVP with scheduled public feed ingestion.

> Important: This is not an official medical, clinical, emergency, or government surveillance system.

## What changed in the real-time version?

The original MVP used only `backend/data/reports.csv`.

This version adds:

- FastAPI live-ingestion endpoints
- SQLite storage for live feed matches
- RSS/public page monitoring
- Scheduled refresh every 6 hours using APScheduler
- Manual refresh endpoint and frontend button
- Live ingestion status card
- Live public feed matches section

## Architecture

```txt
Official/public RSS feeds + official pages
        ↓
FastAPI ingestion service
        ↓
SQLite live_items table
        ↓
FastAPI JSON endpoints
        ↓
Next.js dashboard
```

The curated CSV still exists as a stable baseline dataset. The real-time part monitors feeds and official pages for new hantavirus-related items.

## Sources monitored by default

RSS feeds:

- WHO Disease Outbreak News RSS
- CDC Emerging Infectious Diseases current issue RSS
- CDC Emerging Infectious Diseases ahead-of-print RSS
- ECDC Latest News RSS

Official pages:

- CDC Andes Virus Situation Summary
- CDC Reported Hantavirus Cases

You can edit these in:

```txt
backend/app/ingest.py
```

## Run with Docker

```bash
docker compose up --build
```

Open:

```txt
Frontend: http://localhost:3000
Backend:  http://localhost:8000
API docs: http://localhost:8000/docs
```

## Run locally without Docker

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## API endpoints

### Baseline reports

```txt
GET /api/reports
GET /api/reports/summary
```

### Real-time ingestion

```txt
GET  /api/live/items
GET  /api/live/status
POST /api/live/refresh
```

Use `POST /api/live/refresh` to manually trigger ingestion during a demo.

## How “real-time” is it?

This is real-time in the practical dashboard sense: it refreshes from public online sources on a schedule and can be manually refreshed. It is not second-by-second streaming.

Default refresh interval:

```txt
Every 6 hours
```

Change it in `backend/app/main.py`:

```python
scheduler.add_job(refresh_live_data, "interval", hours=6, id="refresh_live_data", replace_existing=True)
```

## Suggested next upgrades

- PostgreSQL instead of SQLite
- Map view with Leaflet or Mapbox
- Admin upload page for CSV/Excel reports
- NLP extraction of cases, deaths, dates, and locations from articles
- Deduplication by canonical URL and title similarity
- Source confidence score
- Email/Slack alert when high-severity outbreak terms appear
- Airflow or GitHub Actions ETL pipeline

## Portfolio description

Built a real-time infectious disease surveillance dashboard using Next.js, FastAPI, SQLite, scheduled ETL, RSS ingestion, and Docker to monitor hantavirus-related public-health updates from official/public sources.
