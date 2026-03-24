import type { SessionFormSchema } from "./types";
import { BACKEND_URL } from "@/config";

export const apiFetch = async (path: string, options: RequestInit = {}) => {
  const headers = {
    "ngrok-skip-browser-warning": "true",
    ...options.headers,
  };

  const res = await fetch(`${BACKEND_URL}${path}`, { 
    ...options, 
    headers 
  });

  if (!res.ok) {
    throw new Error(await res.text());
  }

  return res.json();
};

export async function getPlotUrl(session: SessionFormSchema, view: string, runId: string) {
  const res = await fetch(`${BACKEND_URL}/plot/?view=${view}&runId=${runId}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "ngrok-skip-browser-warning": "true" 
    },
    body: JSON.stringify(session)
  });

  if (!res.ok) {
    throw new Error("Plot request failed");
  }

  const blob = await res.blob();
  return URL.createObjectURL(blob);
}

export async function getSubjects(): Promise<string[]> {
  return apiFetch(`/participants/`);
}

export async function getTasks(subject: string) {
  const data = await apiFetch(`/participants/${subject}/tasks/`);
  return data.tasks as [string, string | null][];
}

export async function fetchTableData(
  session: SessionFormSchema, view: string, runId: string
) {
  return apiFetch(`/data/?view=${view}&runId=${runId}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(session),
  });
}