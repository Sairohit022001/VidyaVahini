import React, { useState } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Progress } from './ui/progress';
import { Badge } from './ui/badge';
import { Switch } from './ui/switch';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Sheet, SheetContent, SheetTrigger } from './ui/sheet';
import { Menu, ArrowLeft, Trophy, Image, BookOpen, Volume2, FileText, Play } from 'lucide-react';
import { User } from '../App';

interface StudentDashboardProps {
  user: User;
  onNavigate: (view: string) => void;
  onLogout: () => void;
  isDark: boolean;
  setIsDark: (dark: boolean) => void;
}

export function StudentDashboard({ user, onNavigate, onLogout, isDark, setIsDark }: StudentDashboardProps) {
  const [isOnline, setIsOnline] = useState(true);
  const [selectedClass, setSelectedClass] = useState(user.class || 'Class 8');
  const [selectedSubject, setSelectedSubject] = useState(user.subject || 'Science');
  const [selectedLevel, setSelectedLevel] = useState('Beginner');
  const [selectedLanguage, setSelectedLanguage] = useState('English');
  const [selectedTopic, setSelectedTopic] = useState<string | null>(null);

  const classes = ['Class 1', 'Class 2', 'Class 3', 'Class 4', 'Class 5', 'Class 6', 'Class 7', 'Class 8', 'Class 9', 'Class 10'];
  const subjects = ['English', 'Hindi', 'Mathematics', 'Science', 'Social Science', 'EVS'];
  const levels = ['Beginner', 'Intermediate', 'Advanced'];
  const languages = ['English', 'Hindi', 'Tamil', 'Telugu', 'Bengali', 'Marathi'];

  const topicsBySubject = {
    'Science': ['Photosynthesis', 'Respiration', 'Light & Shadow', 'Sound', 'Magnetism'],
    'Mathematics': ['Fractions', 'Decimals', 'Geometry', 'Algebra', 'Mensuration'],
    'English': ['Grammar', 'Comprehension', 'Story Writing', 'Poetry', 'Vocabulary'],
    'Hindi': ['व्याकरण', 'कविता', 'गद्य', 'निबंध', 'वर्तनी'],
    'Social Science': ['History', 'Geography', 'Civics', 'Economics', 'Culture'],
    'EVS': ['Plants', 'Animals', 'Environment', 'Water', 'Air']
  };

  const topics = topicsBySubject[selectedSubject as keyof typeof topicsBySubject] || [];

  const menuItems = [
    { label: 'My Lessons', action: () => setSelectedTopic(null) },
    { label: 'My Rewards', action: () => {} },
    { label: 'Settings', action: () => {} },
    { label: 'Help', action: () => {} },
    { label: 'Logout', action: onLogout },
  ];

  const handleTopicSelect = (topic: string) => {
    setSelectedTopic(topic);
  };

  const handleLessonActivity = (activity: string) => {
    console.log(`Opening ${activity} for topic: ${selectedTopic}`);
    if (activity === 'quiz') {
      onNavigate('quiz');
    } else {
      onNavigate('lesson');
    }
  };

  if (selectedTopic) {
    return (
      <div className="min-h-screen bg-background p-4">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-4">
            <Button variant="outline" size="sm" onClick={() => setSelectedTopic(null)}>
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Topics
            </Button>
            <div>
              <h1 className="text-2xl tracking-tight">VIDYAVĀHINĪ</h1>
              <p className="text-sm text-muted-foreground">CLASS 1 TO 10</p>
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

        {/* Topic Content */}
        <div className="max-w-4xl mx-auto">
          <Card>
            <CardHeader>
              <CardTitle className="text-center">{selectedTopic}</CardTitle>
              <div className="text-center space-y-2">
                <Badge variant="secondary">{selectedSubject}</Badge>
                <Badge variant="outline">{selectedClass}</Badge>
                <Progress value={75} className="h-2 mt-4" />
                <p className="text-sm text-muted-foreground">75% Complete</p>
              </div>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                <Button 
                  variant="outline" 
                  className="h-20 flex flex-col items-center justify-center gap-2"
                  onClick={() => handleLessonActivity('diagram')}
                >
                  <Image className="w-6 h-6" />
                  <span className="text-sm">View Diagram</span>
                </Button>
                <Button 
                  variant="outline" 
                  className="h-20 flex flex-col items-center justify-center gap-2"
                  onClick={() => handleLessonActivity('lesson')}
                >
                  <BookOpen className="w-6 h-6" />
                  <span className="text-sm">View Lesson</span>
                </Button>
                <Button 
                  variant="outline" 
                  className="h-20 flex flex-col items-center justify-center gap-2"
                  onClick={() => handleLessonActivity('story')}
                >
                  <BookOpen className="w-6 h-6" />
                  <span className="text-sm">Read Story</span>
                </Button>
                <Button 
                  variant="outline" 
                  className="h-20 flex flex-col items-center justify-center gap-2"
                  onClick={() => handleLessonActivity('audio')}
                >
                  <Volume2 className="w-6 h-6" />
                  <span className="text-sm">Read Aloud</span>
                </Button>
                <Button 
                  variant="outline" 
                  className="h-20 flex flex-col items-center justify-center gap-2"
                  onClick={() => handleLessonActivity('summary')}
                >
                  <FileText className="w-6 h-6" />
                  <span className="text-sm">View Summary</span>
                </Button>
                <Button 
                  variant="outline" 
                  className="h-20 flex flex-col items-center justify-center gap-2"
                  onClick={() => handleLessonActivity('research')}
                >
                  <FileText className="w-6 h-6" />
                  <span className="text-sm">View Research Paper</span>
                </Button>
                <Button 
                  variant="outline" 
                  className="h-20 flex flex-col items-center justify-center gap-2"
                  onClick={() => handleLessonActivity('story2')}
                >
                  <BookOpen className="w-6 h-6" />
                  <span className="text-sm">View Story</span>
                </Button>
                <Button 
                  className="h-20 flex flex-col items-center justify-center gap-2"
                  onClick={() => handleLessonActivity('quiz')}
                >
                  <Play className="w-6 h-6" />
                  <span className="text-sm">Take Quiz</span>
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* No AI Assistant Button for students */}
      </div>
    );
  }

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
            <p className="text-sm text-muted-foreground">CLASS 1 TO 10</p>
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

      {/* Back Button */}
      <div className="mb-4">
        <Button variant="outline" size="sm" onClick={() => window.history.back()}>
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back
        </Button>
      </div>

      {/* Welcome Section with Enhanced Dropdowns */}
      <div className="mb-6">
        <h2 className="text-xl mb-2">WELCOME BACK STUDENT</h2>
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

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Content - My Lessons */}
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>MY LESSONS</CardTitle>
              <p className="text-sm text-muted-foreground">Choose a topic to start learning</p>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {topics.map((topic, index) => (
                  <Button
                    key={topic}
                    variant="outline"
                    className="h-24 flex flex-col items-center justify-center gap-2 text-left"
                    onClick={() => handleTopicSelect(topic)}
                  >
                    <div className="text-sm font-medium">{topic}</div>
                    <div className="flex items-center gap-2 text-xs text-muted-foreground">
                      <div className="w-16 bg-secondary rounded-full h-1">
                        <div 
                          className="bg-primary h-1 rounded-full" 
                          style={{width: `${Math.random() * 100}%`}}
                        ></div>
                      </div>
                      <span>{Math.floor(Math.random() * 100)}%</span>
                    </div>
                  </Button>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Rewards Section */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>REWARDS</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="text-center space-y-2">
                <div className="text-4xl">🏆</div>
                <p className="text-sm">Quiz Master</p>
                <Badge variant="secondary">Earned</Badge>
              </div>
              
              <div className="space-y-3">
                <p className="text-sm">MY BADGES</p>
                <div className="grid grid-cols-1 gap-2">
                  <div className="text-center p-3 border rounded">
                    <div className="text-2xl mb-2">🏆</div>
                    <div className="text-xs">Quiz Master</div>
                    <Badge variant="secondary" className="text-xs mt-1">Earned</Badge>
                  </div>
                  <div className="text-center p-3 border rounded opacity-50">
                    <div className="text-2xl mb-2">⭐</div>
                    <div className="text-xs">Lesson Completer</div>
                    <Badge variant="outline" className="text-xs mt-1">Locked</Badge>
                  </div>
                </div>
              </div>

              <div className="text-center space-y-2">
                <p className="text-sm text-muted-foreground">CLASS RANK</p>
                <p className="text-xs text-muted-foreground">Out of 35 students</p>
                <div className="text-3xl">#3</div>
                <p className="text-sm">400 points</p>
              </div>
            </CardContent>
          </Card>

          <div className="text-center">
            <p className="text-sm text-muted-foreground mb-2">Welcome, {user.name}! 🎉</p>
            <p className="text-xs text-muted-foreground">Keep learning and growing!</p>
          </div>
        </div>
      </div>

      {/* No AI Assistant Button for Class 1-10 students */}
    </div>
  );
}