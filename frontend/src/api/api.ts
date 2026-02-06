
import type { SchemaEndpoints } from "@/hooks/useSchema";
import { ENDPOINTS } from "./endpoints";
import type {
  TrainModelData,
  PredictModelData,
  EvaluateModelData,
  CompareModelData,
  SingleSubjectTask,
} from "./types";

const BACKEND_URL = "http://localhost:8000";

export const apiFetch = async (path: string, options: RequestInit) => {
  const res = await fetch(`${BACKEND_URL}${path}`, options);

  if (!res.ok) {
    throw new Error(await res.text());
  }

  return res.json();
};

export const trainModel = (data: TrainModelData) =>
  apiFetch(ENDPOINTS.TRAIN, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

export const predictModel = (data: PredictModelData) => {
  const formData = new FormData();
  formData.append("file", data.file);
  formData.append("model_name", data.model_name);

  return apiFetch(ENDPOINTS.PREDICT, {
    method: "POST",
    body: formData,
  });
};

export const evaluateModel = (data: EvaluateModelData) => {
  const formData = new FormData();
  formData.append("file", data.file);

  return apiFetch(ENDPOINTS.EVALUATE, {
    method: "POST",
    body: formData,
  });
};

export const compareModel = (data: CompareModelData) => {
  const formData = new FormData();
  formData.append("file1", data.file1);
  formData.append("file2", data.file2);

  return apiFetch(ENDPOINTS.COMPARE, {
    method: "POST",
    body: formData,
  });
};

export const getPlotUrl = (params: {
  type: string;
  task: SingleSubjectTask
}) => {
  const search = new URLSearchParams({
    type: params.type,
    subject: params.task.subject,
    task: params.task.task,
    t: Date.now().toString(),
  })

  if (params.task.run) {
    search.set("run", params.task.run)
  }

  return `${BACKEND_URL}${ENDPOINTS.PLOT}?${search.toString()}`;
};


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


// Sessions
export async function createSession(): Promise<string> {
  const res = await fetch(`${BACKEND_URL}/session`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({})
  })

  if (!res.ok) throw new Error("Failed to create session")

  const data = await res.json()
  return data.session_id
}


export async function getSession(sessionId: string) {
  if (!sessionId) throw new Error("getSession: sessionId required")

  const res = await fetch(`${BACKEND_URL}/session/${sessionId}`)
  if (!res.ok) throw new Error("Failed to fetch session")

  return await res.json()
}

export async function patchSession(
  sessionId: string,
  endpoint: SchemaEndpoints,
  values: Record<string, any>
) {
  const res = await fetch(`${BACKEND_URL}/session/${sessionId}/${endpoint}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(values),
  })

  if (!res.ok) throw new Error("Failed to patch session")
}