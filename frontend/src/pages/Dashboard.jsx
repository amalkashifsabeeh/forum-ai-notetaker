import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getSessions } from "../api/backend";

export default function Dashboard() {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    // Load sessions once when this page mounts.
    async function loadSessions() {
      setLoading(true);
      setError("");

      try {
        const payload = await getSessions();
        // Backend wraps rows inside payload.data.
        setSessions(payload.data || []);
      } catch (err) {
        setError(err.message || "Failed to load sessions.");
      } finally {
        setLoading(false);
      }
    }

    loadSessions();
  }, []);

  return (
    <div className="container">
      <h1>Dashboard</h1>

      {loading ? <p>Loading sessions...</p> : null}
      {error ? <p>{error}</p> : null}

      {!loading && !error && sessions.length === 0 ? (
        <p>No sessions yet. Upload one to get started.</p>
      ) : null}

      {!loading && !error && sessions.length > 0 ? (
        <ul>
          {sessions.map((session) => (
            <li key={session.id}>
              <strong>{session.title}</strong> — {session.status} —{" "}
              <Link to={`/notes/${session.id}`}>View transcript/notes</Link>
            </li>
          ))}
        </ul>
      ) : null}
    </div>
  );
}
