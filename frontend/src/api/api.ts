
import { ENDPOINTS } from "./endpoints";
import type {
  TrainModelData,
  PredictModelData,
  EvaluateModelData,
  CompareModelData,
} from "./types";

const BACKEND_URL = "http://localhost:8000";

const apiFetch = async (path: string, options: RequestInit) => {
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

// #TODO clean function
export const getPlotUrl = (params: {
  type: string;
  subject?: string;
  task?: string;
}) => {
  const search = new URLSearchParams({
    ...params,
    t: Date.now().toString(),
  });

  return `${BACKEND_URL}${ENDPOINTS.PLOT}?${search.toString()}`;
};
