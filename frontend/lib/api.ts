export const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

export type Report = {
  report_date: string;
  country: string;
  region: string;
  confirmed_cases: number | string;
  deaths: number | string;
  virus_type: string;
  source_name: string;
  source_url: string;
  notes: string;
};

export type Summary = {
  total_confirmed_cases: number;
  total_deaths: number;
  case_fatality_rate_percent: number;
  latest_report_date: string;
  static_reports: number;
  live_items: number;
};

export type LiveItem = {
  id: number;
  title: string;
  source_name: string;
  source_url: string;
  published_at?: string;
  summary?: string;
  matched_keywords: string[];
  created_at?: string;
};

export async function fetchJson<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, { cache: 'no-store', ...options });
  if (!res.ok) throw new Error(`API error ${res.status}`);
  return res.json();
}
