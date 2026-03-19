import type { SessionFormSchema } from "./types";
import { BACKEND_URL } from "@/config";

export const apiFetch = async (path: string, options: RequestInit) => {
  const res = await fetch(`${BACKEND_URL}${path}`, options);

  if (!res.ok) {
    throw new Error(await res.text());
  }

  return res.json();
};

export async function getPlotUrl(session: SessionFormSchema, view: string, runId: string) {
  const res = await fetch(`${BACKEND_URL}/plot?view=${view}&runId=${runId}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(session)
  })

  if (!res.ok) {
    throw new Error("Plot request failed")
  }

  const blob = await res.blob()
  return URL.createObjectURL(blob)
}


export async function getSubjects(): Promise<string[]> {
  const res = await fetch(`${BACKEND_URL}/participants/`)
  if (!res.ok) throw new Error("Failed to fetch subjects")
  return await res.json()
}

export async function getTasks(subject: string) {
  const res = await fetch(`${BACKEND_URL}/participants/${subject}/tasks/`)
  if (!res.ok) throw new Error("Failed to fetch tasks")
  const data = await res.json()
  return data.tasks as [string, string | null][]
}

export async function fetchTableData(
  session: SessionFormSchema, view: string, runId: string
) {
  const res = await fetch(
    `${BACKEND_URL}/data?view=${view}&runId=${runId}`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(session),
    }
  )

  if (!res.ok) {
    throw new Error("Failed to fetch table data")
  }

  return res.json()
}