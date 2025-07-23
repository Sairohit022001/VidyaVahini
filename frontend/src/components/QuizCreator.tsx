import React, { useState } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { ArrowLeft, Plus, Trash2, Save, Send, Wand2, Copy } from 'lucide-react';
import { User, QuizQuestion } from '../App';

interface QuizCreatorProps {
  user: User;
  onNavigate: (view: string) => void;
  onBack: () => void;
}

interface QuizData {
  title: string;
  subject: string;
  class: string;
  topic: string;
  difficulty: string;
  timeLimit: number;
  questions: QuizQuestion[];
  status: 'draft' | 'published';
}

export function QuizCreator({ user, onNavigate, onBack }: QuizCreatorProps) {
  const [quiz, setQuiz] = useState<QuizData>({
    title: '',
    subject: user.subject || 'Mathematics',
    class: user.class || 'Class 6D',
    topic: '',
    difficulty: 'medium',
    timeLimit: 30,
    questions: [{
      id: '1',
      question: '',
      options: ['', '', '', ''],
      correct: 0,
      explanation: ''
    }],
    status: 'draft'
  });

  const [isGenerating, setIsGenerating] = useState(false);

  const subjects = {
    'Class 6D': ['Mathematics', 'Science', 'English', 'Hindi', 'Social Science'],
    'Class 7A': ['Mathematics', 'Science', 'English', 'Hindi', 'Social Science'],
    'Class 8B': ['Mathematics', 'Science', 'English', 'Hindi', 'Social Science'],
  };

  const quizTopics = {
    'Mathematics': [
      'Fractions and Decimals', 'Integers', 'Algebra', 'Geometry', 'Mensuration',
      'Ratio and Proportion', 'Percentage', 'Simple Interest', 'Data Handling'
    ],
    'Science': [
      'Photosynthesis', 'Respiration', 'Light', 'Sound', 'Motion and Force',
      'Electricity', 'Magnetism', 'Acids and Bases', 'Metals and Non-metals'
    ],
    'English': [
      'Grammar', 'Comprehension', 'Vocabulary', 'Writing Skills', 'Literature',
      'Poetry', 'Prose', 'Drama', 'Letter Writing'
    ]
  };

  const generateAIQuiz = async () => {
    if (!quiz.topic) {
      alert('Please select a topic first');
      return;
    }

    setIsGenerating(true);
    
    // Simulate AI generation delay
    await new Promise(resolve => setTimeout(resolve, 2000));

    const sampleQuestions: QuizQuestion[] = [
      {
        id: '1',
        question: `What is the main function of chlorophyll in ${quiz.topic.toLowerCase()}?`,
        options: [
          'To absorb water from soil',
          'To absorb light energy from sunlight',
          'To release oxygen into air',
          'To store food in leaves'
        ],
        correct: 1,
        explanation: 'Chlorophyll is the green pigment in plants that absorbs light energy from the sun, which is essential for photosynthesis.'
      },
      {
        id: '2',
        question: `Which gas is released during ${quiz.topic.toLowerCase()}?`,
        options: [
          'Carbon dioxide',
          'Nitrogen',
          'Oxygen',
          'Hydrogen'
        ],
        correct: 2,
        explanation: 'Oxygen is released as a byproduct when plants convert carbon dioxide and water into glucose during photosynthesis.'
      },
      {
        id: '3',
        question: `Where does ${quiz.topic.toLowerCase()} mainly occur in plants?`,
        options: [
          'Roots',
          'Stems',
          'Leaves',
          'Flowers'
        ],
        correct: 2,
        explanation: 'Photosynthesis mainly occurs in the leaves because they contain chloroplasts with chlorophyll and receive maximum sunlight.'
      }
    ];

    setQuiz(prev => ({
      ...prev,
      title: prev.title || `${prev.topic} Quiz`,
      questions: sampleQuestions
    }));
    
    setIsGenerating(false);
  };

  const addQuestion = () => {
    const newQuestion: QuizQuestion = {
      id: (quiz.questions.length + 1).toString(),
      question: '',
      options: ['', '', '', ''],
      correct: 0,
      explanation: ''
    };
    setQuiz(prev => ({
      ...prev,
      questions: [...prev.questions, newQuestion]
    }));
  };

  const removeQuestion = (index: number) => {
    setQuiz(prev => ({
      ...prev,
      questions: prev.questions.filter((_, i) => i !== index)
    }));
  };

  const updateQuestion = (index: number, field: string, value: any) => {
    setQuiz(prev => ({
      ...prev,
      questions: prev.questions.map((q, i) => 
        i === index ? { ...q, [field]: value } : q
      )
    }));
  };

  const updateOption = (questionIndex: number, optionIndex: number, value: string) => {
    setQuiz(prev => ({
      ...prev,
      questions: prev.questions.map((q, i) => 
        i === questionIndex ? {
          ...q,
          options: q.options.map((opt, j) => j === optionIndex ? value : opt)
        } : q
      )
    }));
  };

  const handleSave = () => {
    console.log('Saving quiz:', quiz);
    alert('Quiz saved as draft!');
  };

  const handlePublish = () => {
    setQuiz(prev => ({ ...prev, status: 'published' }));
    console.log('Publishing quiz:', quiz);
    alert('Quiz published successfully!');
  };

  const duplicateQuiz = () => {
    const duplicated = {
      ...quiz,
      title: quiz.title + ' (Copy)',
      status: 'draft' as const
    };
    setQuiz(duplicated);
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
              <h1 className="text-xl">Quiz Creator</h1>
              <Badge variant={quiz.status === 'published' ? 'default' : 'secondary'}>
                {quiz.status}
              </Badge>
            </div>
          </div>
          
          <div className="flex gap-2">
            <Button variant="outline" onClick={duplicateQuiz} size="sm">
              <Copy className="w-4 h-4 mr-2" />
              Duplicate
            </Button>
            <Button variant="outline" onClick={handleSave} size="sm">
              <Save className="w-4 h-4 mr-2" />
              Save Draft
            </Button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Quiz Settings */}
          <div className="lg:col-span-1">
            <Card>
              <CardHeader>
                <CardTitle>Quiz Settings</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="text-sm font-medium">Quiz Title</label>
                  <Input
                    value={quiz.title}
                    onChange={(e) => setQuiz(prev => ({ ...prev, title: e.target.value }))}
                    placeholder="Enter quiz title"
                  />
                </div>
                
                <div>
                  <label className="text-sm font-medium">Class</label>
                  <Select 
                    value={quiz.class} 
                    onValueChange={(value) => setQuiz(prev => ({ ...prev, class: value }))}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {Object.keys(subjects).map((cls) => (
                        <SelectItem key={cls} value={cls}>{cls}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <label className="text-sm font-medium">Subject</label>
                  <Select 
                    value={quiz.subject} 
                    onValueChange={(value) => setQuiz(prev => ({ ...prev, subject: value }))}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {subjects[quiz.class as keyof typeof subjects]?.map((subject) => (
                        <SelectItem key={subject} value={subject}>{subject}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <label className="text-sm font-medium">Topic</label>
                  <Select 
                    value={quiz.topic} 
                    onValueChange={(value) => setQuiz(prev => ({ ...prev, topic: value }))}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Select topic" />
                    </SelectTrigger>
                    <SelectContent>
                      {quizTopics[quiz.subject as keyof typeof quizTopics]?.map((topic) => (
                        <SelectItem key={topic} value={topic}>{topic}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <label className="text-sm font-medium">Difficulty</label>
                  <Select 
                    value={quiz.difficulty} 
                    onValueChange={(value) => setQuiz(prev => ({ ...prev, difficulty: value }))}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="easy">Easy</SelectItem>
                      <SelectItem value="medium">Medium</SelectItem>
                      <SelectItem value="hard">Hard</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <label className="text-sm font-medium">Time Limit (minutes)</label>
                  <Input
                    type="number"
                    value={quiz.timeLimit}
                    onChange={(e) => setQuiz(prev => ({ ...prev, timeLimit: parseInt(e.target.value) }))}
                    min={10}
                    max={120}
                  />
                </div>

                <Button 
                  onClick={generateAIQuiz}
                  className="w-full"
                  disabled={isGenerating}
                >
                  <Wand2 className="w-4 h-4 mr-2" />
                  {isGenerating ? 'Generating...' : 'Generate AI Quiz'}
                </Button>
              </CardContent>
            </Card>
          </div>

          {/* Quiz Content */}
          <div className="lg:col-span-3">
            <Card>
              <CardContent className="p-6">
                <Tabs defaultValue="questions" className="w-full">
                  <TabsList className="grid w-full grid-cols-2">
                    <TabsTrigger value="questions">Questions ({quiz.questions.length})</TabsTrigger>
                    <TabsTrigger value="preview">Preview & Publish</TabsTrigger>
                  </TabsList>
                  
                  <TabsContent value="questions" className="mt-6 space-y-6">
                    <div className="flex items-center justify-between">
                      <h3>Quiz Questions</h3>
                      <Button onClick={addQuestion} size="sm">
                        <Plus className="w-4 h-4 mr-2" />
                        Add Question
                      </Button>
                    </div>

                    {quiz.questions.map((question, qIndex) => (
                      <Card key={question.id}>
                        <CardHeader>
                          <div className="flex items-center justify-between">
                            <CardTitle className="text-base">Question {qIndex + 1}</CardTitle>
                            {quiz.questions.length > 1 && (
                              <Button variant="destructive" size="sm" onClick={() => removeQuestion(qIndex)}>
                                <Trash2 className="w-4 h-4" />
                              </Button>
                            )}
                          </div>
                        </CardHeader>
                        <CardContent className="space-y-4">
                          <div>
                            <label className="text-sm font-medium">Question</label>
                            <Textarea
                              value={question.question}
                              onChange={(e) => updateQuestion(qIndex, 'question', e.target.value)}
                              placeholder="Enter your question here..."
                              className="min-h-20"
                            />
                          </div>

                          <div className="space-y-2">
                            <label className="text-sm font-medium">Options</label>
                            {question.options.map((option, oIndex) => (
                              <div key={oIndex} className="flex gap-2 items-center">
                                <input
                                  type="radio"
                                  name={`correct-${qIndex}`}
                                  checked={question.correct === oIndex}
                                  onChange={() => updateQuestion(qIndex, 'correct', oIndex)}
                                  className="w-4 h-4"
                                />
                                <Input
                                  value={option}
                                  onChange={(e) => updateOption(qIndex, oIndex, e.target.value)}
                                  placeholder={`Option ${oIndex + 1}`}
                                  className="flex-1"
                                />
                                {question.correct === oIndex && (
                                  <Badge variant="default">Correct</Badge>
                                )}
                              </div>
                            ))}
                          </div>

                          <div>
                            <label className="text-sm font-medium">Explanation</label>
                            <Textarea
                              value={question.explanation}
                              onChange={(e) => updateQuestion(qIndex, 'explanation', e.target.value)}
                              placeholder="Explain why this answer is correct..."
                              className="min-h-16"
                            />
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </TabsContent>
                  
                  <TabsContent value="preview" className="mt-6 space-y-6">
                    <div className="space-y-4">
                      <h3>Quiz Preview</h3>
                      <Card>
                        <CardContent className="p-4 space-y-3">
                          <div className="grid grid-cols-2 gap-4">
                            <div><strong>Title:</strong> {quiz.title || 'Untitled Quiz'}</div>
                            <div><strong>Subject:</strong> {quiz.subject}</div>
                            <div><strong>Class:</strong> {quiz.class}</div>
                            <div><strong>Topic:</strong> {quiz.topic || 'No topic selected'}</div>
                            <div><strong>Difficulty:</strong> {quiz.difficulty}</div>
                            <div><strong>Time Limit:</strong> {quiz.timeLimit} minutes</div>
                            <div><strong>Questions:</strong> {quiz.questions.length}</div>
                            <div><strong>Status:</strong> <Badge variant={quiz.status === 'published' ? 'default' : 'secondary'}>{quiz.status}</Badge></div>
                          </div>
                        </CardContent>
                      </Card>

                      <div className="space-y-4">
                        <h4>Question Summary</h4>
                        {quiz.questions.map((question, index) => (
                          <Card key={question.id}>
                            <CardContent className="p-4">
                              <div className="space-y-2">
                                <div><strong>Q{index + 1}:</strong> {question.question || 'No question text'}</div>
                                <div className="grid grid-cols-2 gap-2 text-sm">
                                  {question.options.map((option, oIndex) => (
                                    <div key={oIndex} className={`p-2 rounded ${question.correct === oIndex ? 'bg-green-100 dark:bg-green-900' : 'bg-gray-100 dark:bg-gray-800'}`}>
                                      {oIndex + 1}. {option || 'Empty option'}
                                      {question.correct === oIndex && <span className="ml-2 text-green-600">✓</span>}
                                    </div>
                                  ))}
                                </div>
                              </div>
                            </CardContent>
                          </Card>
                        ))}
                      </div>
                      
                      <div className="flex gap-3">
                        <Button onClick={handleSave} variant="outline" className="flex-1">
                          <Save className="w-4 h-4 mr-2" />
                          Save as Draft
                        </Button>
                        <Button onClick={handlePublish} className="flex-1" disabled={!quiz.title || !quiz.topic || quiz.questions.some(q => !q.question)}>
                          <Send className="w-4 h-4 mr-2" />
                          Publish Quiz
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