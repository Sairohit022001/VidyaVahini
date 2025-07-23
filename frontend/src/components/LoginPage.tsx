import React, { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { User, UserRole } from '../App';

interface LoginPageProps {
  onLogin: (user: User) => void;
}

export function LoginPage({ onLogin }: LoginPageProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isSignUp, setIsSignUp] = useState(false);
  const [selectedClass, setSelectedClass] = useState('');
  const [userType, setUserType] = useState<'student' | 'teacher'>('student');
  const [passwordError, setPasswordError] = useState('');

  const classOptions = [
    'Class 1', 'Class 2', 'Class 3', 'Class 4', 'Class 5',
    'Class 6', 'Class 7', 'Class 8', 'Class 9', 'Class 10', 'UG'
  ];

  const validatePassword = (pass: string) => {
    if (pass.length < 8) return 'Password must be at least 8 characters long';
    if (!/[A-Z]/.test(pass)) return 'Password must contain at least one uppercase letter';
    if (!/[a-z]/.test(pass)) return 'Password must contain at least one lowercase letter';
    if (!/[0-9]/.test(pass)) return 'Password must contain at least one number';
    if (!/[!@#$%^&*]/.test(pass)) return 'Password must contain at least one special character (!@#$%^&*)';
    return '';
  };

  const handleGoogleAuth = () => {
    if (isSignUp && userType === 'student' && !selectedClass) {
      alert('Please select your class');
      return;
    }

    const mockUser: User = {
      id: 'google-user-1',
      name: 'Google User',
      email: 'user@gmail.com',
      role: userType === 'teacher' ? 'teacher' : selectedClass === 'UG' ? 'ug' : 'student',
      class: userType === 'teacher' ? 'Class 6D' : (selectedClass === 'UG' ? 'Engineering' : selectedClass),
      subject: userType === 'teacher' ? 'Mathematics' : (selectedClass === 'UG' ? 'Computer Science' : 'Science')
    };
    onLogin(mockUser);
  };

  const handleEmailAuth = () => {
    if (!email || !password) {
      alert('Please fill in all fields');
      return;
    }
    
    if (isSignUp) {
      const passwordValidation = validatePassword(password);
      if (passwordValidation) {
        setPasswordError(passwordValidation);
        return;
      }
      if (userType === 'student' && !selectedClass) {
        alert('Please select your class');
        return;
      }
    }
    
    setPasswordError('');
    const role: UserRole = userType === 'teacher' ? 'teacher' : selectedClass === 'UG' ? 'ug' : 'student';
    const mockUser: User = {
      id: 'email-user-1',
      name: email.split('@')[0],
      email,
      role,
      class: userType === 'teacher' ? 'Class 6D' : (selectedClass === 'UG' ? 'Engineering' : selectedClass),
      subject: userType === 'teacher' ? 'Mathematics' : (selectedClass === 'UG' ? 'Computer Science' : 'Science')
    };
    onLogin(mockUser);
  };

  const handleDemoLogin = (role: UserRole) => {
    const demoUsers = {
      student: {
        id: 'demo-student',
        name: 'Demo Student',
        email: 'student@demo.com',
        role: 'student' as UserRole,
        class: 'Class 8',
        subject: 'Science'
      },
      teacher: {
        id: 'demo-teacher',
        name: 'Demo Teacher',
        email: 'teacher@demo.com',
        role: 'teacher' as UserRole,
        class: 'Class 6D',
        subject: 'Mathematics'
      },
      ug: {
        id: 'demo-ug',
        name: 'Demo UG Student',
        email: 'ug@demo.com',
        role: 'ug' as UserRole,
        class: 'Engineering',
        subject: 'Computer Science'
      }
    };
    
    onLogin(demoUsers[role]);
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden">
      {/* Aesthetic Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-50 to-purple-50 dark:from-gray-900 dark:to-gray-800">
        {/* Background Elements */}
        <div className="absolute top-10 left-10 text-6xl opacity-10 rotate-12">📚</div>
        <div className="absolute top-32 right-20 text-4xl opacity-10 -rotate-12">✏️</div>
        <div className="absolute bottom-20 left-20 text-5xl opacity-10 rotate-45">💻</div>
        <div className="absolute bottom-40 right-10 text-3xl opacity-10 -rotate-12">📝</div>
        <div className="absolute top-1/2 left-1/4 text-4xl opacity-10 rotate-12">🎓</div>
        <div className="absolute top-1/3 right-1/3 text-5xl opacity-10 -rotate-45">📖</div>
        <div className="absolute bottom-1/3 left-1/2 text-3xl opacity-10 rotate-90">🖊️</div>
        
        {/* Floating geometric shapes */}
        <div className="absolute top-20 right-1/4 w-16 h-16 border-2 border-blue-200 opacity-20 rotate-45"></div>
        <div className="absolute bottom-32 left-1/3 w-20 h-20 border-2 border-purple-200 opacity-20 rounded-full"></div>
        <div className="absolute top-1/2 right-10 w-12 h-12 bg-gradient-to-r from-blue-200 to-purple-200 opacity-20 rotate-12"></div>
      </div>

      <div className="w-full max-w-md space-y-6 relative z-10">
        {/* Logo and Header */}
        <div className="text-center space-y-2">
          <h1 className="text-3xl tracking-tight">VIDYAVĀHINĪ</h1>
          <p className="text-muted-foreground">Sign in to continue your learning journey</p>
        </div>

        {/* Demo Access Cards */}
        {/* <div className="space-y-3">
          <p className="text-sm text-center text-muted-foreground">Quick Demo Access</p>
          
          <div className="grid grid-cols-2 gap-3">
            <Button 
              variant="outline" 
              onClick={() => handleDemoLogin('student')}
              className="h-16 flex flex-col items-center justify-center gap-2 bg-white/80 backdrop-blur-sm"
            >
              <span className="text-2xl">🎓</span>
              <span className="text-sm">Student Demo</span>
            </Button>
            <Button 
              variant="outline" 
              onClick={() => handleDemoLogin('teacher')}
              className="h-16 flex flex-col items-center justify-center gap-2 bg-white/80 backdrop-blur-sm"
            >
              <span className="text-2xl">👨‍🏫</span>
              <span className="text-sm">Teacher Demo</span>
            </Button>
          </div>
        </div> */}

        {/* Main Login Card */}
        <Card className="bg-white/90 backdrop-blur-sm">
          <CardHeader>
            <CardTitle>{isSignUp ? 'Sign Up' : 'Login'}</CardTitle>
            <CardDescription>
              {isSignUp ? 'Create your account' : 'Welcome back'}
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* User Type Selection for Sign Up */}
            {isSignUp && (
              <div className="space-y-3">
                <div>
                  <label className="text-sm font-medium">I am a:</label>
                  <Select value={userType} onValueChange={(value: 'student' | 'teacher') => setUserType(value)}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="student">Student</SelectItem>
                      <SelectItem value="teacher">Teacher</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                {userType === 'student' && (
                  <div>
                    <label className="text-sm font-medium">Select your class:</label>
                    <Select value={selectedClass} onValueChange={setSelectedClass}>
                      <SelectTrigger>
                        <SelectValue placeholder="Choose your class" />
                      </SelectTrigger>
                      <SelectContent>
                        {classOptions.map((cls) => (
                          <SelectItem key={cls} value={cls}>{cls}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                )}
              </div>
            )}

            {/* Google Auth */}
            <Button 
              onClick={handleGoogleAuth}
              className="w-full"
              variant="outline"
              disabled={isSignUp && userType === 'student' && !selectedClass}
            >
              Continue with Google
            </Button>
            
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t"></div>
              </div>
              <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-background px-2 text-muted-foreground">Or continue with</span>
              </div>
            </div>

            {/* Email/Password */}
            <div className="space-y-3">
              <Input
                type="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
              <div>
                <Input
                  type="password"
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => {
                    setPassword(e.target.value);
                    if (passwordError) setPasswordError('');
                  }}
                />
                {passwordError && (
                  <p className="text-xs text-destructive mt-1">{passwordError}</p>
                )}
                {isSignUp && (
                  <div className="text-xs text-muted-foreground mt-1">
                    Password must be 8+ characters with uppercase, lowercase, number, and special character
                  </div>
                )}
              </div>
              <Button 
                onClick={handleEmailAuth}
                className="w-full"
                disabled={isSignUp && userType === 'student' && !selectedClass}
              >
                {isSignUp ? 'Sign Up' : 'Sign In'}
              </Button>
            </div>

            <div className="text-center">
              <Button
                variant="link"
                onClick={() => {
                  setIsSignUp(!isSignUp);
                  setSelectedClass('');
                  setUserType('student');
                  setPasswordError('');
                }}
                className="text-sm"
              >
                {isSignUp ? 'Already have an account? Sign In' : "Don't have an account? Sign Up"}
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}