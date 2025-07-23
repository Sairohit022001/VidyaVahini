import React, { useState } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Badge } from './ui/badge';
import { Progress } from './ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { ArrowLeft, TrendingUp, TrendingDown, Users, Award, Clock, Target } from 'lucide-react';
import { User } from '../App';

interface AnalyticsProps {
  user: User;
  onNavigate: (view: string) => void;
  onBack: () => void;
}

export function Analytics({ user, onNavigate, onBack }: AnalyticsProps) {
  const [selectedClass, setSelectedClass] = useState(user.class || 'Class 6D');
  const [selectedSubject, setSelectedSubject] = useState(user.subject || 'Mathematics');
  const [timeFrame, setTimeFrame] = useState('last30days');

  const classes = ['Class 6D', 'Class 7A', 'Class 8B'];
  const subjects = ['Mathematics', 'Science', 'English', 'Hindi', 'Social Science'];

  const analyticsData = {
    overview: {
      totalStudents: 24,
      activeStudents: 18,
      averageScore: 85,
      completionRate: 78,
      totalQuizzes: 12,
      totalLessons: 45
    },
    studentPerformance: [
      { id: 1, name: 'Alice Johnson', avgScore: 92, quizzesTaken: 8, lessonsCompleted: 12, improvement: 5 },
      { id: 2, name: 'Bob Smith', avgScore: 88, quizzesTaken: 10, lessonsCompleted: 15, improvement: 8 },
      { id: 3, name: 'Charlie Brown', avgScore: 76, quizzesTaken: 6, lessonsCompleted: 10, improvement: -2 },
      { id: 4, name: 'Diana Prince', avgScore: 94, quizzesTaken: 11, lessonsCompleted: 18, improvement: 12 },
      { id: 5, name: 'Edward Norton', avgScore: 82, quizzesTaken: 9, lessonsCompleted: 14, improvement: 6 },
    ],
    quizAnalytics: [
      { id: 1, title: 'Photosynthesis Quiz', attempts: 24, avgScore: 78, difficulty: 'Medium', date: '2024-01-15' },
      { id: 2, title: 'Fractions Quiz', attempts: 22, avgScore: 85, difficulty: 'Easy', date: '2024-01-10' },
      { id: 3, title: 'Light & Shadow', attempts: 18, avgScore: 72, difficulty: 'Hard', date: '2024-01-08' },
      { id: 4, title: 'Grammar Basics', attempts: 20, avgScore: 88, difficulty: 'Medium', date: '2024-01-05' },
    ],
    topicAnalytics: [
      { topic: 'Photosynthesis', avgScore: 78, studentsStruggling: 6, mastery: 'Good' },
      { topic: 'Fractions', avgScore: 85, studentsStruggling: 3, mastery: 'Excellent' },
      { topic: 'Grammar', avgScore: 88, studentsStruggling: 2, mastery: 'Excellent' },
      { topic: 'Light', avgScore: 72, studentsStruggling: 8, mastery: 'Needs Work' },
    ]
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
              <p className="text-sm text-muted-foreground">Performance insights and data</p>
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
            <Select value={selectedSubject} onValueChange={setSelectedSubject}>
              <SelectTrigger className="w-40">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {subjects.map((subject) => (
                  <SelectItem key={subject} value={subject}>{subject}</SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Select value={timeFrame} onValueChange={setTimeFrame}>
              <SelectTrigger className="w-40">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="last7days">Last 7 days</SelectItem>
                <SelectItem value="last30days">Last 30 days</SelectItem>
                <SelectItem value="last90days">Last 3 months</SelectItem>
                <SelectItem value="all">All time</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>

        {/* Overview Cards */}
        <div className="grid grid-cols-2 md:grid-cols-6 gap-4 mb-6">
          <Card>
            <CardContent className="p-4 text-center">
              <Users className="w-8 h-8 mx-auto mb-2 text-primary" />
              <div className="text-2xl font-bold">{analyticsData.overview.totalStudents}</div>
              <div className="text-xs text-muted-foreground">Total Students</div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4 text-center">
              <div className="w-8 h-8 mx-auto mb-2 bg-green-500 rounded-full flex items-center justify-center">
                <Users className="w-4 h-4 text-white" />
              </div>
              <div className="text-2xl font-bold">{analyticsData.overview.activeStudents}</div>
              <div className="text-xs text-muted-foreground">Active Students</div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4 text-center">
              <Award className="w-8 h-8 mx-auto mb-2 text-primary" />
              <div className="text-2xl font-bold">{analyticsData.overview.averageScore}%</div>
              <div className="text-xs text-muted-foreground">Average Score</div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4 text-center">
              <Target className="w-8 h-8 mx-auto mb-2 text-primary" />
              <div className="text-2xl font-bold">{analyticsData.overview.completionRate}%</div>
              <div className="text-xs text-muted-foreground">Completion Rate</div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4 text-center">
              <div className="w-8 h-8 mx-auto mb-2 bg-blue-500 rounded-full flex items-center justify-center text-white">
                Q
              </div>
              <div className="text-2xl font-bold">{analyticsData.overview.totalQuizzes}</div>
              <div className="text-xs text-muted-foreground">Quizzes Created</div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4 text-center">
              <div className="w-8 h-8 mx-auto mb-2 bg-purple-500 rounded-full flex items-center justify-center text-white">
                L
              </div>
              <div className="text-2xl font-bold">{analyticsData.overview.totalLessons}</div>
              <div className="text-xs text-muted-foreground">Lessons Created</div>
            </CardContent>
          </Card>
        </div>

        {/* Detailed Analytics */}
        <Tabs defaultValue="students" className="w-full">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="students">Student Performance</TabsTrigger>
            <TabsTrigger value="quizzes">Quiz Analytics</TabsTrigger>
            <TabsTrigger value="topics">Topic Mastery</TabsTrigger>
            <TabsTrigger value="insights">AI Insights</TabsTrigger>
          </TabsList>
          
          <TabsContent value="students" className="mt-6">
            <Card>
              <CardHeader>
                <CardTitle>Student Performance Overview</CardTitle>
                <p className="text-sm text-muted-foreground">Individual student progress and performance metrics</p>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {analyticsData.studentPerformance.map((student) => (
                    <div key={student.id} className="flex items-center justify-between p-4 border rounded">
                      <div className="flex items-center gap-4">
                        <div className="w-10 h-10 bg-primary rounded-full flex items-center justify-center text-primary-foreground font-medium">
                          {student.name.charAt(0)}
                        </div>
                        <div>
                          <div className="font-medium">{student.name}</div>
                          <div className="text-sm text-muted-foreground">
                            {student.quizzesTaken} quizzes • {student.lessonsCompleted} lessons completed
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center gap-4">
                        <div className="text-right">
                          <div className="text-lg font-medium">{student.avgScore}%</div>
                          <div className="text-xs text-muted-foreground">Average Score</div>
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
                  {analyticsData.quizAnalytics.map((quiz) => (
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
                  {analyticsData.topicAnalytics.map((topic, index) => (
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
          
          <TabsContent value="insights" className="mt-6">
            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>AI-Generated Insights</CardTitle>
                  <p className="text-sm text-muted-foreground">Intelligent recommendations based on your class performance</p>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="p-4 bg-blue-50 dark:bg-blue-950 rounded border border-blue-200 dark:border-blue-800">
                    <div className="font-medium text-blue-800 dark:text-blue-200">🎯 Recommendation</div>
                    <p className="text-sm text-blue-700 dark:text-blue-300 mt-1">
                      Consider creating additional practice materials for "Light & Shadow" topic. 8 students are struggling with an average score of 72%.
                    </p>
                  </div>
                  
                  <div className="p-4 bg-green-50 dark:bg-green-950 rounded border border-green-200 dark:border-green-800">
                    <div className="font-medium text-green-800 dark:text-green-200">✅ Strength</div>
                    <p className="text-sm text-green-700 dark:text-green-300 mt-1">
                      Excellent performance in Fractions! Students show 85% average with only 3 students needing additional support.
                    </p>
                  </div>
                  
                  <div className="p-4 bg-amber-50 dark:bg-amber-950 rounded border border-amber-200 dark:border-amber-800">
                    <div className="font-medium text-amber-800 dark:text-amber-200">⚠️ Action Needed</div>
                    <p className="text-sm text-amber-700 dark:text-amber-300 mt-1">
                      Charlie Brown shows declining performance (-2% improvement). Consider one-on-one session or additional support.
                    </p>
                  </div>

                  <div className="p-4 bg-purple-50 dark:bg-purple-950 rounded border border-purple-200 dark:border-purple-800">
                    <div className="font-medium text-purple-800 dark:text-purple-200">🚀 Opportunity</div>
                    <p className="text-sm text-purple-700 dark:text-purple-300 mt-1">
                      Diana Prince shows exceptional improvement (+12%). Consider advanced materials or peer tutoring opportunities.
                    </p>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}