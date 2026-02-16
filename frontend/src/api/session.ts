import type { SchemaEndpoints } from "@/hooks/useSchema";
import type { PipelineSession } from "./types";

const BACKEND_URL = "http://localhost:8000";

export function getSid(): string | null {
  return localStorage.getItem("sid");
}

export function setSid(sid: string) {
  localStorage.setItem("sid", sid);
}

export function refreshSession(data: any) {
  if (data?.session_id) {
    setSid(data.session_id);
  }
}

export async function createSession(): Promise<string> {
  const res = await fetch(`${BACKEND_URL}/session`, { method: "POST" });
  if (!res.ok) throw new Error("Failed to create session");

  const data = await res.json();
  setSid(data.session_id);
  return data.session_id;
}

// Load entire session
export async function getSession() {
  let sid = getSid();

  // first page load
  if (!sid) {
    sid = await createSession();
  }

  const res = await fetch(`${BACKEND_URL}/session/${sid}`);
  const data = await res.json();

  // backend restart recovery
  refreshSession(data);

  return data;
}

// Update one schema section
export async function patchSession(
  endpoint: SchemaEndpoints,
  values: PipelineSession
) {
  let sid = getSid();

  // page opened and user typed before load finished
  if (!sid) {
    sid = await createSession();
  }

  const res = await fetch(`${BACKEND_URL}/session/${sid}/${endpoint}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(values),
  });

  const data = await res.json();

  // backend restarted → new sid returned
  refreshSession(data);
}