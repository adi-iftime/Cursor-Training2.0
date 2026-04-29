/** Task F3: API client — uses same-origin proxy in dev (vite.config). */

const BASE = "";

export type Workout = {
  id: number;
  title: string;
  duration_min: number;
  calories: number | null;
  notes: string | null;
  activity_type_id: number | null;
  performed_at: string;
};

export type MetricsSummary = {
  total_workouts: number;
  total_minutes: number;
  total_calories: number;
  avg_duration_min: number;
};

export type KpiSnapshot = {
  workout_count: number;
  rollup_days_available: number;
  last_7d_total_calories: number;
  headline: string;
};

async function get<T>(path: string): Promise<T> {
  const r = await fetch(`${BASE}${path}`);
  if (!r.ok) throw new Error(`${r.status}`);
  return r.json() as Promise<T>;
}

export async function fetchWorkouts(): Promise<Workout[]> {
  return get<Workout[]>("/workouts");
}

export async function fetchSummary(): Promise<MetricsSummary> {
  return get<MetricsSummary>("/metrics/summary");
}

export async function fetchKpi(): Promise<KpiSnapshot> {
  return get<KpiSnapshot>("/metrics/kpi");
}
