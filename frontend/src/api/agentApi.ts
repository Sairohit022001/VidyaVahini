// src/api/agentApi.ts
import axiosInstance from "./axios";


const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const runAgentPrompt = async (prompt: string) => {
  const response = await axiosInstance.post("/run", { prompt });
  return response.data;
};

// ✅ Core Curriculum Agents
export const runLessonAgent = async (prompt: string) => {
  return await axiosInstance.post("/api/lesson_planner_agent", { prompt });
};
export const runStoryAgent = async (prompt: string) => {
  return await axiosInstance.post("/api/story_generator_agent", { prompt });
};
export const runQuizAgent = async (prompt: string) => {
  return await axiosInstance.post("/api/quiz_generator_agent", { prompt });
};
export const runVoiceTutorAgent = async (prompt: string) => {
  return await axiosInstance.post("/api/voice_tutor_agent", { prompt });
};
export const runVisualAgent = async (prompt: string) => {
  return await axiosInstance.post("/api/visual_generator_agent", { prompt });
};

// ✅ Course Planning & Dashboard
export const runCoursePlannerAgent = async (prompt: string) => {
  return await axiosInstance.post("/api/course_planner_agent", { prompt });
};
export const runTeacherDashboardAgent = async (prompt: string) => {
  return await axiosInstance.post("/api/teacher_dashboard_agent", { prompt });
};

// ✅ Advanced Learning Agents
export const runAskMeAgent = async (prompt: string) => {
  return await axiosInstance.post("/api/ask_me_anything_agent", { prompt });
};
export const runSyncAgent = async (prompt: string) => {
  return await axiosInstance.post("/api/content_sync_agent", { prompt });
};
export const runContentCreatorAgent = async (prompt: string) => {
  return await axiosInstance.post("/api/content_creator_agent", { prompt });
};
export const runPredictiveAnalyticsAgent = async (prompt: string) => {
  return await axiosInstance.post("/api/predictive_analytics_agent", { prompt });
};
export const runStudentAnalyticsAgent = async (prompt: string) => {
  return await axiosInstance.post("/api/student_analytics_agent", { prompt });
};
export const runGamificationAgent = async (prompt: string) => {
  return await axiosInstance.post("/api/gamification_agent", { prompt });
};

// ✅ Multimodal + Research
export const runMultimodalResearchAgent = async (prompt: string) => {
  return await axiosInstance.post("/api/multimodal_research_agent", { prompt });
};

// Optional: PDF/Research Expansion if still used
export const runResearchAgent = async (prompt: string) => {
  return await axiosInstance.post("/api/research_fetcher_agent", { prompt });
};
export const runLessonFromPaperAgent = async (prompt: string) => {
  return await axiosInstance.post("/api/lesson_from_research_agent", { prompt });
};
export const runQAGenFromTopicAgent = async (prompt: string) => {
  return await axiosInstance.post("/api/qa_generator_topic_agent", { prompt });
};
export const runQAGenFromPaperAgent = async (prompt: string) => {
  return await axiosInstance.post("/api/qa_generator_paper_agent", { prompt });
};
export const runPdfLessonAgent = async (prompt: string) => {
  return await axiosInstance.post("/api/lesson_from_pdf_agent", { prompt });
};
export const runPdfQAAgent = async (prompt: string) => {
  return await axiosInstance.post("/api/qa_from_pdf_agent", { prompt });
};
export const runPdfSummaryAgent = async (prompt: string) => {
  return await axiosInstance.post("/api/summary_from_pdf_agent", { prompt });
};
export const runSummaryAgent = async (prompt: string) => {
  return await axiosInstance.post("/api/summary_generator_agent", { prompt });
};
export const runLanguageTranslateAgent = async (prompt: string) => {
  return await axiosInstance.post("/api/language_translator_agent", { prompt });
};
