import React, { useState } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Switch } from './ui/switch';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Sheet, SheetContent, SheetTrigger } from './ui/sheet';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { MessageCircle, Users, BookOpen, FileQuestion, Menu, Plus, Calendar, FileText, Upload, Wifi, WifiOff } from 'lucide-react';
import { User } from '../App';
import { AIChatBot } from './AIChatBot';

interface TeacherDashboardProps {
  user: User;
  onNavigate: (view: string) => void;
  onLogout: () => void;
  isDark: boolean;
  setIsDark: (dark: boolean) => void;
}

export function TeacherDashboard({ user, onNavigate, onLogout, isDark, setIsDark }: TeacherDashboardProps) {
  const [isOnline, setIsOnline] = useState(true);
  const [selectedClass, setSelectedClass] = useState(user.class || 'Class 6D');
  const [selectedSubject, setSelectedSubject] = useState(user.subject || 'Mathematics');
  const [selectedLevel, setSelectedLevel] = useState('Beginner');
  const [selectedLanguage, setSelectedLanguage] = useState('English');
  const [showChat, setShowChat] = useState(false);
  const [syncStatus, setSyncStatus] = useState('synced'); // synced, syncing, error

  const classes = ['Class 6D', 'Class 7A', 'Class 8B', 'Class 9C', 'Class 10A'];
  const subjects = ['Mathematics', 'Science', 'English', 'Hindi', 'Social Science'];
  const levels = ['Beginner', 'Intermediate', 'Advanced'];
  const languages = ['English', 'Hindi', 'Tamil', 'Telugu', 'Bengali', 'Marathi'];

  const [students, setStudents] = useState([
    { id: 1, name: 'Alice Johnson', class: 'Class 6D', performance: 85, status: 'active' },
    { id: 2, name: 'Bob Smith', class: 'Class 6D', performance: 92, status: 'active' },
    { id: 3, name: 'Charlie Brown', class: 'Class 6D', performance: 78, status: 'inactive' },
    { id: 4, name: 'Diana Prince', class: 'Class 6D', performance: 88, status: 'active' },
  ]);

  const handleCreateLesson = () => {
    onNavigate('lesson-planner');
  };

  const handleGenerateQuiz = () => {
    onNavigate('quiz-creator');
  };

  const handleClassAnalytics = () => {
    onNavigate('class-analytics');
  };

  const handleCoursePlanner = () => {
    onNavigate('course-planner');
  };

  const menuItems = [
    { label: 'Dashboard', action: () => onNavigate('teacher-dashboard') },
    { label: 'Create Lesson', action: handleCreateLesson },
    { label: 'Generate Quiz', action: handleGenerateQuiz },
    { label: 'Class Analytics', action: handleClassAnalytics },
    { label: 'Course Planner', action: handleCoursePlanner },
    { label: 'Settings', action: () => {} },
    { label: 'Help', action: () => setShowChat(true) },
    { label: 'Logout', action: onLogout },
  ];

  return (
    <div className="min-h-screen bg-background p-4">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-4">
          <Sheet>
            <SheetTrigger asChild>
              <Button variant="outline" size="sm">
                <Menu className="w-4 h-4" />
              </Button>
            </SheetTrigger>
            <SheetContent side="left" className="w-64">
              <div className="space-y-4">
                <div className="px-3 py-2">
                  <h2 className="mb-2 px-4 text-lg font-semibold tracking-tight">
                    Menu
                  </h2>
                  <div className="space-y-1">
                    {menuItems.map((item, index) => (
                      <Button
                        key={index}
                        variant="ghost"
                        className="w-full justify-start"
                        onClick={item.action}
                      >
                        {item.label}
                      </Button>
                    ))}
                  </div>
                </div>
              </div>
            </SheetContent>
          </Sheet>
          <div>
            <h1 className="text-2xl tracking-tight">VIDYAVĀHINĪ</h1>
            <p className="text-sm text-muted-foreground">TEACHER DASHBOARD</p>
          </div>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <span className="text-sm">{isOnline ? 'Online' : 'Offline'}</span>
            <div className={`w-2 h-2 rounded-full ${isOnline ? 'bg-green-500' : 'bg-red-500'}`}></div>
          </div>
          <Switch checked={isDark} onCheckedChange={setIsDark} />
          <Button variant="outline" onClick={onLogout}>Logout</Button>
        </div>
      </div>

      {/* Welcome Section with Enhanced Dropdowns */}
      <div className="mb-6">
        <h2 className="text-xl mb-2">WELCOME BACK TEACHER</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
          <Select value={selectedClass} onValueChange={setSelectedClass}>
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {classes.map((cls) => (
                <SelectItem key={cls} value={cls}>{cls}</SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Select value={selectedSubject} onValueChange={setSelectedSubject}>
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {subjects.map((subject) => (
                <SelectItem key={subject} value={subject}>{subject}</SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Select value={selectedLevel} onValueChange={setSelectedLevel}>
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {levels.map((level) => (
                <SelectItem key={level} value={level}>{level}</SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Select value={selectedLanguage} onValueChange={setSelectedLanguage}>
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {languages.map((language) => (
                <SelectItem key={language} value={language}>{language}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
        <p className="text-sm text-muted-foreground">
          SUBJECT: {selectedSubject.toUpperCase()} • LEVEL: {selectedLevel.toUpperCase()} • LANGUAGE: {selectedLanguage.toUpperCase()}
        </p>
      </div>

      {/* Main Tabs */}
      <Tabs defaultValue="dashboard" className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="dashboard">Dashboard</TabsTrigger>
          <TabsTrigger value="course-planner">Course Planner</TabsTrigger>
        </TabsList>
        
        <TabsContent value="dashboard" className="mt-6">
          {/* Main Action Buttons */}
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-6">
            <Button 
              onClick={handleCreateLesson}
              className="h-20 flex flex-col items-center justify-center gap-2"
            >
              <Plus className="w-6 h-6" />
              <span>Create New Lesson</span>
            </Button>
            <Button 
              onClick={handleGenerateQuiz}
              variant="outline"
              className="h-20 flex flex-col items-center justify-center gap-2"
            >
              <FileQuestion className="w-6 h-6" />
              <span>Generate Quiz</span>
            </Button>
            <Button 
              onClick={handleClassAnalytics}
              variant="outline"
              className="h-20 flex flex-col items-center justify-center gap-2"
            >
              <Users className="w-6 h-6" />
              <span>Class Analytics</span>
            </Button>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Recent Activity */}
            <div className="lg:col-span-2 space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Recent Activity</CardTitle>
                  <div className="flex items-center gap-4">
                    <Badge variant="secondary">{selectedClass}</Badge>
                    <Badge variant="outline">{selectedSubject}</Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="space-y-2">
                      <h4>Recent Lessons</h4>
                      <div className="space-y-2">
                        <div className="flex items-center justify-between p-3 border rounded">
                          <div>
                            <p className="text-sm">Photosynthesis Basics</p>
                            <p className="text-xs text-muted-foreground">Science • {selectedClass}</p>
                          </div>
                          <div className="flex gap-2">
                            <Badge>published</Badge>
                            <Button variant="outline" size="sm" onClick={handleCreateLesson}>Edit</Button>
                          </div>
                        </div>
                        <div className="flex items-center justify-between p-3 border rounded">
                          <div>
                            <p className="text-sm">Fractions Introduction</p>
                            <p className="text-xs text-muted-foreground">Maths • {selectedClass}</p>
                          </div>
                          <div className="flex gap-2">
                            <Badge variant="secondary">draft</Badge>
                            <Button variant="outline" size="sm" onClick={handleCreateLesson}>Edit</Button>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className="space-y-2">
                      <h4>Recent Quizzes</h4>
                      <div className="space-y-2">
                        <div className="flex items-center justify-between p-3 border rounded">
                          <div>
                            <p className="text-sm">Photosynthesis Quiz</p>
                            <p className="text-xs text-muted-foreground">Science • {selectedClass}</p>
                            <p className="text-xs text-muted-foreground">10 questions • 24 submissions</p>
                          </div>
                          <div className="text-right">
                            <p className="text-sm">78% avg</p>
                            <Button variant="outline" size="sm" onClick={handleClassAnalytics}>View Results</Button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Class Statistics */}
            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Class Overview</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="text-center p-4 border rounded">
                      <div className="text-2xl">{students.length}</div>
                      <div className="text-xs text-muted-foreground">Total Students</div>
                    </div>
                    <div className="text-center p-4 border rounded">
                      <div className="text-2xl">{students.filter(s => s.status === 'active').length}</div>
                      <div className="text-xs text-muted-foreground">Active Today</div>
                    </div>
                    <div className="text-center p-4 border rounded">
                      <div className="text-2xl">12</div>
                      <div className="text-xs text-muted-foreground">Lessons Created</div>
                    </div>
                    <div className="text-center p-4 border rounded">
                      <div className="text-2xl">85%</div>
                      <div className="text-xs text-muted-foreground">Avg Performance</div>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <h4 className="text-sm">Top Performers</h4>
                    <div className="space-y-1 text-xs">
                      {students
                        .sort((a, b) => b.performance - a.performance)
                        .slice(0, 3)
                        .map((student, index) => (
                          <div key={student.id} className="flex justify-between">
                            <span>#{index + 1} {student.name}</span>
                            <span>{student.performance}%</span>
                          </div>
                        ))}
                    </div>
                  </div>
                </CardContent>
              </Card>

              <div className="text-center">
                <p className="text-sm text-muted-foreground mb-2">Welcome, {user.name}! 👨‍🏫</p>
                <p className="text-xs text-muted-foreground">Managing {selectedClass} - {selectedSubject}</p>
              </div>
            </div>
          </div>
        </TabsContent>
        
        <TabsContent value="course-planner" className="mt-6">
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg">Course Planning</h3>
                <p className="text-sm text-muted-foreground">Plan and schedule your curriculum</p>
              </div>
              <Button variant="outline">
                <Upload className="w-4 h-4 mr-2" />
                Upload Course
              </Button>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <Button 
                variant="outline"
                className="h-20 flex flex-col items-center justify-center gap-2"
              >
                <Calendar className="w-6 h-6" />
                <span>Schedule</span>
              </Button>
              <Button 
                variant="outline"
                className="h-20 flex flex-col items-center justify-center gap-2"
              >
                <Plus className="w-6 h-6" />
                <span>Generate Next Plan</span>
              </Button>
              <Button 
                variant="outline"
                className="h-20 flex flex-col items-center justify-center gap-2"
              >
                <FileText className="w-6 h-6" />
                <span>Mock Test Papers</span>
              </Button>
              <Button 
                variant="outline"
                className="h-20 flex flex-col items-center justify-center gap-2"
              >
                <BookOpen className="w-6 h-6" />
                <span>Edit Course Plan</span>
              </Button>
            </div>

            <Card>
              <CardHeader>
                <CardTitle>Current Course Plan</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="grid grid-cols-3 gap-4 text-sm">
                    <div>
                      <p className="font-medium">Week 1-2</p>
                      <p className="text-muted-foreground">Photosynthesis & Plant Biology</p>
                    </div>
                    <div>
                      <p className="font-medium">Week 3-4</p>
                      <p className="text-muted-foreground">Respiration & Circulation</p>
                    </div>
                    <div>
                      <p className="font-medium">Week 5-6</p>
                      <p className="text-muted-foreground">Light & Shadow Physics</p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>

      {/* Sync Status Footer */}
      <div className="fixed bottom-4 left-4 flex items-center gap-2 text-sm text-muted-foreground">
        {syncStatus === 'synced' && <Wifi className="w-4 h-4 text-green-500" />}
        {syncStatus === 'syncing' && <WifiOff className="w-4 h-4 text-yellow-500" />}
        {syncStatus === 'error' && <WifiOff className="w-4 h-4 text-red-500" />}
        <span>
          {syncStatus === 'synced' && 'All changes synced'}
          {syncStatus === 'syncing' && 'Syncing changes...'}
          {syncStatus === 'error' && 'Sync failed - will retry'}
        </span>
      </div>

      {/* AI Assistant Button */}
      <div className="fixed bottom-6 right-6">
        <Button
          onClick={() => setShowChat(!showChat)}
          className="rounded-full w-14 h-14 shadow-lg"
        >
          <MessageCircle className="w-6 h-6" />
        </Button>
      </div>

      {/* AI Chat Bot */}
      {showChat && (
        <div className="fixed bottom-24 right-6 w-80">
          <AIChatBot onClose={() => setShowChat(false)} userType="teacher" />
        </div>
      )}
    </div>
  );
}