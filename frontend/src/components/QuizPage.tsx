import React, { useState, useEffect } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Progress } from './ui/progress';
import { Badge } from './ui/badge';
import { RadioGroup, RadioGroupItem } from './ui/radio-group';
import { Label } from './ui/label';
import { ArrowLeft, CheckCircle, XCircle, RotateCcw, Trophy } from 'lucide-react';
import { User, QuizQuestion } from '../App';

interface QuizPageProps {
  user: User;
  onNavigate: (view: string) => void;
  onBack: () => void;
}

export function QuizPage({ user, onNavigate, onBack }: QuizPageProps) {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<string>('');
  const [showResults, setShowResults] = useState(false);
  const [userAnswers, setUserAnswers] = useState<number[]>([]);
  const [score, setScore] = useState(0);
  const [showExplanation, setShowExplanation] = useState(false);

  const questions: QuizQuestion[] = user.role === 'ug' 
    ? [
        {
          id: '1',
          question: 'What is the primary reason an induction motor requires a starting mechanism?',
          options: [
            'To reduce starting current',
            'To increase starting torque',
            'Both to reduce starting current and increase starting torque',
            'To prevent overheating'
          ],
          correct: 2,
          explanation: 'Induction motors require starting mechanisms to both reduce the high starting current (which can be 5-7 times the rated current) and to provide adequate starting torque for the load.'
        },
        {
          id: '2',
          question: 'Which starting method is most commonly used for large induction motors?',
          options: [
            'Direct-on-line starting',
            'Star-delta starting',
            'Auto-transformer starting',
            'Rotor resistance starting'
          ],
          correct: 1,
          explanation: 'Star-delta starting is widely used for large induction motors as it reduces starting current to 1/3 of direct starting while providing reasonable starting torque.'
        },
        {
          id: '3',
          question: 'In a squirrel cage induction motor, what creates the rotating magnetic field?',
          options: [
            'The rotor windings',
            'The stator windings with three-phase AC supply',
            'External magnets',
            'DC excitation'
          ],
          correct: 1,
          explanation: 'The three-phase AC supply to the stator windings creates a rotating magnetic field that rotates at synchronous speed, which induces currents in the rotor.'
        }
      ]
    : [
        {
          id: '1',
          question: 'What is the main function of chlorophyll in photosynthesis?',
          options: [
            'To absorb water',
            'To absorb light energy',
            'To release oxygen',
            'To store glucose'
          ],
          correct: 1,
          explanation: 'Chlorophyll is the green pigment in plants that absorbs light energy from the sun, which is essential for the photosynthesis process to convert carbon dioxide and water into glucose.'
        },
        {
          id: '2',
          question: 'Which gas is released as a byproduct of photosynthesis?',
          options: [
            'Carbon dioxide',
            'Nitrogen',
            'Oxygen',
            'Hydrogen'
          ],
          correct: 2,
          explanation: 'Oxygen is released as a byproduct when plants use carbon dioxide and water to make glucose during photosynthesis. This oxygen is essential for most life on Earth.'
        },
        {
          id: '3',
          question: 'Where does photosynthesis mainly occur in a plant?',
          options: [
            'Roots',
            'Stem',
            'Leaves',
            'Flowers'
          ],
          correct: 2,
          explanation: 'Photosynthesis mainly occurs in the leaves because they contain the most chloroplasts with chlorophyll, and they are positioned to receive maximum sunlight.'
        },
        {
          id: '4',
          question: 'What is the chemical equation for photosynthesis?',
          options: [
            '6CO₂ + 6H₂O + light energy → C₆H₁₂O₆ + 6O₂',
            'C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O + energy',
            'CO₂ + H₂O → C₆H₁₂O₆ + O₂',
            '6O₂ + C₆H₁₂O₆ → 6CO₂ + 6H₂O'
          ],
          correct: 0,
          explanation: 'The balanced chemical equation shows that 6 molecules of carbon dioxide plus 6 molecules of water, with light energy, produce 1 molecule of glucose and 6 molecules of oxygen.'
        }
      ];

  const handleAnswerSelect = (answerIndex: string) => {
    setSelectedAnswer(answerIndex);
  };

  const handleNext = () => {
    const newAnswers = [...userAnswers];
    newAnswers[currentQuestion] = parseInt(selectedAnswer);
    setUserAnswers(newAnswers);

    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
      setSelectedAnswer('');
      setShowExplanation(false);
    } else {
      // Calculate score
      let correctAnswers = 0;
      newAnswers.forEach((answer, index) => {
        if (answer === questions[index].correct) {
          correctAnswers++;
        }
      });
      setScore(Math.round((correctAnswers / questions.length) * 100));
      setShowResults(true);
    }
  };

  const handleShowExplanation = () => {
    setShowExplanation(true);
  };

  const handleRetakeQuiz = () => {
    setCurrentQuestion(0);
    setSelectedAnswer('');
    setShowResults(false);
    setUserAnswers([]);
    setScore(0);
    setShowExplanation(false);
  };

  const currentQuestionData = questions[currentQuestion];
  const progressPercentage = ((currentQuestion + 1) / questions.length) * 100;

  if (showResults) {
    return (
      <div className="min-h-screen bg-background p-4">
        <div className="max-w-2xl mx-auto">
          <div className="flex items-center gap-4 mb-6">
            <Button variant="outline" onClick={onBack}>
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Dashboard
            </Button>
          </div>

          <Card>
            <CardHeader className="text-center">
              <div className="mx-auto w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mb-4">
                <Trophy className="w-8 h-8 text-primary" />
              </div>
              <CardTitle>Quiz Complete!</CardTitle>
              <div className="space-y-2">
                <div className="text-4xl font-bold text-primary">{score}%</div>
                <p className="text-muted-foreground">
                  You got {userAnswers.filter((answer, index) => answer === questions[index].correct).length} out of {questions.length} questions correct
                </p>
                <Badge variant={score >= 80 ? 'default' : score >= 60 ? 'secondary' : 'destructive'}>
                  {score >= 80 ? 'Excellent' : score >= 60 ? 'Good' : 'Needs Improvement'}
                </Badge>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-3">
                <h3>Question Review</h3>
                {questions.map((question, index) => (
                  <div key={question.id} className="p-4 border rounded">
                    <div className="flex items-start gap-3">
                      {userAnswers[index] === question.correct ? (
                        <CheckCircle className="w-5 h-5 text-green-500 mt-1" />
                      ) : (
                        <XCircle className="w-5 h-5 text-red-500 mt-1" />
                      )}
                      <div className="flex-1">
                        <p className="text-sm font-medium">{question.question}</p>
                        <p className="text-xs text-muted-foreground mt-1">
                          Your answer: {question.options[userAnswers[index]]}
                        </p>
                        {userAnswers[index] !== question.correct && (
                          <p className="text-xs text-green-600 mt-1">
                            Correct answer: {question.options[question.correct]}
                          </p>
                        )}
                        <p className="text-xs text-muted-foreground mt-2">
                          {question.explanation}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              <div className="flex gap-3">
                <Button onClick={handleRetakeQuiz} variant="outline" className="flex-1">
                  <RotateCcw className="w-4 h-4 mr-2" />
                  Retake Quiz
                </Button>
                <Button onClick={onBack} className="flex-1">
                  Continue Learning
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background p-4">
      <div className="max-w-2xl mx-auto">
        <div className="flex items-center gap-4 mb-6">
          <Button variant="outline" onClick={onBack}>
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back
          </Button>
          <div className="flex-1">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-muted-foreground">
                Question {currentQuestion + 1} of {questions.length}
              </span>
              <span className="text-sm text-muted-foreground">
                {Math.round(progressPercentage)}% Complete
              </span>
            </div>
            <Progress value={progressPercentage} className="h-2" />
          </div>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>
              {user.role === 'ug' ? 'Advanced Engineering Quiz' : 'Photosynthesis Quiz'}
            </CardTitle>
            <Badge variant="outline">
              {user.role === 'ug' ? 'University Level' : 'School Level'}
            </Badge>
          </CardHeader>
          <CardContent className="space-y-6">
            <div>
              <h3 className="text-lg mb-4">{currentQuestionData.question}</h3>
              
              <RadioGroup value={selectedAnswer} onValueChange={handleAnswerSelect}>
                {currentQuestionData.options.map((option, index) => (
                  <div key={index} className="flex items-center space-x-2 p-3 border rounded hover:bg-accent/50">
                    <RadioGroupItem value={index.toString()} id={`option-${index}`} />
                    <Label htmlFor={`option-${index}`} className="flex-1 cursor-pointer">
                      {option}
                    </Label>
                  </div>
                ))}
              </RadioGroup>
            </div>

            {showExplanation && (
              <div className="p-4 bg-accent/50 rounded border">
                <h4 className="font-medium mb-2">Explanation:</h4>
                <p className="text-sm text-muted-foreground">
                  {currentQuestionData.explanation}
                </p>
              </div>
            )}

            <div className="flex gap-3">
              {!showExplanation && selectedAnswer && (
                <Button variant="outline" onClick={handleShowExplanation}>
                  Show Explanation
                </Button>
              )}
              <Button 
                onClick={handleNext}
                disabled={!selectedAnswer}
                className="flex-1"
              >
                {currentQuestion === questions.length - 1 ? 'Finish Quiz' : 'Next Question'}
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}