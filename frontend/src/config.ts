const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
const FRONTEND_URL = import.meta.env.VITE_FRONTEND_URL;

if (!BACKEND_URL) {
  throw new Error("VITE_BACKEND_URL is not set in your .env file");
}

if (!FRONTEND_URL) {
  throw new Error("VITE_FRONTEND_URL is not set in your .env file");
}

export { BACKEND_URL, FRONTEND_URL };