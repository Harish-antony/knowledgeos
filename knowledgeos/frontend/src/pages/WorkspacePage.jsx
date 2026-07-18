import { useEffect, useState, useRef } from "react";
import { uploadDocument, listDocuments, askQuestion } from "../api/client";

export default function WorkspacePage() {
  const [documents, setDocuments] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [sessionId, setSessionId] = useState(null);
  const [asking, setAsking] = useState(false);
  const fileInput = useRef();

  async function loadDocs() {
    const data = await listDocuments();
    setDocuments(data);
  }

  useEffect(() => {
    loadDocs();
  }, []);

  async function handleUpload(e) {
    const file = e.target.files[0];
    if (!file) return;
    setUploading(true);
    try {
      await uploadDocument(file);
      await loadDocs();
    } catch (err) {
      alert(err.message);
    } finally {
      setUploading(false);
      fileInput.current.value = "";
    }
  }

  async function handleAsk(e) {
    e.preventDefault();
    if (!question.trim()) return;
    const q = question;
    setMessages((prev) => [...prev, { role: "user", content: q }]);
    setQuestion("");
    setAsking(true);
    try {
      const res = await askQuestion(q, sessionId);
      setSessionId(res.session_id);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: res.answer, citations: res.citations },
      ]);
    } catch (err) {
      setMessages((prev) => [...prev, { role: "assistant", content: `Error: ${err.message}` }]);
    } finally {
      setAsking(false);
    }
  }

  return (
    <div style={{ display: "flex", height: "100vh" }}>
      {/* Sidebar: documents */}
      <aside style={{ width: 280, borderRight: "1px solid #222", padding: 20, overflowY: "auto" }}>
        <h2 style={{ fontSize: 16, marginBottom: 16 }}>Documents</h2>
        <label
          style={{
            display: "block",
            textAlign: "center",
            padding: 10,
            border: "1px dashed #444",
            borderRadius: 8,
            cursor: "pointer",
            marginBottom: 16,
            color: "#9ca3af",
          }}
        >
          {uploading ? "Uploading..." : "+ Upload PDF/DOCX/TXT"}
          <input
            ref={fileInput}
            type="file"
            accept=".pdf,.docx,.txt"
            onChange={handleUpload}
            style={{ display: "none" }}
          />
        </label>
        {documents.map((doc) => (
          <div key={doc.id} style={{ padding: "8px 0", borderBottom: "1px solid #1c1c22", fontSize: 13 }}>
            <div>{doc.filename}</div>
            <div style={{ color: doc.status === "ready" ? "#4ade80" : "#facc15", fontSize: 11 }}>
              {doc.status} · {doc.chunk_count} chunks
            </div>
          </div>
        ))}
      </aside>

      {/* Chat area */}
      <main style={{ flex: 1, display: "flex", flexDirection: "column", padding: 20 }}>
        <h2 style={{ fontSize: 16, marginBottom: 16 }}>Ask your documents</h2>
        <div style={{ flex: 1, overflowY: "auto", marginBottom: 16 }}>
          {messages.map((m, i) => (
            <div key={i} style={{ marginBottom: 16 }}>
              <div style={{ fontWeight: 600, marginBottom: 4, color: m.role === "user" ? "#818cf8" : "#4ade80" }}>
                {m.role === "user" ? "You" : "KnowledgeOS"}
              </div>
              <div style={{ whiteSpace: "pre-wrap" }}>{m.content}</div>
              {m.citations?.length > 0 && (
                <div style={{ marginTop: 8, fontSize: 12, color: "#9ca3af" }}>
                  {m.citations.map((c, ci) => (
                    <div key={ci} style={{ marginBottom: 4 }}>
                      [{ci + 1}] {c.filename} — "{c.chunk_text.slice(0, 100)}..." (score: {c.score})
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
        <form onSubmit={handleAsk} style={{ display: "flex", gap: 8 }}>
          <input
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask a question about your documents..."
            style={{ flex: 1, padding: 12, borderRadius: 8, border: "1px solid #333", background: "#16161d", color: "#eee" }}
          />
          <button
            disabled={asking}
            style={{ padding: "12px 20px", borderRadius: 8, background: "#4f46e5", color: "#fff", border: "none" }}
          >
            {asking ? "..." : "Ask"}
          </button>
        </form>
      </main>
    </div>
  );
}
