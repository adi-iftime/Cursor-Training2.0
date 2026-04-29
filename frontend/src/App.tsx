import WorkoutList from "./components/WorkoutList";
import MetricsDashboard from "./components/MetricsDashboard";

export default function App() {
  return (
    <div>
      <h1>Personal Fitness Tracker</h1>
      <MetricsDashboard />
      <WorkoutList />
    </div>
  );
}
