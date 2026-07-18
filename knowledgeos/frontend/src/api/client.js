const BASE_URL = import.meta.env.VITE_BACKEND_URL;

function authHeader() {
  const token = localStorage.getItem("token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function parseError(res) {
  let data;
  try {
    data = await res.json();
  } catch (e) {
    return "Request failed";
  }
  const detail = data.detail;
  if (Array.isArray(detail)) {
    return detail.map(e => {
      const field = e.loc && e.loc.length > 0 ? e.loc[e.loc.length - 1] : "Error";
      return `${field}: ${e.msg}`;
    }).join(", ");
  }
  return detail || "Request failed";
}

export async function register(email, password, full_name) {
  const res = await fetch(`${BASE_URL}/api/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password, full_name }),
  });
  if (!res.ok) throw new Error(await parseError(res));
  return res.json();
}

export async function login(email, password) {
  const res = await fetch(`${BASE_URL}/api/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) throw new Error(await parseError(res));
  return res.json();
}

export async function uploadDocument(file) {
  const formData = new FormData();
  formData.append("file", file);
  const res = await fetch(`${BASE_URL}/api/documents`, {
    method: "POST",
    headers: authHeader(),
    body: formData,
  });
  if (!res.ok) throw new Error(await parseError(res));
  return res.json();
}

export async function listDocuments() {
  const res = await fetch(`${BASE_URL}/api/documents`, { headers: authHeader() });
  if (!res.ok) throw new Error(await parseError(res));
  return res.json();
}

export async function askQuestion(question, sessionId) {
  const res = await fetch(`${BASE_URL}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeader() },
    body: JSON.stringify({ question, session_id: sessionId }),
  });
  if (!res.ok) throw new Error(await parseError(res));
  return res.json();
}
