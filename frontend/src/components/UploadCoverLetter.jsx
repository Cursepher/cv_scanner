import React, { useState } from "react";

export default function UploadCoverLetter() {
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setError("");
    setResult(null);
    const selected = e.target.files[0];
    if (selected && !selected.name.endsWith(".pdf")) {
      setError("Only PDF files are allowed.");
      setFile(null);
    } else {
      setFile(selected);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError("Please select a PDF file.");
      return;
    }
    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      if (data.error) {
        setError(data.error);
      } else {
        setResult(data);
      }
    } catch (err) {
      setError("Failed to upload/process file.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: "auto", padding: 20 }}>
      <h1>Upload your PDF Cover Letter</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" accept=".pdf" onChange={handleFileChange} />
        <button type="submit" disabled={loading} style={{ marginLeft: 10 }}>
          {loading ? "Uploading..." : "Upload & Process"}
        </button>
      </form>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {result && (
        <div style={{ marginTop: 20 }}>
          <h2>Redacted Text:</h2>
          <pre style={{ whiteSpace: "pre-wrap", background: "#eee", padding: 10 }}>
            {result.redacted}
          </pre>
          <h2>Skills Detected:</h2>
          <pre style={{ whiteSpace: "pre-wrap", background: "#eee", padding: 10 }}>
            {JSON.stringify(result.skills, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
