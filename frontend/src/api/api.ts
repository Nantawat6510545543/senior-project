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

interface EvaluateModelData {
  file: File,
}

interface CompareModelData {
  file1: File,
  file2: File
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
    throw new Error(`Error: ${res.status} - ${res.statusText}`);
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
    throw new Error(`Error: ${res.status} - ${res.statusText}`);
  }

  return await res.json();
};

export const evaluateModel = async (data: EvaluateModelData) => {
  const formData = new FormData();
  formData.append("file", data.file);

  const res = await fetch(`${BACKEND_URL}/evaluate`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    throw new Error(`Error: ${res.status} - ${res.statusText}`);
  }

  return await res.json();
};

export const compareModel = async (data: CompareModelData) => {
  const formData = new FormData();
  formData.append("file1", data.file1);
  formData.append("file2", data.file2);

  const res = await fetch(`${BACKEND_URL}/compare`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    throw new Error(`Error: ${res.status} - ${res.statusText}`);
  }

  return await res.json();
};