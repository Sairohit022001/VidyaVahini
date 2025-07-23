import React, { useState, useRef, useEffect } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Input } from './ui/input';
import { ScrollArea } from './ui/scroll-area';
import { X, Send, Mic, MicOff } from 'lucide-react';

interface AIChatBotProps {
  onClose: () => void;
  userType: 'student' | 'teacher' | 'ug';
}

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'ai';
  timestamp: Date;
}

export function AIChatBot({ onClose, userType }: AIChatBotProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: userType === 'teacher' 
        ? 'Hello! I\'m your AI Teaching Assistant. I can help you create lessons, generate quizzes, analyze student performance, and answer any educational questions you have.'
        : 'Hello! I\'m your AI Learning Assistant. I can help you understand concepts, solve problems, create study plans, and answer any academic questions you have.',
      sender: 'ai',
      timestamp: new Date()
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputText.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputText,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);

    // Simulate AI response
    setTimeout(() => {
      const aiResponse: Message = {
        id: (Date.now() + 1).toString(),
        text: generateAIResponse(inputText, userType),
        sender: 'ai',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, aiResponse]);
      setIsLoading(false);
    }, 1500);
  };

  const generateAIResponse = (query: string, type: string): string => {
    const lowerQuery = query.toLowerCase();
    
    if (type === 'teacher') {
      if (lowerQuery.includes('lesson') || lowerQuery.includes('teach')) {
        return 'I can help you create engaging lessons! Consider using interactive elements like diagrams, stories, and real-world examples. Would you like me to generate specific content for your topic?';
      }
      if (lowerQuery.includes('quiz') || lowerQuery.includes('assessment')) {
        return 'For effective quizzes, I recommend mixing question types: multiple choice for concept recognition, short answers for understanding, and practical problems for application. What subject are you creating a quiz for?';
      }
      if (lowerQuery.includes('student') || lowerQuery.includes('performance')) {
        return 'Student performance can be improved through personalized learning paths, regular feedback, and varied teaching methods. Would you like specific strategies for struggling students?';
      }
      return 'I can assist with lesson planning, content creation, student assessment, curriculum design, and educational best practices. What specific area would you like help with?';
    } else {
      if (lowerQuery.includes('study') || lowerQuery.includes('learn')) {
        return 'Great question! Effective studying involves active recall, spaced repetition, and connecting new concepts to what you already know. What subject are you working on?';
      }
      if (lowerQuery.includes('solve') || lowerQuery.includes('problem')) {
        return 'I\'d be happy to help you solve problems! Please share the specific problem you\'re working on, and I\'ll guide you through the solution step by step.';
      }
      if (lowerQuery.includes('explain') || lowerQuery.includes('understand')) {
        return 'I can break down complex concepts into simpler parts. What topic would you like me to explain? I can use examples, analogies, and visual descriptions to make it clearer.';
      }
      return 'I\'m here to help with your learning! I can explain concepts, help solve problems, create study plans, provide examples, and answer questions about any subject. What would you like to work on?';
    }
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;

      const audioChunks: BlobPart[] = [];
      mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data);
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        // In a real implementation, you would send this to a speech-to-text service
        // For demo purposes, we'll simulate converting speech to text
        setTimeout(() => {
          const simulatedText = 'This is converted speech text from microphone input';
          setInputText(simulatedText);
          setIsRecording(false);
        }, 1000);
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (error) {
      console.error('Error accessing microphone:', error);
      alert('Microphone access denied. Please allow microphone permissions and try again.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
    }
  };

  const toggleRecording = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  return (
    <Card className="w-full h-96 flex flex-col shadow-lg">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">
          AI {userType === 'teacher' ? 'Teaching' : 'Learning'} Assistant
        </CardTitle>
        <Button variant="ghost" size="sm" onClick={onClose}>
          <X className="w-4 h-4" />
        </Button>
      </CardHeader>
      <CardContent className="flex-1 flex flex-col p-3 space-y-3">
        {/* Messages Area */}
        <ScrollArea className="flex-1 pr-3">
          <div className="space-y-3">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[80%] rounded-lg px-3 py-2 text-sm ${
                    message.sender === 'user'
                      ? 'bg-primary text-primary-foreground'
                      : 'bg-muted text-muted-foreground'
                  }`}
                >
                  {message.text}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-muted text-muted-foreground rounded-lg px-3 py-2 text-sm">
                  AI is typing...
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </ScrollArea>

        {/* Input Area */}
        <div className="flex gap-2">
          <Input
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Type your question or use voice input..."
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            className="flex-1"
          />
          <Button
            variant={isRecording ? 'destructive' : 'outline'}
            size="sm"
            onClick={toggleRecording}
            disabled={isLoading}
          >
            {isRecording ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
          </Button>
          <Button
            onClick={handleSendMessage}
            disabled={!inputText.trim() || isLoading}
            size="sm"
          >
            <Send className="w-4 h-4" />
          </Button>
        </div>

        {isRecording && (
          <div className="text-center">
            <div className="inline-flex items-center gap-2 text-sm text-destructive">
              <div className="w-2 h-2 bg-destructive rounded-full animate-pulse"></div>
              Recording... Click mic to stop
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}