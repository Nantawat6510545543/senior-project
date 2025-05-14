const BACKEND_URL = "http://localhost:8000";

interface TrainModelData {
  model_name: string;
  dataset_name: string;
  epochs: number;
  kfolds: number;
}

export const trainModel = async (data: TrainModelData) => {
  console.log(data)
  const res = await fetch(`${BACKEND_URL}/train`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!res.ok) {
    const error = await res.json();
    console.error(`Backend error ${res.status}:`, error);
    throw new Error("Failed to train model");
  }

  return await res.json();
};

export const predictModel = async () => {
  const res = await fetch(`${BACKEND_URL}/predict`, { method: "POST" });
  return await res.json();
};

export const compareModel = async () => {
  const res = await fetch(`${BACKEND_URL}/compare`, { method: "POST" });
  return await res.json();
};

export const evaluateModel = async () => {
  const res = await fetch(`${BACKEND_URL}/evaluate`, { method: "POST" });
  return await res.json();
};