import React, { useState } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { ArrowLeft, Save, Send, Wand2, Image, BookOpen, Volume2, FileText, HelpCircle, Lightbulb, Sparkles } from 'lucide-react';
import { User } from '../App';

interface LessonPlannerProps {
  user: User;
  onNavigate: (view: string) => void;
  onBack: () => void;
}

export function LessonPlanner({ user, onNavigate, onBack }: LessonPlannerProps) {
  const [lessonData, setLessonData] = useState({
    title: '',
    subject: user.subject || 'Mathematics',
    class: user.class || 'Class 6D',
    topic: '',
    duration: 45,
    story: '',
    summary: '',
    notes: '',
    worksheet: '',
    diagram: '',
    audio: '',
    researchPaper: '',
    qna: '',
    status: 'draft' as 'draft' | 'published'
  });

  const [isGenerating, setIsGenerating] = useState<string | null>(null);
  const [selectedContent, setSelectedContent] = useState<string | null>(null);

  const subjects = ['Mathematics', 'Science', 'English', 'Hindi', 'Social Science'];
  const classes = ['Class 6D', 'Class 7A', 'Class 8B'];

  const generateAllContent = async () => {
    if (!lessonData.title) {
      alert('Please enter a lesson title first');
      return;
    }

    setIsGenerating('all');
    
    // Simulate AI generation
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    const content = {
      story: `Once upon a time, in the magical world of ${lessonData.topic || lessonData.title}, there lived a curious student who discovered the wonders of ${lessonData.subject.toLowerCase()}. Through exciting adventures and challenges, they learned the fundamental concepts that would shape their understanding forever.`,
      
      summary: `This lesson covers the essential concepts of ${lessonData.topic || lessonData.title}. Students will learn the basic principles, understand key terminology, and apply their knowledge through practical examples. The lesson is designed to build a strong foundation for advanced topics.`,
      
      notes: `KEY CONCEPTS:\n• Definition and importance of ${lessonData.topic || lessonData.title}\n• Basic principles and rules\n• Common applications\n• Examples and practice problems\n\nIMPORTANT POINTS:\n• Remember the key formula\n• Practice regularly\n• Connect with real-world examples`,
      
      worksheet: `WORKSHEET: ${lessonData.topic || lessonData.title}\n\nName: _______________  Date: _________\n\n1. Define ${lessonData.topic || lessonData.title}\n2. List three important characteristics\n3. Solve the following problems:\n   a) Example problem 1\n   b) Example problem 2\n4. Explain in your own words why this topic is important`,
      
      diagram: `[Visual Diagram Generated]\n\nThis interactive diagram shows the key components of ${lessonData.topic || lessonData.title}:\n\n1. Main concept visualization\n2. Process flow charts\n3. Connecting relationships\n4. Real-world applications\n\nStudents can interact with each element to understand the connections better.`,
      
      audio: `<speak>\n<p>Welcome to today's lesson on <emphasis level="strong">${lessonData.topic || lessonData.title}</emphasis>.</p>\n<break time="1s"/>\n<p>Let's begin our journey of discovery together.</p>\n<p>Pay attention to the key concepts and <emphasis>remember to take notes</emphasis>.</p>\n</speak>`,
      
      researchPaper: `Research Paper: ${lessonData.topic || lessonData.title}\n\nAbstract: This paper explores the advanced concepts of ${lessonData.topic || lessonData.title} and its applications in modern education.\n\nIntroduction: The study of ${lessonData.topic || lessonData.title} has evolved significantly over the years...\n\nMethodology: Our research approach includes theoretical analysis and practical applications...\n\nFindings: Key discoveries indicate that students learn better when concepts are presented with real-world examples...\n\nConclusion: The implications for education are substantial and support interactive learning methods.`,
      
      qna: `Q&A for ${lessonData.topic || lessonData.title}:\n\nQ1: What is ${lessonData.topic || lessonData.title}?\nA1: ${lessonData.topic || lessonData.title} is a fundamental concept that helps students understand the underlying principles of ${lessonData.subject}.\n\nQ2: Why is this topic important?\nA2: This topic forms the foundation for advanced learning and has practical applications in daily life.\n\nQ3: How can students apply this knowledge?\nA3: Students can use these concepts to solve real-world problems and build upon this knowledge for future learning.\n\nQ4: What are common mistakes to avoid?\nA4: Common mistakes include not understanding the basic principles and failing to practice regularly.`
    };
    
    setLessonData(prev => ({
      ...prev,
      ...content
    }));
    
    setIsGenerating(null);
  };

  const generateContent = async (type: string) => {
    setIsGenerating(type);
    
    // Simulate AI generation
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    const content = {
      story: `Once upon a time, in the magical world of ${lessonData.topic || lessonData.title}, there lived a curious student who discovered the wonders of ${lessonData.subject.toLowerCase()}. Through exciting adventures and challenges, they learned the fundamental concepts that would shape their understanding forever.`,
      
      summary: `This lesson covers the essential concepts of ${lessonData.topic || lessonData.title}. Students will learn the basic principles, understand key terminology, and apply their knowledge through practical examples. The lesson is designed to build a strong foundation for advanced topics.`,
      
      diagram: `[Visual Diagram Generated]\n\nThis interactive diagram shows the key components of ${lessonData.topic || lessonData.title}:\n\n1. Main concept visualization\n2. Process flow charts\n3. Connecting relationships\n4. Real-world applications\n\nStudents can interact with each element to understand the connections better.`,
      
      audio: `<speak>\n<p>Welcome to today's lesson on <emphasis level="strong">${lessonData.topic || lessonData.title}</emphasis>.</p>\n<break time="1s"/>\n<p>Let's begin our journey of discovery together.</p>\n<p>Pay attention to the key concepts and <emphasis>remember to take notes</emphasis>.</p>\n</speak>`,
      
      researchPaper: `Research Paper: ${lessonData.topic || lessonData.title}\n\nAbstract: This paper explores the advanced concepts of ${lessonData.topic || lessonData.title} and its applications in modern education.\n\nIntroduction: The study of ${lessonData.topic || lessonData.title} has evolved significantly over the years...\n\nMethodology: Our research approach includes theoretical analysis and practical applications...\n\nFindings: Key discoveries indicate that students learn better when concepts are presented with real-world examples...\n\nConclusion: The implications for education are substantial and support interactive learning methods.`,
      
      qna: `Q&A for ${lessonData.topic || lessonData.title}:\n\nQ1: What is ${lessonData.topic || lessonData.title}?\nA1: ${lessonData.topic || lessonData.title} is a fundamental concept that helps students understand the underlying principles of ${lessonData.subject}.\n\nQ2: Why is this topic important?\nA2: This topic forms the foundation for advanced learning and has practical applications in daily life.\n\nQ3: How can students apply this knowledge?\nA3: Students can use these concepts to solve real-world problems and build upon this knowledge for future learning.\n\nQ4: What are common mistakes to avoid?\nA4: Common mistakes include not understanding the basic principles and failing to practice regularly.`
    };
    
    setLessonData(prev => ({
      ...prev,
      [type]: content[type as keyof typeof content]
    }));
    
    setSelectedContent(type);
    setIsGenerating(null);
  };

  const handleSave = () => {
    console.log('Saving lesson:', lessonData);
    alert('Lesson saved as draft!');
  };

  const handlePublish = () => {
    setLessonData(prev => ({ ...prev, status: 'published' }));
    console.log('Publishing lesson:', lessonData);
    alert('Lesson published successfully!');
  };

  return (
    <div className="min-h-screen bg-background p-4">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-4">
            <Button variant="outline" onClick={onBack}>
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Dashboard
            </Button>
            <div>
              <h1 className="text-xl">Lesson Planner</h1>
              <Badge variant={lessonData.status === 'published' ? 'default' : 'secondary'}>
                {lessonData.status}
              </Badge>
            </div>
          </div>
          
          <div className="flex gap-2">
            <Button variant="outline" onClick={handleSave} size="sm">
              <Save className="w-4 h-4 mr-2" />
              Save Draft
            </Button>
            <Button onClick={handlePublish} size="sm">
              <Send className="w-4 h-4 mr-2" />
              Publish
            </Button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Lesson Settings */}
          <div className="lg:col-span-1">
            <Card>
              <CardHeader>
                <CardTitle>Lesson Settings</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="text-sm font-medium">Lesson Title</label>
                  <Input
                    value={lessonData.title}
                    onChange={(e) => setLessonData(prev => ({ ...prev, title: e.target.value }))}
                    placeholder="Enter lesson title"
                  />
                </div>
                
                <div>
                  <label className="text-sm font-medium">Class</label>
                  <Select 
                    value={lessonData.class} 
                    onValueChange={(value) => setLessonData(prev => ({ ...prev, class: value }))}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {classes.map((cls) => (
                        <SelectItem key={cls} value={cls}>{cls}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <label className="text-sm font-medium">Subject</label>
                  <Select 
                    value={lessonData.subject} 
                    onValueChange={(value) => setLessonData(prev => ({ ...prev, subject: value }))}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {subjects.map((subject) => (
                        <SelectItem key={subject} value={subject}>{subject}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <label className="text-sm font-medium">Topic</label>
                  <Input
                    value={lessonData.topic}
                    onChange={(e) => setLessonData(prev => ({ ...prev, topic: e.target.value }))}
                    placeholder="Enter topic"
                  />
                </div>

                <div>
                  <label className="text-sm font-medium">Duration (minutes)</label>
                  <Input
                    type="number"
                    value={lessonData.duration}
                    onChange={(e) => setLessonData(prev => ({ ...prev, duration: parseInt(e.target.value) }))}
                    min={15}
                    max={120}
                  />
                </div>

                {/* Main Generate Button */}
                <Button
                  onClick={generateAllContent}
                  disabled={isGenerating === 'all' || !lessonData.title}
                  className="w-full h-12"
                  size="lg"
                >
                  <Sparkles className="w-5 h-5 mr-2" />
                  {isGenerating === 'all' ? 'Generating All Content...' : 'Generate Lesson Contents'}
                </Button>
              </CardContent>
            </Card>
          </div>

          {/* Lesson Generator */}
          <div className="lg:col-span-3">
            <Card>
              <CardContent className="p-6">
                <Tabs defaultValue="generator" className="w-full">
                  <TabsList className="grid w-full grid-cols-2">
                    <TabsTrigger value="generator">Lesson Generator</TabsTrigger>
                    <TabsTrigger value="preview">Preview & Publish</TabsTrigger>
                  </TabsList>
                  
                  <TabsContent value="generator" className="mt-6 space-y-6">
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                      <Button
                        onClick={() => generateContent('diagram')}
                        disabled={isGenerating === 'diagram'}
                        variant="outline"
                        className="h-16 flex flex-col items-center justify-center gap-2"
                      >
                        <Image className="w-5 h-5" />
                        <span className="text-sm">
                          {isGenerating === 'diagram' ? 'Generating...' : 'Generate Visual Diagrams'}
                        </span>
                      </Button>
                      <Button
                        onClick={() => generateContent('story')}
                        disabled={isGenerating === 'story'}
                        variant="outline"
                        className="h-16 flex flex-col items-center justify-center gap-2"
                      >
                        <BookOpen className="w-5 h-5" />
                        <span className="text-sm">
                          {isGenerating === 'story' ? 'Generating...' : 'Generate Story'}
                        </span>
                      </Button>
                      <Button
                        onClick={() => generateContent('audio')}
                        disabled={isGenerating === 'audio'}
                        variant="outline"
                        className="h-16 flex flex-col items-center justify-center gap-2"
                      >
                        <Volume2 className="w-5 h-5" />
                        <span className="text-sm">
                          {isGenerating === 'audio' ? 'Generating...' : 'Generate SSML Audio'}
                        </span>
                      </Button>
                      <Button
                        onClick={() => generateContent('researchPaper')}
                        disabled={isGenerating === 'researchPaper'}
                        variant="outline"
                        className="h-16 flex flex-col items-center justify-center gap-2"
                      >
                        <FileText className="w-5 h-5" />
                        <span className="text-sm">
                          {isGenerating === 'researchPaper' ? 'Generating...' : 'Generate Research Paper'}
                        </span>
                      </Button>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                      <Button
                        onClick={() => generateContent('summary')}
                        disabled={isGenerating === 'summary'}
                        variant="outline"
                        className="h-16 flex flex-col items-center justify-center gap-2"
                      >
                        <Lightbulb className="w-5 h-5" />
                        <span className="text-sm">
                          {isGenerating === 'summary' ? 'Generating...' : 'Generate Summary'}
                        </span>
                      </Button>
                      <Button
                        onClick={() => generateContent('qna')}
                        disabled={isGenerating === 'qna'}
                        variant="outline"
                        className="h-16 flex flex-col items-center justify-center gap-2"
                      >
                        <HelpCircle className="w-5 h-5" />
                        <span className="text-sm">
                          {isGenerating === 'qna' ? 'Generating...' : 'Generate Q&A'}
                        </span>
                      </Button>
                    </div>

                    {/* Content Display Area */}
                    {selectedContent && lessonData[selectedContent as keyof typeof lessonData] && (
                      <Card className="mt-6">
                        <CardHeader>
                          <CardTitle className="flex items-center gap-2">
                            {selectedContent === 'diagram' && <Image className="w-5 h-5" />}
                            {selectedContent === 'story' && <BookOpen className="w-5 h-5" />}
                            {selectedContent === 'audio' && <Volume2 className="w-5 h-5" />}
                            {selectedContent === 'researchPaper' && <FileText className="w-5 h-5" />}
                            {selectedContent === 'summary' && <Lightbulb className="w-5 h-5" />}
                            {selectedContent === 'qna' && <HelpCircle className="w-5 h-5" />}
                            {selectedContent.charAt(0).toUpperCase() + selectedContent.slice(1)}
                          </CardTitle>
                        </CardHeader>
                        <CardContent>
                          <Textarea
                            value={lessonData[selectedContent as keyof typeof lessonData] as string}
                            onChange={(e) => setLessonData(prev => ({ ...prev, [selectedContent]: e.target.value }))}
                            className="min-h-40"
                            placeholder={`Generated ${selectedContent} content will appear here...`}
                          />
                        </CardContent>
                      </Card>
                    )}
                  </TabsContent>
                  
                  <TabsContent value="preview" className="mt-6 space-y-6">
                    <div className="space-y-4">
                      <h3>Lesson Preview</h3>
                      <Card>
                        <CardContent className="p-4 space-y-3">
                          <div className="grid grid-cols-2 gap-4">
                            <div><strong>Title:</strong> {lessonData.title || 'Untitled Lesson'}</div>
                            <div><strong>Subject:</strong> {lessonData.subject}</div>
                            <div><strong>Class:</strong> {lessonData.class}</div>
                            <div><strong>Topic:</strong> {lessonData.topic || 'No topic specified'}</div>
                            <div><strong>Duration:</strong> {lessonData.duration} minutes</div>
                            <div><strong>Status:</strong> <Badge variant={lessonData.status === 'published' ? 'default' : 'secondary'}>{lessonData.status}</Badge></div>
                          </div>
                        </CardContent>
                      </Card>

                      <div className="space-y-4">
                        <h4>Content Summary</h4>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          <div className="p-4 border rounded">
                            <p className="font-medium">Story</p>
                            <p className="text-sm text-muted-foreground">{lessonData.story ? '✅ Generated' : '❌ Not generated'}</p>
                          </div>
                          <div className="p-4 border rounded">
                            <p className="font-medium">Summary</p>
                            <p className="text-sm text-muted-foreground">{lessonData.summary ? '✅ Generated' : '❌ Not generated'}</p>
                          </div>
                          <div className="p-4 border rounded">
                            <p className="font-medium">Diagrams</p>
                            <p className="text-sm text-muted-foreground">{lessonData.diagram ? '✅ Generated' : '❌ Not generated'}</p>
                          </div>
                          <div className="p-4 border rounded">
                            <p className="font-medium">Research Paper</p>
                            <p className="text-sm text-muted-foreground">{lessonData.researchPaper ? '✅ Generated' : '❌ Not generated'}</p>
                          </div>
                        </div>
                      </div>
                      
                      <div className="flex gap-3">
                        <Button onClick={handleSave} variant="outline" className="flex-1">
                          <Save className="w-4 h-4 mr-2" />
                          Save as Draft
                        </Button>
                        <Button onClick={handlePublish} className="flex-1" disabled={!lessonData.title || !lessonData.topic}>
                          <Send className="w-4 h-4 mr-2" />
                          Publish Lesson
                        </Button>
                      </div>
                    </div>
                  </TabsContent>
                </Tabs>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}