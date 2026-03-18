import { useState } from "react";
import { uploadSession } from "../api/backend";

export default function Upload() {
  const [title, setTitle] = useState("");
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    // Prevent full page refresh so React can handle submit state.
    event.preventDefault();
    setMessage("");
    setError("");

    // Basic client-side checks before we call the backend.
    if (!title.trim()) {
      setError("Title is required.");
      return;
    }

    if (!file) {
      setError("Please select a file.");
      return;
    }

    setLoading(true);

    try {
      // Send upload request through our shared API helper.
      const payload = await uploadSession({ title: title.trim(), file });
      setMessage(payload.message || "Upload successful.");
      setTitle("");
      setFile(null);
    } catch (err) {
      setError(err.message || "Upload failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="container">
      <h1>Upload Session</h1>

      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="title">Title</label>
          <input
            id="title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Class recording title"
          />
        </div>

        <div>
          <label htmlFor="file">Recording</label>
          <input
            id="file"
            type="file"
            accept=".mp4,.mp3,.wav,.m4a"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
          />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? "Uploading..." : "Upload"}
        </button>
      </form>

      {message ? <p>{message}</p> : null}
      {error ? <p>{error}</p> : null}
    </div>
  );
}
