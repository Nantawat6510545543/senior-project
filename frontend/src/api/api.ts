import { ENDPOINTS } from "./endpoints";
import type {
  TrainModelData,
  PredictModelData,
  EvaluateModelData,
  CompareModelData,
  SessionFormSchema,
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