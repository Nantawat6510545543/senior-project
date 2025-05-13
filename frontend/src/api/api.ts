const BACKEND_URL = "http://localhost:3000";

export const trainModel = async () => {
  const res = await fetch(`${BACKEND_URL}/train`, { method: "POST" });
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