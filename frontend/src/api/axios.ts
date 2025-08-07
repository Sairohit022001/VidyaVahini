import axios from "axios";

const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "/api",
  headers: {
    "x-api-key": "hackathon-demo-key-2025",
    "x-user-role": "teacher",
    "Content-Type": "application/json",
  },
});

export default axiosInstance;
