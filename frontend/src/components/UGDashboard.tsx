import React, { useState } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Progress } from './ui/progress';
import { Badge } from './ui/badge';
import { Switch } from './ui/switch';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Sheet, SheetContent, SheetTrigger } from './ui/sheet';
import { Input } from './ui/input';
import { Upload, Download, MessageCircle, BookOpen, FileText, Image, Volume2, Menu, ArrowLeft, Plus, Layers, Wand2 } from 'lucide-react';
import { User } from '../App';
import { AIChatBot } from './AIChatBot';

interface UGDashboardProps {
  user: User;
  onNavigate: (view: string) => void;
  onLogout: () => void;
  isDark: boolean;
  setIsDark: (dark: boolean) => void;
}

export function UGDashboard({ user, onNavigate, onLogout, isDark, setIsDark }: UGDashboardProps) {
  const [isOnline, setIsOnline] = useState(true);
  const [selectedDepartment, setSelectedDepartment] = useState('Computer Science');
  const [selectedLevel, setSelectedLevel] = useState('Intermediate');
  const [selectedLanguage, setSelectedLanguage] = useState('English');
  const [topicInput, setTopicInput] = useState('');
  const [currentTopic, setCurrentTopic] = useState('');
  const [showChat, setShowChat] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [selectedContent, setSelectedContent] = useState<string | null>(null);
  const [generatedContent, setGeneratedContent] = useState<{[key: string]: string}>({});

  const departments = ['Computer Science', 'Electrical Engineering', 'Mechanical Engineering', 'Civil Engineering', 'Electronics Engineering', 'Information Technology'];
  const levels = ['Beginner', 'Intermediate', 'Advanced', 'Expert'];
  const languages = ['English', 'Hindi', 'Tamil', 'Telugu', 'Bengali', 'Marathi'];

  const handleGenerateTopic = async () => {
    if (!topicInput.trim()) {
      alert('Please enter a topic');
      return;
    }

    setIsGenerating(true);
    setCurrentTopic(topicInput);
    
    // Simulate topic generation
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    setIsGenerating(false);
    setSelectedContent(null);
    setGeneratedContent({});
  };

  const handleContentGeneration = async (type: string) => {
    setSelectedContent(type);
    
    // Simulate content generation
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    const content = {
      diagram: `[Interactive Diagram for ${currentTopic}]\n\nThis visual representation shows:\n1. Core concepts and relationships\n2. Process flow and dependencies\n3. Real-world applications\n4. Advanced implementation details\n\nStudents can interact with each component to explore deeper.`,
      
      lesson: `Comprehensive Lesson: ${currentTopic}\n\nObjective: Understand the fundamental and advanced concepts of ${currentTopic}\n\nIntroduction:\n${currentTopic} is a crucial concept in ${selectedDepartment} that forms the foundation for advanced learning.\n\nKey Concepts:\n• Definition and importance\n• Core principles\n• Mathematical foundations\n• Practical applications\n\nAdvanced Topics:\n• Industry implementations\n• Current research\n• Future directions\n\nConclusion:\nMastering ${currentTopic} will enhance your understanding of ${selectedDepartment} and prepare you for advanced coursework.`,
      
      story: `The Story of ${currentTopic}\n\nIn the world of ${selectedDepartment}, there was once a complex problem that seemed impossible to solve. Engineers and researchers worked tirelessly until they discovered the principles of ${currentTopic}.\n\nThis breakthrough changed everything. What once took days now took minutes. Complex calculations became simple. The impossible became routine.\n\nToday, ${currentTopic} is everywhere - from the device you're using to read this to the infrastructure that powers our modern world. Understanding it means understanding the very foundations of our technological society.`,
      
      research: `Research Paper: ${currentTopic} in Modern ${selectedDepartment}\n\nAbstract:\nThis paper examines the current state and future prospects of ${currentTopic} in the field of ${selectedDepartment}. Through comprehensive analysis and case studies, we explore its applications, challenges, and potential solutions.\n\nIntroduction:\nThe significance of ${currentTopic} in ${selectedDepartment} cannot be overstated. As technology advances, understanding these concepts becomes crucial for innovation.\n\nLiterature Review:\nRecent studies have shown significant developments in ${currentTopic} applications, particularly in areas such as automation, optimization, and system design.\n\nMethodology:\nOur research approach combines theoretical analysis with practical implementation studies across multiple case scenarios.\n\nResults:\nFindings indicate that ${currentTopic} continues to be a driving force in technological advancement, with applications expanding into new domains.\n\nConclusion:\nThe future of ${currentTopic} in ${selectedDepartment} looks promising, with emerging technologies opening new possibilities for innovation and application.`,
      
      flashcards: `Flashcard Set: ${currentTopic}\n\nCard 1:\nQ: What is ${currentTopic}?\nA: [Definition and key characteristics]\n\nCard 2:\nQ: What are the main applications of ${currentTopic}?\nA: [List of practical applications]\n\nCard 3:\nQ: What are the key principles behind ${currentTopic}?\nA: [Fundamental concepts and theories]\n\nCard 4:\nQ: How is ${currentTopic} implemented in modern systems?\nA: [Implementation details and examples]\n\nCard 5:\nQ: What are the current challenges in ${currentTopic}?\nA: [Current limitations and research areas]\n\nCard 6:\nQ: What skills are needed to master ${currentTopic}?\nA: [Required knowledge and competencies]`
    };
    
    setGeneratedContent(prev => ({
      ...prev,
      [type]: content[type as keyof typeof content]
    }));
  };

  const handleFileUpload = () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.pdf,.doc,.docx,.ppt';
    input.onchange = (e) => {
      const file = (e.target as HTMLInputElement).files?.[0];
      if (file) {
        console.log('Uploaded:', file.name);
      }
    };
    input.click();
  };

  const handleDownloadPDF = () => {
    const link = document.createElement('a');
    link.href = 'data:application/pdf;base64,JVBERi0xLjQKJdPr6eEKMSAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovUGFnZXMgMiAwIFIKPj4KZW5kb2JqCjIgMCBvYmoKPDwKL1R5cGUgL1BhZ2VzCi9LaWRzIFszIDAgUl0KL0NvdW50IDEKPD4KZW5kb2JqCjMgMCBvYmoKPDwKL1R5cGUgL1BhZ2UKL1BhcmVudCAyIDAgUgovTWVkaWFCb3ggWzAgMCA2MTIgNzkyXQovUmVzb3VyY2VzIDw8Ci9Gb250IDw8Ci9GMSA0IDAgUgo+Pgo+PgovQ29udGVudHMgNSAwIFIKPj4KZW5kb2JqCjQgMCBvYmoKPDwKL1R5cGUgL0ZvbnQKL1N1YnR5cGUgL1R5cGUxCi9CYXNlRm9udCAvSGVsdmV0aWNhCj4+CmVuZG9iago1IDAgb2JqCjw8Ci9MZW5ndGggNTIKPj4Kc3RyZWFtCkJUCi9GMSA5IFRmCjEwIDQ4MCBUZEYKQWR2YW5jZWQgVG9waWMgLSBEYXRhIFN0cnVjdHVyZXMKRVQKZW5kc3RyZWFtCmVuZG9iagp4cmVmCjAgNgowMDAwMDAwMDAwIDY1NTM1IGYgCjAwMDAwMDAwMDkgMDAwMDAgbiAKMDAwMDAwMDA1OCAwMDAwMCBuIAowMDAwMDAwMTE1IDAwMDAwIG4gCjAwMDAwMDAyNDUgMDAwMDAgbiAKMDAwMDAwMDMxNCAwMDAwMCBuIAp0cmFpbGVyCjw8Ci9TaXplIDYKL1Jvb3QgMSAwIFIKPj4Kc3RhcnR4cmVmCjQxNgolJUVPRg==';
    link.download = `${currentTopic.toLowerCase().replace(/\s+/g, '-')}-notes.pdf`;
    link.click();
  };

  const menuItems = [
    { label: 'My Lessons', action: () => {} },
    { label: 'Generate Quiz', action: () => onNavigate('quiz') },
    { label: 'My Rewards', action: () => {} },
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
            <p className="text-sm text-muted-foreground">UG CLASS DASHBOARD</p>
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

      {/* Welcome Section with Simplified Dropdowns */}
      <div className="mb-6">
        <h2 className="text-xl mb-2">WELCOME BACK UG STUDENT</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
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
          <Select value={selectedDepartment} onValueChange={setSelectedDepartment}>
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {departments.map((dept) => (
                <SelectItem key={dept} value={dept}>{dept}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {/* Topic Input Section */}
        <div className="flex gap-2 mb-4">
          <Input
            placeholder="Enter your topic (e.g., Machine Learning, Data Structures, etc.)"
            value={topicInput}
            onChange={(e) => setTopicInput(e.target.value)}
            className="flex-1"
          />
          <Button 
            onClick={handleGenerateTopic}
            disabled={isGenerating || !topicInput.trim()}
          >
            <Wand2 className="w-4 h-4 mr-2" />
            {isGenerating ? 'Generating...' : 'Generate'}
          </Button>
        </div>

        <p className="text-sm text-muted-foreground">
          LEVEL: {selectedLevel.toUpperCase()} • LANGUAGE: {selectedLanguage.toUpperCase()} • DEPARTMENT: {selectedDepartment.toUpperCase()}
        </p>
        {currentTopic && (
          <p className="text-sm text-primary mt-1">Current Topic: {currentTopic}</p>
        )}
      </div>

      {currentTopic && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Current Topic */}
            <Card>
              <CardHeader>
                <CardTitle>Topic: {currentTopic}</CardTitle>
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <Badge variant="secondary">{selectedLevel}</Badge>
                    <Badge variant="outline">Learning Mode</Badge>
                  </div>
                  <Progress value={68} className="h-2" />
                  <p className="text-xs text-muted-foreground">Ready to explore this topic</p>
                </div>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                  <Button 
                    variant="outline" 
                    className="h-16 flex flex-col items-center justify-center gap-1"
                    onClick={() => handleContentGeneration('diagram')}
                  >
                    <Image className="w-4 h-4" />
                    <span className="text-xs">View Diagram</span>
                  </Button>
                  <Button 
                    variant="outline" 
                    className="h-16 flex flex-col items-center justify-center gap-1"
                    onClick={() => handleContentGeneration('story')}
                  >
                    <BookOpen className="w-4 h-4" />
                    <span className="text-xs">Read Story</span>
                  </Button>
                  <Button 
                    variant="outline" 
                    className="h-16 flex flex-col items-center justify-center gap-1"
                    onClick={() => handleContentGeneration('lesson')}
                  >
                    <BookOpen className="w-4 h-4" />
                    <span className="text-xs">View Lesson</span>
                  </Button>
                  <Button 
                    variant="outline" 
                    className="h-16 flex flex-col items-center justify-center gap-1"
                    onClick={() => handleContentGeneration('lesson')}
                  >
                    <Plus className="w-4 h-4" />
                    <span className="text-xs">Generate Lesson</span>
                  </Button>
                  <Button 
                    variant="outline" 
                    className="h-16 flex flex-col items-center justify-center gap-1"
                    onClick={() => handleContentGeneration('diagram')}
                  >
                    <Image className="w-4 h-4" />
                    <span className="text-xs">Generate Diagram</span>
                  </Button>
                  <Button 
                    variant="outline" 
                    className="h-16 flex flex-col items-center justify-center gap-1"
                    onClick={() => handleContentGeneration('research')}
                  >
                    <FileText className="w-4 h-4" />
                    <span className="text-xs">Generate Research Paper</span>
                  </Button>
                  <Button 
                    variant="outline" 
                    className="h-16 flex flex-col items-center justify-center gap-1"
                    onClick={() => handleContentGeneration('flashcards')}
                  >
                    <Layers className="w-4 h-4" />
                    <span className="text-xs">Generate Flashcards</span>
                  </Button>
                  <Button 
                    variant="outline" 
                    className="h-16 flex flex-col items-center justify-center gap-1"
                    onClick={handleDownloadPDF}
                  >
                    <Download className="w-4 h-4" />
                    <span className="text-xs">Download PDF</span>
                  </Button>
                  <Button 
                    variant="outline" 
                    className="h-16 flex flex-col items-center justify-center gap-1"
                    onClick={handleFileUpload}
                  >
                    <Upload className="w-4 h-4" />
                    <span className="text-xs">Upload Files</span>
                  </Button>
                  <Button 
                    variant="outline" 
                    className="h-16 flex flex-col items-center justify-center gap-1"
                    onClick={() => onNavigate('lesson')}
                  >
                    <Volume2 className="w-4 h-4" />
                    <span className="text-xs">AI Voice Tutor</span>
                  </Button>
                </div>
              </CardContent>
            </Card>

            {/* Content Display */}
            {selectedContent && generatedContent[selectedContent] && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    {selectedContent === 'diagram' && <Image className="w-5 h-5" />}
                    {selectedContent === 'story' && <BookOpen className="w-5 h-5" />}
                    {selectedContent === 'lesson' && <BookOpen className="w-5 h-5" />}
                    {selectedContent === 'research' && <FileText className="w-5 h-5" />}
                    {selectedContent === 'flashcards' && <Layers className="w-5 h-5" />}
                    {selectedContent.charAt(0).toUpperCase() + selectedContent.slice(1)}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="whitespace-pre-wrap text-sm bg-muted p-4 rounded border">
                    {generatedContent[selectedContent]}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Quiz & Assessment */}
            <Card>
              <CardHeader>
                <CardTitle>QUIZ & ASSESSMENT</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 gap-3">
                  <Button onClick={() => onNavigate('quiz')}>
                    <Wand2 className="w-4 h-4 mr-2" />
                    Generate Quiz
                  </Button>
                  <Button onClick={() => onNavigate('quiz')}>
                    <FileText className="w-4 h-4 mr-2" />
                    Quiz Me
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Gamification */}
            <Card>
              <CardHeader>
                <CardTitle>GAMIFICATION</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="text-center space-y-2">
                  <p className="text-sm text-muted-foreground">Current Level</p>
                  <div className="text-3xl">🏆</div>
                  <p className="text-sm">Level 7</p>
                  <Progress value={75} className="h-2" />
                </div>
                
                <div className="space-y-2">
                  <p className="text-sm">Achievement Badges</p>
                  <div className="grid grid-cols-2 gap-2">
                    <div className="text-center p-2 border rounded">
                      <div className="text-lg">🏆</div>
                      <div className="text-xs">Quiz Master</div>
                    </div>
                    <div className="text-center p-2 border rounded opacity-50">
                      <div className="text-lg">🔬</div>
                      <div className="text-xs">Research Pro</div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Performance Stats */}
            <Card>
              <CardHeader>
                <CardTitle>MY PERFORMANCE</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="text-center space-y-2">
                  <p className="text-sm text-muted-foreground">CLASS RANK</p>
                  <p className="text-xs text-muted-foreground">Out of 45 students</p>
                  <div className="text-3xl">#7</div>
                  <p className="text-sm">1,250 points</p>
                </div>

                <div className="space-y-2">
                  <p className="text-sm">Recent Activity</p>
                  <div className="space-y-2 text-xs">
                    <div className="flex justify-between">
                      <span>Topics Explored</span>
                      <span>12</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Quizzes Taken</span>
                      <span>8</span>
                    </div>
                    <div className="flex justify-between text-muted-foreground">
                      <span>Average Score</span>
                      <Badge variant="secondary" className="text-xs">92%</Badge>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <div className="text-center">
              <p className="text-sm text-muted-foreground mb-2">Welcome, {user.name}! 🎯</p>
              <p className="text-xs text-muted-foreground">{selectedDepartment} Student</p>
            </div>
          </div>
        </div>
      )}

      {!currentTopic && (
        <div className="text-center py-12">
          <div className="text-6xl mb-4">🎓</div>
          <h3 className="text-lg mb-2">Ready to Learn?</h3>
          <p className="text-muted-foreground">Enter a topic above to start your learning journey</p>
        </div>
      )}

      {/* AI Assistant Button - Only for UG */}
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
          <AIChatBot onClose={() => setShowChat(false)} userType="ug" />
        </div>
      )}
    </div>
  );
}