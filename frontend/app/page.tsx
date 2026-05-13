'use client';

import { useEffect, useState } from 'react';
import { Activity, RefreshCcw, Database, Newspaper } from 'lucide-react';
import { fetchJson, type Report, type Summary, type LiveItem } from '../lib/api';

export default function HomePage() {
  const [summary, setSummary] = useState<Summary | null>(null);
  const [reports, setReports] = useState<Report[]>([]);
  const [liveItems, setLiveItems] = useState<LiveItem[]>([]);
  const [status, setStatus] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function loadDashboard() {
    setError('');
    try {
      const [summaryData, reportData, feedData, statusData] = await Promise.all([
        fetchJson<Summary>('/api/reports/summary'),
        fetchJson<Report[]>('/api/reports'),
        fetchJson<LiveItem[]>('/api/live/items?limit=20'),
        fetchJson<any>('/api/live/status'),
      ]);
      setSummary(summaryData);
      setReports(reportData);
      setLiveItems(feedData);
      setStatus(statusData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to load dashboard');
    }
  }

  async function refreshLiveData() {
    setLoading(true);
    setError('');
    try {
      await fetchJson('/api/live/refresh', { method: 'POST' });
      await loadDashboard();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Refresh failed');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { loadDashboard(); }, []);

  return (
    <main className="container">
      <section className="hero">
        <div>
          <h1>HantaWatch 🐭🦠</h1>
          <p>
            A real-time MVP public-health surveillance dashboard. It combines a curated baseline dataset with scheduled ingestion from official/public feeds and pages.
          </p>
        </div>
        <div className="badge">Real-time MVP: refreshes every 6 hours</div>
      </section>

      {error && <div className="card" style={{ borderColor: '#f87171' }}>{error}</div>}

      <section className="grid">
        <div className="card"><h3>Total cases</h3><div className="stat">{summary?.total_confirmed_cases ?? '—'}</div></div>
        <div className="card"><h3>Total deaths</h3><div className="stat">{summary?.total_deaths ?? '—'}</div></div>
        <div className="card"><h3>Case fatality rate</h3><div className="stat">{summary ? `${summary.case_fatality_rate_percent}%` : '—'}</div></div>
        <div className="card"><h3>Live feed items</h3><div className="stat">{summary?.live_items ?? '—'}</div></div>
      </section>

      <section className="section card">
        <div className="toolbar">
          <div>
            <h2><Activity size={20}/> Live ingestion status</h2>
            <p className="muted">Latest refresh: {status?.latest_refresh?.refreshed_at ?? 'Not refreshed yet'}</p>
            <p className="muted">Sources monitored: {(status?.feeds?.length ?? 0) + (status?.official_pages?.length ?? 0)}</p>
          </div>
          <button className="button" onClick={refreshLiveData} disabled={loading}>
            <RefreshCcw size={16}/> {loading ? 'Refreshing...' : 'Refresh Live Data'}
          </button>
        </div>
      </section>

      <section className="section">
        <h2><Newspaper size={20}/> Live public feed matches</h2>
        {liveItems.length === 0 ? (
          <div className="card muted">No live matches yet. Click “Refresh Live Data” after starting the backend with internet access.</div>
        ) : (
          liveItems.map(item => (
            <a key={item.id} className="card feed-item section" href={item.source_url} target="_blank">
              <h3>{item.title}</h3>
              <p className="muted">{item.source_name} · {item.published_at ?? item.created_at}</p>
              <p>{item.summary}</p>
              <div>{item.matched_keywords.map(k => <span className="pill" key={k}>{k}</span>)}</div>
            </a>
          ))
        )}
      </section>

      <section className="section">
        <h2><Database size={20}/> Curated baseline reports</h2>
        <div className="table-wrap">
          <table>
            <thead><tr><th>Date</th><th>Country</th><th>Region</th><th>Cases</th><th>Deaths</th><th>Source</th><th>Notes</th></tr></thead>
            <tbody>
              {reports.map((r, i) => (
                <tr key={`${r.source_url}-${i}`}>
                  <td>{r.report_date}</td><td>{r.country}</td><td>{r.region}</td><td>{r.confirmed_cases}</td><td>{r.deaths || '—'}</td>
                  <td><a className="source-link" href={r.source_url} target="_blank">{r.source_name}</a></td><td>{r.notes}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <p className="footer">
        Educational use only. This app monitors public feeds and official pages for situational awareness; it is not a medical diagnosis, emergency alerting, or official surveillance system.
      </p>
    </main>
  );
}
