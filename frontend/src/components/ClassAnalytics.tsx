import React, { useState } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Input } from './ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Badge } from './ui/badge';
import { Avatar, AvatarFallback } from './ui/avatar';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogTrigger } from './ui/dialog';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Progress } from './ui/progress';
import { ArrowLeft, Plus, TrendingUp, TrendingDown, Users, Award, Target } from 'lucide-react';
import { User } from '../App';

interface ClassAnalyticsProps {
  user: User;
  onNavigate: (view: string) => void;
  onBack: () => void;
}

interface Student {
  id: number;
  name: string;
  email: string;
  class: string;
  rollNumber: string;
  joinDate: string;
  performance: number;
  status: 'active' | 'inactive';
  attendance: number;
  quizzesTaken: number;
  lessonsCompleted: number;
  lastActive: string;
  improvement: number;
}

export function ClassAnalytics({ user, onNavigate, onBack }: ClassAnalyticsProps) {
  const [selectedClass, setSelectedClass] = useState(user.class || 'Class 6D');
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');

  const [students, setStudents] = useState<Student[]>([
    {
      id: 1, name: 'Alice Johnson', email: 'alice.johnson@school.com', class: 'Class 6D',
      rollNumber: '6D001', joinDate: '2024-01-15', performance: 92, status: 'active',
      attendance: 95, quizzesTaken: 8, lessonsCompleted: 12, lastActive: '2024-01-20', improvement: 5
    },
    {
      id: 2, name: 'Bob Smith', email: 'bob.smith@school.com', class: 'Class 6D',
      rollNumber: '6D002', joinDate: '2024-01-15', performance: 88, status: 'active',
      attendance: 92, quizzesTaken: 10, lessonsCompleted: 15, lastActive: '2024-01-20', improvement: 8
    },
    {
      id: 3, name: 'Charlie Brown', email: 'charlie.brown@school.com', class: 'Class 6D',
      rollNumber: '6D003', joinDate: '2024-01-15', performance: 76, status: 'inactive',
      attendance: 78, quizzesTaken: 6, lessonsCompleted: 10, lastActive: '2024-01-18', improvement: -2
    },
    {
      id: 4, name: 'Diana Prince', email: 'diana.prince@school.com', class: 'Class 6D',
      rollNumber: '6D004', joinDate: '2024-01-15', performance: 94, status: 'active',
      attendance: 98, quizzesTaken: 11, lessonsCompleted: 18, lastActive: '2024-01-20', improvement: 12
    }
  ]);

  const availableStudents = [
    { id: 101, name: 'Frank Miller', email: 'frank.miller@school.com', class: 'Unassigned' },
    { id: 102, name: 'Grace Kelly', email: 'grace.kelly@school.com', class: 'Unassigned' },
  ];

  const classes = ['Class 6D', 'Class 7A', 'Class 8B'];

  const quizAnalytics = [
    { id: 1, title: 'Photosynthesis Quiz', attempts: 24, avgScore: 78, difficulty: 'Medium', date: '2024-01-15' },
    { id: 2, title: 'Fractions Quiz', attempts: 22, avgScore: 85, difficulty: 'Easy', date: '2024-01-10' },
    { id: 3, title: 'Light & Shadow', attempts: 18, avgScore: 72, difficulty: 'Hard', date: '2024-01-08' },
  ];

  const topicAnalytics = [
    { topic: 'Photosynthesis', avgScore: 78, studentsStruggling: 6, mastery: 'Good' },
    { topic: 'Fractions', avgScore: 85, studentsStruggling: 3, mastery: 'Excellent' },
    { topic: 'Light', avgScore: 72, studentsStruggling: 8, mastery: 'Needs Work' },
  ];

  const filteredStudents = students.filter(student => {
    const matchesSearch = student.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         student.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         student.rollNumber.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'all' || student.status === statusFilter;
    const matchesClass = student.class === selectedClass;
    
    return matchesSearch && matchesStatus && matchesClass;
  });

  const addStudentToClass = (studentId: number) => {
    const availableStudent = availableStudents.find(s => s.id === studentId);
    if (availableStudent) {
      const newStudent: Student = {
        id: availableStudent.id, name: availableStudent.name, email: availableStudent.email,
        class: selectedClass, rollNumber: `${selectedClass.slice(-2)}${String(availableStudent.id).padStart(3, '0')}`,
        joinDate: new Date().toISOString().split('T')[0], performance: 0, status: 'active',
        attendance: 0, quizzesTaken: 0, lessonsCompleted: 0, 
        lastActive: new Date().toISOString().split('T')[0], improvement: 0
      };
      setStudents(prev => [...prev, newStudent]);
    }
  };

  const addClass = () => {
    alert('Add new class functionality - would open class creation form');
  };

  const getMasteryColor = (mastery: string) => {
    switch (mastery) {
      case 'Excellent': return 'bg-green-500';
      case 'Good': return 'bg-blue-500';
      case 'Needs Work': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  return (
    <div className="min-h-screen bg-background p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-4">
            <Button variant="outline" onClick={onBack}>
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Dashboard
            </Button>
            <div>
              <h1 className="text-xl">Class Analytics</h1>
              <p className="text-sm text-muted-foreground">Student management and performance analytics</p>
            </div>
          </div>
          
          <div className="flex gap-2">
            <Select value={selectedClass} onValueChange={setSelectedClass}>
              <SelectTrigger className="w-40">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {classes.map((cls) => (
                  <SelectItem key={cls} value={cls}>{cls}</SelectItem>
                ))}
              </SelectContent>
            </Select>
            
            <Dialog>
              <DialogTrigger asChild>
                <Button variant="outline">
                  <Plus className="w-4 h-4 mr-2" />
                  Add Student
                </Button>
              </DialogTrigger>
              <DialogContent className="max-w-md">
                <DialogHeader>
                  <DialogTitle>Add Student to {selectedClass}</DialogTitle>
                  <DialogDescription>
                    Select students from the available list to add them to your class.
                  </DialogDescription>
                </DialogHeader>
                <div className="space-y-4">
                  {availableStudents.map((student) => (
                    <div key={student.id} className="flex items-center justify-between p-3 border rounded">
                      <div>
                        <div className="font-medium">{student.name}</div>
                        <div className="text-sm text-muted-foreground">{student.email}</div>
                      </div>
                      <Button 
                        size="sm" 
                        onClick={() => addStudentToClass(student.id)}
                        disabled={students.some(s => s.id === student.id)}
                      >
                        Add
                      </Button>
                    </div>
                  ))}
                </div>
              </DialogContent>
            </Dialog>

            <Button onClick={addClass}>
              <Plus className="w-4 h-4 mr-2" />
              Add Class
            </Button>
          </div>
        </div>

        {/* Filters and Search */}
        <div className="flex gap-4 mb-6">
          <div className="flex-1">
            <Input
              placeholder="Search students by name, email, or roll number..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="max-w-md"
            />
          </div>
          <Select value={statusFilter} onValueChange={setStatusFilter}>
            <SelectTrigger className="w-40">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Students</SelectItem>
              <SelectItem value="active">Active Only</SelectItem>
              <SelectItem value="inactive">Inactive Only</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {/* Main Analytics Tabs */}
        <Tabs defaultValue="students" className="w-full">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="students">Student Performance</TabsTrigger>
            <TabsTrigger value="quizzes">Quiz Analytics</TabsTrigger>
            <TabsTrigger value="topics">Topic Mastery</TabsTrigger>
          </TabsList>
          
          <TabsContent value="students" className="mt-6">
            <Card>
              <CardHeader>
                <CardTitle>Students in {selectedClass} ({filteredStudents.length})</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {filteredStudents.map((student) => (
                    <div key={student.id} className="flex items-center justify-between p-4 border rounded hover:bg-accent/50">
                      <div className="flex items-center gap-4">
                        <Avatar>
                          <AvatarFallback>{student.name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                        </Avatar>
                        <div>
                          <div className="font-medium">{student.name}</div>
                          <div className="text-sm text-muted-foreground">{student.email}</div>
                          <div className="text-xs text-muted-foreground">Roll: {student.rollNumber}</div>
                        </div>
                      </div>
                      
                      <div className="flex items-center gap-6">
                        <div className="text-center">
                          <div className="text-lg font-bold">{student.performance}%</div>
                          <div className="text-xs text-muted-foreground">Performance</div>
                        </div>
                        
                        <div className="text-center">
                          <div className="text-sm">{student.quizzesTaken}/{student.lessonsCompleted}</div>
                          <div className="text-xs text-muted-foreground">Quiz/Lessons</div>
                        </div>
                        
                        <div className="flex items-center gap-2">
                          {student.improvement >= 0 ? (
                            <TrendingUp className="w-4 h-4 text-green-500" />
                          ) : (
                            <TrendingDown className="w-4 h-4 text-red-500" />
                          )}
                          <span className={`text-sm ${student.improvement >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                            {student.improvement >= 0 ? '+' : ''}{student.improvement}%
                          </span>
                        </div>
                        
                        <Badge variant={student.status === 'active' ? 'default' : 'secondary'}>
                          {student.status}
                        </Badge>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
          
          <TabsContent value="quizzes" className="mt-6">
            <Card>
              <CardHeader>
                <CardTitle>Quiz Performance Analytics</CardTitle>
                <p className="text-sm text-muted-foreground">Detailed breakdown of quiz performance and engagement</p>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {quizAnalytics.map((quiz) => (
                    <div key={quiz.id} className="flex items-center justify-between p-4 border rounded">
                      <div>
                        <div className="font-medium">{quiz.title}</div>
                        <div className="text-sm text-muted-foreground">
                          Created on {new Date(quiz.date).toLocaleDateString()}
                        </div>
                      </div>
                      <div className="flex items-center gap-6">
                        <div className="text-center">
                          <div className="text-lg font-medium">{quiz.attempts}</div>
                          <div className="text-xs text-muted-foreground">Attempts</div>
                        </div>
                        <div className="text-center">
                          <div className="text-lg font-medium">{quiz.avgScore}%</div>
                          <div className="text-xs text-muted-foreground">Average Score</div>
                        </div>
                        <Badge variant={quiz.difficulty === 'Easy' ? 'secondary' : quiz.difficulty === 'Medium' ? 'default' : 'destructive'}>
                          {quiz.difficulty}
                        </Badge>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
          
          <TabsContent value="topics" className="mt-6">
            <Card>
              <CardHeader>
                <CardTitle>Topic Mastery Analysis</CardTitle>
                <p className="text-sm text-muted-foreground">Understanding which topics students find challenging</p>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {topicAnalytics.map((topic, index) => (
                    <div key={index} className="p-4 border rounded">
                      <div className="flex items-center justify-between mb-3">
                        <div className="font-medium">{topic.topic}</div>
                        <Badge variant={topic.mastery === 'Excellent' ? 'default' : topic.mastery === 'Good' ? 'secondary' : 'destructive'}>
                          {topic.mastery}
                        </Badge>
                      </div>
                      <div className="grid grid-cols-3 gap-4 text-sm">
                        <div>
                          <div className="text-muted-foreground">Average Score</div>
                          <div className="text-lg font-medium">{topic.avgScore}%</div>
                        </div>
                        <div>
                          <div className="text-muted-foreground">Students Struggling</div>
                          <div className="text-lg font-medium">{topic.studentsStruggling}</div>
                        </div>
                        <div>
                          <div className="text-muted-foreground">Mastery Level</div>
                          <div className="flex items-center gap-2">
                            <div className={`w-3 h-3 rounded-full ${getMasteryColor(topic.mastery)}`}></div>
                            <span>{topic.mastery}</span>
                          </div>
                        </div>
                      </div>
                      <div className="mt-3">
                        <Progress value={topic.avgScore} className="h-2" />
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}