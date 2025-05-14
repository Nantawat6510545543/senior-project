const BACKEND_URL = "http://localhost:8000";

interface TrainModelData {
  model_name: string;
  dataset_name: string;
  epochs: number;
  kfolds: number;
}

interface PredictModelData {
  file: File,
  model_name: string
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
    throw new Error(`Failed to fetch: ${res.statusText}`);
  }

  return await res.json();
};


export const predictModel = async (data: PredictModelData) => {
  const formData = new FormData();
  formData.append("file", data.file); // Append the actual file to the FormData
  formData.append("model_name", data.model_name);

  const res = await fetch(`${BACKEND_URL}/predict`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch: ${res.statusText}`);
  }

  return await res.json(); // Return the prediction result
};
export const compareModel = async () => {
  const res = await fetch(`${BACKEND_URL}/compare`, { method: "POST" });
  return await res.json();
};

export const evaluateModel = async () => {
  const res = await fetch(`${BACKEND_URL}/evaluate`, { method: "POST" });
  return await res.json();
};