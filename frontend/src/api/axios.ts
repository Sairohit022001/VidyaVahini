// src/api/axios.ts
import axios from "axios";

const axiosInstance = axios.create({
  baseURL: "http://localhost:8000/api",
  headers: {
    "x-api-key": "hackathon-demo-key-2025",
    "x-user-role": "teacher",
    "Content-Type": "application/json",
  },
});

export default axiosInstance;
