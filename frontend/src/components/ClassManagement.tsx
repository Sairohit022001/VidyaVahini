import React, { useState } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Input } from './ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Badge } from './ui/badge';
import { Avatar, AvatarFallback } from './ui/avatar';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogTrigger } from './ui/dialog';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { ArrowLeft, Plus, Search, MoreVertical, Mail, Phone, Calendar, BookOpen, TrendingUp } from 'lucide-react';
import { User } from '../App';

interface ClassManagementProps {
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
}

export function ClassManagement({ user, onNavigate, onBack }: ClassManagementProps) {
  const [selectedClass, setSelectedClass] = useState(user.class || 'Class 6D');
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');

  const [students, setStudents] = useState<Student[]>([
    {
      id: 1,
      name: 'Alice Johnson',
      email: 'alice.johnson@school.com',
      class: 'Class 6D',
      rollNumber: '6D001',
      joinDate: '2024-01-15',
      performance: 92,
      status: 'active',
      attendance: 95,
      quizzesTaken: 8,
      lessonsCompleted: 12,
      lastActive: '2024-01-20'
    },
    {
      id: 2,
      name: 'Bob Smith',
      email: 'bob.smith@school.com',
      class: 'Class 6D',
      rollNumber: '6D002',
      joinDate: '2024-01-15',
      performance: 88,
      status: 'active',
      attendance: 92,
      quizzesTaken: 10,
      lessonsCompleted: 15,
      lastActive: '2024-01-20'
    },
    {
      id: 3,
      name: 'Charlie Brown',
      email: 'charlie.brown@school.com',
      class: 'Class 6D',
      rollNumber: '6D003',
      joinDate: '2024-01-15',
      performance: 76,
      status: 'inactive',
      attendance: 78,
      quizzesTaken: 6,
      lessonsCompleted: 10,
      lastActive: '2024-01-18'
    },
    {
      id: 4,
      name: 'Diana Prince',
      email: 'diana.prince@school.com',
      class: 'Class 6D',
      rollNumber: '6D004',
      joinDate: '2024-01-15',
      performance: 94,
      status: 'active',
      attendance: 98,
      quizzesTaken: 11,
      lessonsCompleted: 18,
      lastActive: '2024-01-20'
    },
    {
      id: 5,
      name: 'Edward Norton',
      email: 'edward.norton@school.com',
      class: 'Class 6D',
      rollNumber: '6D005',
      joinDate: '2024-01-15',
      performance: 82,
      status: 'active',
      attendance: 89,
      quizzesTaken: 9,
      lessonsCompleted: 14,
      lastActive: '2024-01-19'
    }
  ]);

  const availableStudents = [
    { id: 101, name: 'Frank Miller', email: 'frank.miller@school.com', class: 'Unassigned' },
    { id: 102, name: 'Grace Kelly', email: 'grace.kelly@school.com', class: 'Unassigned' },
    { id: 103, name: 'Henry Ford', email: 'henry.ford@school.com', class: 'Unassigned' },
  ];

  const classes = ['Class 6D', 'Class 7A', 'Class 8B'];

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
        id: availableStudent.id,
        name: availableStudent.name,
        email: availableStudent.email,
        class: selectedClass,
        rollNumber: `${selectedClass.slice(-2)}${String(availableStudent.id).padStart(3, '0')}`,
        joinDate: new Date().toISOString().split('T')[0],
        performance: 0,
        status: 'active',
        attendance: 0,
        quizzesTaken: 0,
        lessonsCompleted: 0,
        lastActive: new Date().toISOString().split('T')[0]
      };
      setStudents(prev => [...prev, newStudent]);
    }
  };

  const removeStudentFromClass = (studentId: number) => {
    setStudents(prev => prev.filter(s => s.id !== studentId));
  };

  const toggleStudentStatus = (studentId: number) => {
    setStudents(prev => prev.map(student => 
      student.id === studentId 
        ? { ...student, status: student.status === 'active' ? 'inactive' : 'active' }
        : student
    ));
  };

  const getPerformanceColor = (performance: number) => {
    if (performance >= 90) return 'text-green-600';
    if (performance >= 80) return 'text-blue-600';
    if (performance >= 70) return 'text-yellow-600';
    return 'text-red-600';
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
              <h1 className="text-xl">Class Management</h1>
              <p className="text-sm text-muted-foreground">Manage students and class assignments</p>
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
                <Button>
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
                  <p className="text-sm text-muted-foreground">Select students to add to your class:</p>
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

        {/* Class Overview */}
        <div className="grid grid-cols-4 gap-4 mb-6">
          <Card>
            <CardContent className="p-4 text-center">
              <div className="text-2xl font-bold">{students.filter(s => s.class === selectedClass).length}</div>
              <div className="text-sm text-muted-foreground">Total Students</div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4 text-center">
              <div className="text-2xl font-bold text-green-600">
                {students.filter(s => s.class === selectedClass && s.status === 'active').length}
              </div>
              <div className="text-sm text-muted-foreground">Active Students</div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4 text-center">
              <div className="text-2xl font-bold text-blue-600">
                {Math.round(students
                  .filter(s => s.class === selectedClass)
                  .reduce((acc, s) => acc + s.performance, 0) / 
                  students.filter(s => s.class === selectedClass).length) || 0}%
              </div>
              <div className="text-sm text-muted-foreground">Average Performance</div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4 text-center">
              <div className="text-2xl font-bold text-purple-600">
                {Math.round(students
                  .filter(s => s.class === selectedClass)
                  .reduce((acc, s) => acc + s.attendance, 0) / 
                  students.filter(s => s.class === selectedClass).length) || 0}%
              </div>
              <div className="text-sm text-muted-foreground">Average Attendance</div>
            </CardContent>
          </Card>
        </div>

        {/* Student List */}
        <Tabs defaultValue="list" className="w-full">
          <TabsList>
            <TabsTrigger value="list">Student List</TabsTrigger>
            <TabsTrigger value="performance">Performance View</TabsTrigger>
          </TabsList>
          
          <TabsContent value="list" className="mt-6">
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
                          <div className="text-xs text-muted-foreground">Roll: {student.rollNumber} • Joined: {new Date(student.joinDate).toLocaleDateString()}</div>
                        </div>
                      </div>
                      
                      <div className="flex items-center gap-6">
                        <div className="text-center">
                          <div className={`text-lg font-bold ${getPerformanceColor(student.performance)}`}>
                            {student.performance}%
                          </div>
                          <div className="text-xs text-muted-foreground">Performance</div>
                        </div>
                        
                        <div className="text-center">
                          <div className="text-sm">{student.attendance}%</div>
                          <div className="text-xs text-muted-foreground">Attendance</div>
                        </div>
                        
                        <div className="text-center">
                          <div className="text-sm">{student.quizzesTaken}/{student.lessonsCompleted}</div>
                          <div className="text-xs text-muted-foreground">Quiz/Lessons</div>
                        </div>
                        
                        <Badge variant={student.status === 'active' ? 'default' : 'secondary'}>
                          {student.status}
                        </Badge>
                        
                        <div className="flex gap-2">
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => toggleStudentStatus(student.id)}
                          >
                            {student.status === 'active' ? 'Deactivate' : 'Activate'}
                          </Button>
                          <Button
                            variant="destructive"
                            size="sm"
                            onClick={() => removeStudentFromClass(student.id)}
                          >
                            Remove
                          </Button>
                        </div>
                      </div>
                    </div>
                  ))}
                  
                  {filteredStudents.length === 0 && (
                    <div className="text-center py-8 text-muted-foreground">
                      No students found matching your criteria.
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
          
          <TabsContent value="performance" className="mt-6">
            <Card>
              <CardHeader>
                <CardTitle>Performance Overview</CardTitle>
                <p className="text-sm text-muted-foreground">Detailed performance metrics for all students</p>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {filteredStudents.map((student) => (
                    <Card key={student.id}>
                      <CardContent className="p-4">
                        <div className="flex items-center gap-3 mb-4">
                          <Avatar>
                            <AvatarFallback>{student.name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                          </Avatar>
                          <div>
                            <div className="font-medium">{student.name}</div>
                            <div className="text-sm text-muted-foreground">{student.rollNumber}</div>
                          </div>
                        </div>
                        
                        <div className="space-y-3">
                          <div className="flex items-center justify-between">
                            <span className="text-sm">Performance</span>
                            <span className={`font-bold ${getPerformanceColor(student.performance)}`}>
                              {student.performance}%
                            </span>
                          </div>
                          
                          <div className="flex items-center justify-between">
                            <span className="text-sm">Attendance</span>
                            <span className="font-medium">{student.attendance}%</span>
                          </div>
                          
                          <div className="flex items-center justify-between">
                            <span className="text-sm">Quizzes Taken</span>
                            <span className="font-medium">{student.quizzesTaken}</span>
                          </div>
                          
                          <div className="flex items-center justify-between">
                            <span className="text-sm">Lessons Completed</span>
                            <span className="font-medium">{student.lessonsCompleted}</span>
                          </div>
                          
                          <div className="flex items-center justify-between">
                            <span className="text-sm">Last Active</span>
                            <span className="text-sm text-muted-foreground">
                              {new Date(student.lastActive).toLocaleDateString()}
                            </span>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
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