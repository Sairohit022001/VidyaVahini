import React, { useState } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Switch } from './ui/switch';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Sheet, SheetContent, SheetTrigger } from './ui/sheet';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from './ui/dialog';
import { MessageCircle, Users, BookOpen, FileQuestion, Menu, Plus, Calendar, FileText, Upload, Wifi, WifiOff, Download, Edit, UserPlus, School } from 'lucide-react';
import { User } from '../App';
import { AIChatBot } from './AIChatBot';

interface TeacherDashboardProps {
  user: User;
  onNavigate: (view: string) => void;
  onLogout: () => void;
  isDark: boolean;
  setIsDark: (dark: boolean) => void;
}

interface CoursePlanItem {
  topic: string;
  duration: string;
}

interface ClassData {
  id: string;
  grade: string;
  section: string;
  subject: string;
  teacherUID: string;
}

interface StudentData {
  id: string;
  name: string;
  classId?: string;
}

export function TeacherDashboard({ user, onNavigate, onLogout, isDark, setIsDark }: TeacherDashboardProps) {
  const [isOnline, setIsOnline] = useState(true);
  const [showChat, setShowChat] = useState(false);
  const [syncStatus, setSyncStatus] = useState('synced'); // synced, syncing, error
  const [coursePlan, setCoursePlan] = useState<CoursePlanItem[]>([]);
  const [isGeneratingPlan, setIsGeneratingPlan] = useState(false);
  
  // Class Management State
  const [classes, setClasses] = useState<ClassData[]>([
    { id: 'class-1', grade: '6', section: 'D', subject: 'Mathematics', teacherUID: user.id },
    { id: 'class-2', grade: '7', section: 'A', subject: 'Science', teacherUID: user.id }
  ]);
  const [showCreateClassDialog, setShowCreateClassDialog] = useState(false);
  const [showAddStudentDialog, setShowAddStudentDialog] = useState(false);
  
  // Create Class Form State
  const [newClassGrade, setNewClassGrade] = useState('');
  const [newClassSection, setNewClassSection] = useState('');
  const [newClassSubject, setNewClassSubject] = useState('');
  
  // Add Student Form State
  const [selectedClassId, setSelectedClassId] = useState('');
  const [studentId, setStudentId] = useState('');

  const grades = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'];
  const sections = ['A', 'B', 'C', 'D', 'E'];
  const subjects = ['Mathematics', 'Science', 'English', 'Hindi', 'Social Science', 'Physics', 'Chemistry', 'Biology'];

  const [students, setStudents] = useState([
    { id: 1, name: 'Alice Johnson', class: 'Class 6D', performance: 85, status: 'active' },
    { id: 2, name: 'Bob Smith', class: 'Class 6D', performance: 92, status: 'active' },
    { id: 3, name: 'Charlie Brown', class: 'Class 6D', performance: 78, status: 'inactive' },
    { id: 4, name: 'Diana Prince', class: 'Class 6D', performance: 88, status: 'active' },
  ]);

  const handleCreateClass = async () => {
    if (!newClassGrade || !newClassSection || !newClassSubject) {
      alert('Please fill all required fields');
      return;
    }

    setSyncStatus('syncing');
    try {
      const newClass: ClassData = {
        id: `class-${Date.now()}`,
        grade: newClassGrade,
        section: newClassSection,
        subject: newClassSubject,
        teacherUID: user.id
      };

      // Here you would call your backend API
      // const response = await fetch('/api/create-class', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify(newClass)
      // });

      // Simulate API call
      setTimeout(() => {
        setClasses(prev => [...prev, newClass]);
        setNewClassGrade('');
        setNewClassSection('');
        setNewClassSubject('');
        setShowCreateClassDialog(false);
        setSyncStatus('synced');
      }, 1000);
    } catch (error) {
      console.error('Create class failed:', error);
      setSyncStatus('error');
    }
  };

  const handleAddStudent = async () => {
    if (!selectedClassId || !studentId) {
      alert('Please select a class and enter student ID');
      return;
    }

    setSyncStatus('syncing');
    try {
      const addStudentData = {
        classId: selectedClassId,
        studentId: studentId
      };

      // Here you would call your backend API
      // const response = await fetch('/api/add-student-to-class', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify(addStudentData)
      // });

      // Simulate API call
      setTimeout(() => {
        setSelectedClassId('');
        setStudentId('');
        setShowAddStudentDialog(false);
        setSyncStatus('synced');
        alert(`Student ${studentId} added to class successfully!`);
      }, 1000);
    } catch (error) {
      console.error('Add student failed:', error);
      setSyncStatus('error');
    }
  };

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

  const handleUploadCourse = () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.pdf';
    input.onchange = async (e) => {
      const file = (e.target as HTMLInputElement).files?.[0];
      if (file) {
        setSyncStatus('syncing');
        try {
          // Here you would send the file to your backend
          const formData = new FormData();
          formData.append('file', file);
          
          // Simulated API call - replace with actual backend call
          // const response = await fetch('/api/upload-course', {
          //   method: 'POST',
          //   body: formData
          // });
          // const data = await response.json();
          
          // For now, simulate a response
          setTimeout(() => {
            const mockData = [
              { topic: 'Introduction to Algebra', duration: '2 weeks' },
              { topic: 'Linear Equations', duration: '3 weeks' },
              { topic: 'Quadratic Equations', duration: '2 weeks' },
              { topic: 'Functions and Graphs', duration: '3 weeks' }
            ];
            setCoursePlan(mockData);
            setSyncStatus('synced');
          }, 2000);
        } catch (error) {
          console.error('Upload failed:', error);
          setSyncStatus('error');
        }
      }
    };
    input.click();
  };

  const handleGenerateCoursePlan = async () => {
    setIsGeneratingPlan(true);
    setSyncStatus('syncing');
    
    try {
      // Here you would call your backend API to generate course plan
      // const response = await fetch('/api/generate-course-plan', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({
      //     teacherUID: user.id
      //   })
      // });
      // const data = await response.json();
      
      // For now, simulate a response
      setTimeout(() => {
        const mockGeneratedPlan = [
          { topic: 'Fundamentals of Mathematics', duration: '1 week' },
          { topic: 'Number Systems', duration: '2 weeks' },
          { topic: 'Basic Operations', duration: '2 weeks' },
          { topic: 'Fractions and Decimals', duration: '3 weeks' },
          { topic: 'Geometry Basics', duration: '2 weeks' },
          { topic: 'Measurement', duration: '2 weeks' }
        ];
        setCoursePlan(mockGeneratedPlan);
        setIsGeneratingPlan(false);
        setSyncStatus('synced');
      }, 3000);
    } catch (error) {
      console.error('Generation failed:', error);
      setIsGeneratingPlan(false);
      setSyncStatus('error');
    }
  };

  const handleDownloadCoursePlan = () => {
    if (coursePlan.length === 0) return;
    
    const csvContent = "data:text/csv;charset=utf-8," 
      + "Topic,Duration\n"
      + coursePlan.map(item => `"${item.topic}","${item.duration}"`).join("\n");
    
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `course_plan_${user.name}_${Date.now()}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
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

      {/* Welcome Section with Class Management Buttons */}
      <div className="mb-6">
        <h2 className="text-xl mb-4">WELCOME BACK TEACHER</h2>
        <div className="grid grid-cols-2 gap-4 mb-4">
          <Dialog open={showCreateClassDialog} onOpenChange={setShowCreateClassDialog}>
            <DialogTrigger asChild>
              <Button className="h-16 flex flex-col items-center justify-center gap-2">
                <School className="w-6 h-6" />
                <span>Add Class</span>
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Create New Class</DialogTitle>
              </DialogHeader>
              <div className="space-y-4">
                <div>
                  <Label htmlFor="grade">Grade</Label>
                  <Select value={newClassGrade} onValueChange={setNewClassGrade}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select Grade" />
                    </SelectTrigger>
                    <SelectContent>
                      {grades.map((grade) => (
                        <SelectItem key={grade} value={grade}>Grade {grade}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="section">Section</Label>
                  <Select value={newClassSection} onValueChange={setNewClassSection}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select Section" />
                    </SelectTrigger>
                    <SelectContent>
                      {sections.map((section) => (
                        <SelectItem key={section} value={section}>Section {section}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="subject">Subject</Label>
                  <Select value={newClassSubject} onValueChange={setNewClassSubject}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select Subject" />
                    </SelectTrigger>
                    <SelectContent>
                      {subjects.map((subject) => (
                        <SelectItem key={subject} value={subject}>{subject}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div className="flex gap-2 pt-4">
                  <Button onClick={handleCreateClass} className="flex-1">
                    Create Class
                  </Button>
                  <Button variant="outline" onClick={() => setShowCreateClassDialog(false)} className="flex-1">
                    Cancel
                  </Button>
                </div>
              </div>
            </DialogContent>
          </Dialog>

          <Dialog open={showAddStudentDialog} onOpenChange={setShowAddStudentDialog}>
            <DialogTrigger asChild>
              <Button variant="outline" className="h-16 flex flex-col items-center justify-center gap-2">
                <UserPlus className="w-6 h-6" />
                <span>Add Student</span>
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Add Student to Class</DialogTitle>
              </DialogHeader>
              <div className="space-y-4">
                <div>
                  <Label htmlFor="classId">Select Class</Label>
                  <Select value={selectedClassId} onValueChange={setSelectedClassId}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select Class" />
                    </SelectTrigger>
                    <SelectContent>
                      {classes.map((cls) => (
                        <SelectItem key={cls.id} value={cls.id}>
                          Grade {cls.grade}{cls.section} - {cls.subject}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="studentId">Student ID</Label>
                  <Input
                    id="studentId"
                    value={studentId}
                    onChange={(e) => setStudentId(e.target.value)}
                    placeholder="Enter Student ID"
                  />
                </div>
                <div className="flex gap-2 pt-4">
                  <Button onClick={handleAddStudent} className="flex-1">
                    Add Student
                  </Button>
                  <Button variant="outline" onClick={() => setShowAddStudentDialog(false)} className="flex-1">
                    Cancel
                  </Button>
                </div>
              </div>
            </DialogContent>
          </Dialog>
        </div>
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
                    <Badge variant="secondary">My Classes</Badge>
                    <Badge variant="outline">{classes.length} Active</Badge>
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
                            <p className="text-xs text-muted-foreground">Science • Grade 6D</p>
                          </div>
                          <div className="flex gap-2">
                            <Badge>published</Badge>
                            <Button variant="outline" size="sm" onClick={handleCreateLesson}>Edit</Button>
                          </div>
                        </div>
                        <div className="flex items-center justify-between p-3 border rounded">
                          <div>
                            <p className="text-sm">Fractions Introduction</p>
                            <p className="text-xs text-muted-foreground">Maths • Grade 6D</p>
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
                            <p className="text-xs text-muted-foreground">Science • Grade 6D</p>
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
                <p className="text-xs text-muted-foreground">Managing {classes.length} classes</p>
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
              <Button variant="outline" onClick={handleUploadCourse}>
                <Upload className="w-4 h-4 mr-2" />
                Upload Course
              </Button>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <Button 
                onClick={handleGenerateCoursePlan}
                disabled={isGeneratingPlan}
                className="h-20 flex flex-col items-center justify-center gap-2"
              >
                <Plus className="w-6 h-6" />
                <span>{isGeneratingPlan ? 'Generating...' : 'Generate Course Plan'}</span>
              </Button>
              <Button 
                variant="outline"
                className="h-20 flex flex-col items-center justify-center gap-2"
              >
                <Edit className="w-6 h-6" />
                <span>Edit Course Plan</span>
              </Button>
            </div>

            {coursePlan.length > 0 && (
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle>Generated Course Plan</CardTitle>
                    <Button variant="outline" size="sm" onClick={handleDownloadCoursePlan}>
                      <Download className="w-4 h-4 mr-2" />
                      Download
                    </Button>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <div className="grid grid-cols-2 gap-4 font-semibold text-sm border-b pb-2">
                      <div>Topic</div>
                      <div>Duration</div>
                    </div>
                    {coursePlan.map((item, index) => (
                      <div key={index} className="grid grid-cols-2 gap-4 text-sm py-2 border-b last:border-b-0">
                        <div>{item.topic}</div>
                        <div>{item.duration}</div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
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