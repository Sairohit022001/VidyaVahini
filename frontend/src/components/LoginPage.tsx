import React, { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { User, UserRole } from '../App';
import axios from 'axios';

interface LoginPageProps {
  onLogin: (user: User) => void;
}

export function LoginPage({ onLogin }: LoginPageProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [grade, setGrade] = useState('');
  const [studentId, setStudentId] = useState('');
  const [isSignUp, setIsSignUp] = useState(false);
  const [userType, setUserType] = useState<'student' | 'teacher'>('student');
  const [passwordError, setPasswordError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const gradeOptions = [
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'
  ];

  const validatePassword = (pass: string) => {
    if (pass.length < 8) return 'Password must be at least 8 characters long';
    if (!/[A-Z]/.test(pass)) return 'Password must contain at least one uppercase letter';
    if (!/[a-z]/.test(pass)) return 'Password must contain at least one lowercase letter';
    if (!/[0-9]/.test(pass)) return 'Password must contain at least one number';
    if (!/[!@#$%^&*]/.test(pass)) return 'Password must contain at least one special character (!@#$%^&*)';
    return '';
  };

  const handleRegister = async () => {
    if (!email || !password || !name) {
      alert('Please fill in all required fields');
      return;
    }

    if (!email.includes('@')) {
      alert('Please enter a valid email address');
      return;
    }

    const passwordValidation = validatePassword(password);
    if (passwordValidation) {
      setPasswordError(passwordValidation);
      return;
    }

    if (userType === 'student' && (!grade || !studentId)) {
      alert('Please fill in grade and student ID');
      return;
    }

    setIsLoading(true);
    setPasswordError('');

    try {
      const userData: any = {
        name: name,
      };

      if (userType === 'student') {
        userData.grade = parseInt(grade);
        userData.student_id = studentId;
      }

      const payload = {
        email: email,
        password: password,
        role: userType,
        user_data: userData,
      };

      const response = await axios.post('http://localhost:8000/register', payload);
      
      alert('Registered successfully!');
      
      // Switch to login mode after successful registration
      setIsSignUp(false);
      setPassword('');
      setName('');
      setGrade('');
      setStudentId('');

    } catch (error: any) {
      console.error('Registration error:', error);
      alert('Registration failed: ' + (error.response?.data?.detail || 'Something went wrong'));
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogin = async () => {
    if (!email || !password) {
      alert('Please fill in all fields');
      return;
    }

    if (!email.includes('@')) {
      alert('Please enter a valid email address');
      return;
    }

    setIsLoading(true);

    try {
      const formData = {
        email: email,
        password: password,
      };

      const response = await axios.post('http://localhost:8000/login', formData);
      const { token, role, user_data } = response.data;

      // Store token and role in localStorage
      localStorage.setItem('token', token);
      localStorage.setItem('role', role);

      alert('Login successful!');

      // Create user object for the app
      const user: User = {
        id: user_data?.id || 'user-1',
        name: user_data?.name || email.split('@')[0],
        email: email,
        role: role as UserRole,
        class: role === 'teacher' ? 'Class 6D' : `Class ${user_data?.grade || '6'}`,
        subject: role === 'teacher' ? 'Mathematics' : 'Science'
      };

      onLogin(user);

    } catch (error: any) {
      console.error('Login error:', error);
      alert('Login failed: ' + (error.response?.data?.detail || 'Invalid credentials'));
    } finally {
      setIsLoading(false);
    }
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
              </div>
            )}

            {/* Form Fields */}
            <div className="space-y-3">
              {isSignUp && (
                <Input
                  type="text"
                  placeholder="Enter your full name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                />
              )}

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

              {/* Student-specific fields for registration */}
              {isSignUp && userType === 'student' && (
                <>
                  <div>
                    <label className="text-sm font-medium">Grade:</label>
                    <Select value={grade} onValueChange={setGrade}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select your grade" />
                      </SelectTrigger>
                      <SelectContent>
                        {gradeOptions.map((gradeOption) => (
                          <SelectItem key={gradeOption} value={gradeOption}>
                            Grade {gradeOption}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <Input
                    type="text"
                    placeholder="Enter your Student ID"
                    value={studentId}
                    onChange={(e) => setStudentId(e.target.value)}
                  />
                </>
              )}

              <Button 
                onClick={isSignUp ? handleRegister : handleLogin}
                className="w-full"
                disabled={isLoading}
              >
                {isLoading ? 'Please wait...' : (isSignUp ? 'Sign Up' : 'Sign In')}
              </Button>
            </div>

            <div className="text-center">
              <Button
                variant="link"
                onClick={() => {
                  setIsSignUp(!isSignUp);
                  setName('');
                  setGrade('');
                  setStudentId('');
                  setUserType('student');
                  setPasswordError('');
                }}
                className="text-sm"
                disabled={isLoading}
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
