/** Task F2: Metrics dashboard (mock-friendly). */
import { useEffect, useState } from "react";
import type { KpiSnapshot, MetricsSummary } from "../api/client";
import { fetchKpi, fetchSummary } from "../api/client";

export default function MetricsDashboard() {
  const [summary, setSummary] = useState<MetricsSummary | null>(null);
  const [kpi, setKpi] = useState<KpiSnapshot | null>(null);

  useEffect(() => {
    Promise.all([fetchSummary(), fetchKpi()])
      .then(([s, k]) => {
        setSummary(s);
        setKpi(k);
      })
      .catch(() => {
        setSummary({
          total_workouts: 0,
          total_minutes: 0,
          total_calories: 0,
          avg_duration_min: 0,
        });
        setKpi({
          workout_count: 0,
          rollup_days_available: 0,
          last_7d_total_calories: 0,
          headline: "Start logging workouts to see trends.",
        });
      });
  }, []);

  return (
    <section>
      <h2>Dashboard</h2>
      {summary && (
        <p>
          <strong>{summary.total_workouts}</strong> workouts ·{" "}
          <strong>{summary.total_minutes.toFixed(0)}</strong> min total · avg{" "}
          <strong>{summary.avg_duration_min.toFixed(1)}</strong> min/session
        </p>
      )}
      {kpi && <p style={{ fontStyle: "italic" }}>{kpi.headline}</p>}
    </section>
  );
}
