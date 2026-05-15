# HantaWatch Real-Time MVP 🐭🦠

HantaWatch is a real-time educational public-health surveillance dashboard for hantavirus-related reports and outbreak monitoring.

The platform combines a curated baseline dataset with scheduled ingestion from official/public feeds and pages to provide situational awareness through a modern full-stack dashboard.

> ⚠️ Educational use only. This project is not an official medical, clinical, governmental, or emergency alert system.

---

# 🌐 Live Deployment

## Frontend (Vercel)

https://hantawatch-realtime.vercel.app

## Backend API (Render)

https://hantawatch-realtime.onrender.com

## API Documentation

https://hantawatch-realtime.onrender.com/docs

## Health Check

https://hantawatch-realtime.onrender.com/healthz

---

# 🚀 Features

## Dashboard

- Real-time public-health dashboard
- Summary statistics cards
- Case fatality rate calculation
- Curated baseline outbreak table
- Live ingestion status section
- Manual live refresh button
- Responsive modern UI

## Backend

- FastAPI REST API
- Scheduled ingestion using APScheduler
- RSS/public feed monitoring
- SQLite persistence layer
- Health check endpoint
- Swagger/OpenAPI documentation

## Frontend

- Next.js + TypeScript
- Environment-based API configuration
- Deployed on Vercel
- Live backend integration
- Public deployment support

---

# 🧠 Real-Time Architecture

```txt
Official/Public RSS Feeds + Official Pages
                ↓
        FastAPI Ingestion Service
                ↓
        SQLite Live Items Store
                ↓
        FastAPI JSON Endpoints
                ↓
        Next.js Frontend Dashboard
                ↓
              User
```

The curated CSV dataset still exists as a stable baseline dataset while the ingestion service continuously monitors public sources for hantavirus-related updates.

---

# 📡 Sources Monitored

## RSS Feeds

- WHO Disease Outbreak News RSS
- CDC Emerging Infectious Diseases RSS
- CDC Ahead-of-Print RSS
- ECDC Latest News RSS

## Official Pages

- CDC Andes Virus Summary
- CDC Reported Hantavirus Cases

You can modify monitored sources in:

```txt
backend/app/ingest.py
```

---

# 🛠️ Tech Stack

## Frontend

- Next.js
- TypeScript
- CSS / Global Styling
- Vercel

## Backend

- FastAPI
- Python
- APScheduler
- SQLite
- Pandas
- Feedparser

## DevOps / Deployment

- Docker
- Docker Compose
- GitHub
- Render
- Vercel

---

# ⚙️ Environment Variables

Frontend uses:

```env
NEXT_PUBLIC_API_BASE_URL=https://hantawatch-realtime.onrender.com
```

---

# 🐳 Run with Docker

```bash
docker compose up --build
```

Open:

```txt
Frontend: http://localhost:3000
Backend:  http://localhost:8000
API docs: http://localhost:8000/docs
```

---

# 💻 Run Locally Without Docker

## Backend

```bash
cd backend

python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

## Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# 📚 API Endpoints

## Baseline Reports

```txt
GET /api/reports
GET /api/reports/summary
```

## Live Ingestion

```txt
GET  /api/live/items
GET  /api/live/status
POST /api/live/refresh
```

Use:

```txt
POST /api/live/refresh
```

to manually trigger ingestion during demos.

---

# ⏱️ Refresh Strategy

This project is “real-time” in the practical dashboard sense.

The ingestion service periodically refreshes monitored public sources and also supports manual refresh triggering.

Default refresh interval:

```txt
Every 6 hours
```

Modify in:

```txt
backend/app/main.py
```

```python
scheduler.add_job(
    refresh_live_data,
    "interval",
    hours=6,
    id="refresh_live_data",
    replace_existing=True
)
```

---

# 🔒 CORS + Deployment Notes

- Frontend and backend are deployed separately
- Backend allows Vercel frontend domains via CORS
- Render free-tier instances may spin down during inactivity
- First request after inactivity may take ~30–60 seconds

---

# 🧪 Suggested Future Improvements

- PostgreSQL instead of SQLite
- Interactive outbreak heatmap
- Leaflet or Mapbox integration
- NLP extraction from articles
- AI outbreak summarization
- Source confidence scoring
- Alerting system (email/Slack)
- Authentication/admin dashboard
- Kubernetes deployment
- CI/CD pipelines with GitHub Actions
- Unit/integration testing

---

# 📸 Demo

## Local Dashboard

Add screenshots here later.

Example:

```txt
/docs/screenshots/dashboard.png
```

---

# 📄 Portfolio Description

Built and deployed a real-time infectious disease surveillance dashboard using Next.js, FastAPI, SQLite, APScheduler, RSS ingestion, Docker, Render, and Vercel to monitor hantavirus-related public-health updates from official/public sources.

---

# 👨‍💻 Author

Ryan Trisnadi

LinkedIn:
https://www.linkedin.com/in/ryan-trisnadi-732046106/

GitHub:
https://github.com/ryantrisnadi