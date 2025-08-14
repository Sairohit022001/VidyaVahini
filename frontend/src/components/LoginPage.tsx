import React, { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { User, UserRole } from '../App';
import axios from 'axios';
import { auth } from '../firebase-config';
import { signInWithEmailAndPassword, createUserWithEmailAndPassword, updateProfile } from 'firebase/auth';

interface LoginPageProps {
  onLogin: (user: User) => void;
}

const gradeOptions = [
  '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'
];

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

  const validatePassword = (pass: string) => {
    if (pass.length < 8) return 'Password must be at least 8 characters long';
    if (!/[a-z]/.test(pass)) return 'Password must contain at least one lowercase letter';
    if (!/[A-Z]/.test(pass)) return 'Password must contain at least one uppercase letter';
    if (!/[0-9]/.test(pass)) return 'Password must contain at least one number';
    if (!/[!@#$%^&*]/.test(pass)) return 'Password must contain at least one special character (!@#$%^&*)';
    return '';
  };

  const clearFields = () => {
    setPassword('');
    setName('');
    setGrade('');
    setStudentId('');
    setPasswordError('');
    setEmail('');
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
      // 1. Create user in Firebase Authentication
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);

      // 2. Optionally update user profile with displayName
      if (auth.currentUser) {
        await updateProfile(auth.currentUser, { displayName: name });
      }

      // 3. Prepare user data to send to your backend (exclude password for security)
      const userData: Record<string, any> = { 
        name,  // Include name in user_data
        uid: userCredential.user.uid  // Move uid to user_data
      };
      if (userType === 'student') {
        userData.grade = parseInt(grade);
        userData.student_id = studentId;
      }
  
      const payload = {
        email,
        password,  // ← Add password back
        role: userType,
        name,      // ← Add name as direct field
        user_data: userData,
      };
      
      // 4. Send user data to your backend API
      await axios.post('/register', payload);

      alert('Registered successfully!');
      setIsSignUp(false);
      clearFields();
      setUserType('student');
    } catch (error: any) {
      console.error('Registration error:', error);
      alert('Registration failed: ' + (error.response?.data?.detail || error.message || 'Something went wrong'));
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
      const userCredential = await signInWithEmailAndPassword(auth, email, password);
      const user = userCredential.user;

      // Fetch user role and other info from backend (replace URL as per your API)
      const backendResponse = await axios.get(`http://localhost:8000/users/${user.uid}`);
      const userRole: UserRole = backendResponse.data.role || 'student';

      const authenticatedUser: User = {
        id: user.uid,
        name: user.displayName || user.email || 'User',
        email: user.email || '',
        role: userRole,
        class: userRole === 'teacher' ? 'Class 6D' : 'Class 6',
        subject: userRole === 'teacher' ? 'Mathematics' : 'Science'
      };

      const token = await user.getIdToken();
      localStorage.setItem('token', token);
      localStorage.setItem('role', userRole);
      alert('Login successful!');
      onLogin(authenticatedUser);
    } catch (error: any) {
      console.error('Login error:', error);
      let errorMessage = 'Login failed. Please check your credentials.';
      if (error.code) {
        switch (error.code) {
          case 'auth/user-not-found':
            errorMessage = 'No user found with this email.';
            break;
          case 'auth/wrong-password':
            errorMessage = 'Incorrect password.';
            break;
          case 'auth/invalid-email':
            errorMessage = 'Invalid email address.';
            break;
          case 'auth/invalid-credential':
            errorMessage = 'Invalid credentials.';
            break;
          default:
            errorMessage = error.message;
        }
      } else if (error.message) {
        errorMessage = error.message;
      }
      alert(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDemoLogin = (role: UserRole) => {
    const demoUsers: Record<UserRole, User> = {
      student: {
        id: 'demo-student',
        name: 'Demo Student',
        email: 'student@demo.com',
        role: 'student',
        class: 'Class 8',
        subject: 'Science',
      },
      teacher: {
        id: 'demo-teacher',
        name: 'Demo Teacher',
        email: 'teacher@demo.com',
        role: 'teacher',
        class: 'Class 6D',
        subject: 'Mathematics',
      },
      ug: {
        id: 'demo-ug',
        name: 'Demo UG Student',
        email: 'ug@demo.com',
        role: 'ug',
        class: 'Engineering',
        subject: 'Computer Science',
      },
      guest: {
        id: 'demo-guest',
        name: 'Guest User',
        email: 'guest@demo.com',
        role: 'guest',
        class: 'General',
        subject: 'All Subjects',
      }
    };
    onLogin(demoUsers[role]);
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden">
      {/* Aesthetic Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-50 to-purple-50 dark:from-gray-900 dark:to-gray-800">
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
        <div className="text-center space-y-2">
          <h1 className="text-3xl tracking-tight">VIDYAVĀHINĪ</h1>
          <p className="text-muted-foreground">Sign in to continue your learning journey</p>
        </div>
        <Card className="bg-white/90 backdrop-blur-sm">
          <CardHeader>
            <CardTitle>{isSignUp ? 'Sign Up' : 'Login'}</CardTitle>
            <CardDescription>
              {isSignUp ? 'Create your account' : 'Welcome back'}
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {isSignUp && (
              <div className="space-y-3">
                <div>
                  <label className="text-sm font-medium">I am a:</label>
                  <Select 
                    value={userType} 
                    onValueChange={(value) => setUserType(value as 'student' | 'teacher')}
                  >
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
                    Password must be 8+ characters, include uppercase, lowercase, number, and special character
                  </div>
                )}
              </div>
              {isSignUp && userType === 'student' && (
                <>
                  <div>
                    <label className="text-sm font-medium">Grade:</label>
                    <Select value={grade} onValueChange={val => setGrade(val)}>
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
                  clearFields();
                  setUserType('student');
                }}
                className="text-sm"
                disabled={isLoading}
              >
                {isSignUp ? 'Already have an account? Sign In' : "Don't have an account? Sign Up"}
              </Button>
            </div>
            {/* Uncomment demo buttons if need demo login */}
            {/* <div className="flex justify-center gap-4 mt-3">
              <Button onClick={() => handleDemoLogin('student')}>Demo Student</Button>
              <Button onClick={() => handleDemoLogin('teacher')}>Demo Teacher</Button>
            </div> */}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
