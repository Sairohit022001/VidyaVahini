import React, { useState, useEffect } from 'react';
import { LoginPage } from './components/LoginPage';
import { TeacherDashboard } from './components/TeacherDashboard';
import { StudentDashboard } from './components/StudentDashboard';
import { UGDashboard } from './components/UGDashboard';
import { QuizPage } from './components/QuizPage';
import { LessonView } from './components/LessonView';
import { LessonPlanner } from './components/LessonPlanner';
import { QuizCreator } from './components/QuizCreator';
import { ClassAnalytics } from './components/ClassAnalytics';

export type UserRole = 'student' | 'teacher' | 'ug' | 'guest';

export interface User {
  id: string;
  name: string;
  email: string;
  role: UserRole;
  class?: string;
  subject?: string;
}

export interface Lesson {
  id: string;
  title: string;
  subject: string;
  class: string;
  content: {
    story?: string;
    summary?: string;
    diagram?: string;
    notes?: string;
    worksheet?: string;
  };
  progress: number;
  completed: boolean;
}

export interface Quiz {
  id: string;
  title: string;
  subject: string;
  questions: QuizQuestion[];
  score?: number;
  attempts: number;
}

export interface QuizQuestion {
  id: string;
  question: string;
  options: string[];
  correct: number;
  explanation: string;
}

export default function App() {
  const [user, setUser] = useState<User | null>(null);
  const [currentView, setCurrentView] = useState<string>('login');
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    if (isDark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDark]);

  const handleLogin = (userData: User) => {
    setUser(userData);
    if (userData.role === 'teacher') {
      setCurrentView('teacher-dashboard');
    } else if (userData.role === 'ug') {
      setCurrentView('ug-dashboard');
    } else {
      setCurrentView('student-dashboard');
    }
  };

  const handleLogout = () => {
    setUser(null);
    setCurrentView('login');
  };

  const navigateTo = (view: string) => {
    setCurrentView(view);
  };

  const getBackView = () => {
    if (!user) return 'login';
    if (user.role === 'teacher') return 'teacher-dashboard';
    if (user.role === 'ug') return 'ug-dashboard';
    return 'student-dashboard';
  };

  const renderCurrentView = () => {
    switch (currentView) {
      case 'login':
        return <LoginPage onLogin={handleLogin} />;
      case 'teacher-dashboard':
        return <TeacherDashboard user={user!} onNavigate={navigateTo} onLogout={handleLogout} isDark={isDark} setIsDark={setIsDark} />;
      case 'student-dashboard':
        return <StudentDashboard user={user!} onNavigate={navigateTo} onLogout={handleLogout} isDark={isDark} setIsDark={setIsDark} />;
      case 'ug-dashboard':
        return <UGDashboard user={user!} onNavigate={navigateTo} onLogout={handleLogout} isDark={isDark} setIsDark={setIsDark} />;
      case 'quiz':
        return <QuizPage user={user!} onNavigate={navigateTo} onBack={() => navigateTo(getBackView())} />;
      case 'lesson':
        return <LessonView user={user!} onNavigate={navigateTo} onBack={() => navigateTo(getBackView())} />;
      case 'lesson-planner':
        return <LessonPlanner user={user!} onNavigate={navigateTo} onBack={() => navigateTo('teacher-dashboard')} />;
      case 'quiz-creator':
        return <QuizCreator user={user!} onNavigate={navigateTo} onBack={() => navigateTo('teacher-dashboard')} />;
      case 'class-analytics':
        return <ClassAnalytics user={user!} onNavigate={navigateTo} onBack={() => navigateTo('teacher-dashboard')} />;
      case 'course-planner':
        // For now, redirect to teacher dashboard - you can create a separate component later
        return <TeacherDashboard user={user!} onNavigate={navigateTo} onLogout={handleLogout} isDark={isDark} setIsDark={setIsDark} />;
      default:
        return <LoginPage onLogin={handleLogin} />;
    }
  };

  return (
    <div className="min-h-screen bg-background text-foreground">
      {renderCurrentView()}
    </div>
  );
}