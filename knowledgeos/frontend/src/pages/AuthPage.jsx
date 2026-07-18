import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login, register } from "../api/client";

const inputStyle = {
  width: "100%",
  padding: "12px",
  marginBottom: "12px",
  borderRadius: "8px",
  border: "1px solid #333",
  background: "#16161d",
  color: "#eee",
};

export default function AuthPage() {
  const [mode, setMode] = useState("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  async function submit(e) {
    e.preventDefault();
    setError("");
    try {
      const data =
        mode === "login" ? await login(email, password) : await register(email, password, fullName);
      localStorage.setItem("token", data.token);
      localStorage.setItem("user", JSON.stringify(data.user));
      navigate("/");
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div style={{ maxWidth: 380, margin: "80px auto", padding: 24 }}>
      <h1 style={{ marginBottom: 24 }}>KnowledgeOS</h1>
      <form onSubmit={submit}>
        {mode === "register" && (
          <input
            style={inputStyle}
            placeholder="Full name"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            required
          />
        )}
        <input
          style={inputStyle}
          placeholder="Email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          style={inputStyle}
          placeholder="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        {error && <p style={{ color: "#f87171" }}>{error}</p>}
        <button
          style={{ width: "100%", padding: 12, borderRadius: 8, background: "#4f46e5", color: "#fff", border: "none" }}
        >
          {mode === "login" ? "Log In" : "Register"}
        </button>
      </form>
      <p style={{ marginTop: 16, cursor: "pointer", color: "#9ca3af" }} onClick={() => setMode(mode === "login" ? "register" : "login")}>
        {mode === "login" ? "No account? Register" : "Have an account? Log in"}
      </p>
    </div>
  );
}
