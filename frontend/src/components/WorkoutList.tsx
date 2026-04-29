/** Task F1: Workout list UI (mock-friendly; F3 wires API). */
import { useEffect, useState } from "react";
import type { Workout } from "../api/client";
import { fetchWorkouts } from "../api/client";

export default function WorkoutList() {
  const [items, setItems] = useState<Workout[]>([]);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    fetchWorkouts()
      .then(setItems)
      .catch(() => setErr("Using offline preview — start API or check proxy."));
  }, []);

  return (
    <section>
      <h2>Recent workouts</h2>
      {err && <p style={{ color: "#b45309" }}>{err}</p>}
      <ul style={{ paddingLeft: "1.2rem" }}>
        {items.length === 0 && !err && <li>Loading…</li>}
        {items.map((w) => (
          <li key={w.id}>
            <strong>{w.title}</strong> — {w.duration_min} min
            {w.calories != null ? ` · ${w.calories} kcal` : ""}
          </li>
        ))}
      </ul>
    </section>
  );
}
