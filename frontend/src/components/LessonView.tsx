import React, { useState } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { ArrowLeft, Download, Upload, Play, Pause, Volume2, VolumeX } from 'lucide-react';
import { User } from '../App';

interface LessonViewProps {
  user: User;
  onNavigate: (view: string) => void;
  onBack: () => void;
}

export function LessonView({ user, onNavigate, onBack }: LessonViewProps) {
  const [isAudioPlaying, setIsAudioPlaying] = useState(false);
  const [isMuted, setIsMuted] = useState(false);

  const currentTopic = user.role === 'ug' 
    ? 'HOW AN INDUCTION MOTOR STARTS'
    : 'PHOTOSYNTHESIS';

  const lessonContent = user.role === 'ug' 
    ? {
        story: `In the world of electrical engineering, the induction motor stands as one of the most crucial innovations. When Nikola Tesla first conceived the idea of a rotating magnetic field in 1882, he laid the foundation for what would become the workhorse of modern industry.

The story begins when we apply three-phase AC power to the stator windings. These windings, positioned 120 degrees apart, create a magnetic field that rotates at synchronous speed. This rotating field cuts through the rotor conductors, inducing currents by electromagnetic induction - the same principle Faraday discovered.

However, at startup, the rotor is stationary while the magnetic field rotates at full speed. This creates a significant relative motion, inducing large currents in the rotor. These currents, while necessary for operation, can be dangerously high - often 5 to 7 times the rated current.`,
        
        summary: `Key Points of Induction Motor Starting:

• Rotating Magnetic Field: Created by three-phase stator windings
• High Starting Current: 5-7 times rated current due to stationary rotor
• Low Starting Torque: Typically 1.5-2 times rated torque
• Starting Methods: Direct-on-line, Star-delta, Auto-transformer, Soft starter
• Slip Concept: Difference between synchronous speed and rotor speed
• Power Factor: Poor at startup, improves as motor accelerates`,
        
        diagram: `Motor Starting Circuit Analysis:

Stator Windings (3-phase):
Phase A: 0° 
Phase B: 120°
Phase C: 240°

Starting Current Path:
Supply → Starter → Stator → Induced EMF in Rotor → Rotor Current

Mathematical Relations:
- Synchronous Speed: Ns = 120f/P
- Slip: s = (Ns - Nr)/Ns
- Starting Torque: T ∝ s²R₂/(R₂² + s²X₂²)
- Starting Current: Is = V/(R₁ + jX₁ + reflected rotor impedance)`,
        
        notes: `Detailed Technical Notes:

1. Electromagnetic Principles:
   - Faraday's Law of Induction
   - Lenz's Law application
   - Three-phase system advantages

2. Starting Challenges:
   - High inrush current problems
   - Voltage drop in supply system
   - Mechanical stress on motor
   - Grid stability issues

3. Starting Methods Comparison:
   - DOL: Simple but high current
   - Star-Delta: Reduced current (1/3) but reduced torque (1/3)
   - Auto-transformer: Variable voltage starting
   - Soft starter: Electronic voltage control

4. Protection Systems:
   - Overload protection
   - Short circuit protection
   - Phase failure protection
   - Under-voltage protection`
      }
    : {
        story: `In a quiet forest, a young leaf named Chlora discovered her amazing superpower. Every morning when the sun rose, she could capture sunlight and transform it into food! This magical process was called photosynthesis.

Chlora lived with millions of other leaves on a mighty oak tree. Each day, they worked together like a green factory. They would breathe in carbon dioxide from the air and drink water through their roots. Then, using the energy from sunlight, they would combine these ingredients to make glucose - their food!

As they made their food, something wonderful happened. They released oxygen into the air as a gift to all the animals and humans in the forest. "We're like nature's air purifiers!" Chlora would say proudly to her leaf friends.`,
        
        summary: `Photosynthesis - Nature's Food Factory:

• What is it? The process plants use to make their own food
• Ingredients needed: Sunlight, carbon dioxide, and water
• What's produced: Glucose (food) and oxygen
• Where it happens: Mainly in the leaves
• Why it's important: Provides food for plants and oxygen for animals
• Key player: Chlorophyll - the green pigment that captures sunlight`,
        
        diagram: `Photosynthesis Process:

Sunlight ☀️
    ↓
Chlorophyll (in leaves) 🍃
    ↓
Carbon Dioxide (CO₂) + Water (H₂O)
    ↓
Glucose (C₆H₁₂O₆) + Oxygen (O₂)

The equation:
6CO₂ + 6H₂O + light energy → C₆H₁₂O₆ + 6O₂

Parts of a leaf:
- Chloroplasts: Contain chlorophyll
- Stomata: Tiny pores for gas exchange
- Veins: Transport water and nutrients`,
        
        notes: `Study Notes - Photosynthesis:

1. Key Terms:
   - Chlorophyll: Green pigment that absorbs light
   - Stomata: Tiny holes in leaves for gas exchange
   - Glucose: Sugar that plants use for energy
   - Oxygen: Gas released as a waste product

2. Why is photosynthesis important?
   - Plants make their own food
   - Oxygen is produced for animals to breathe
   - Removes carbon dioxide from the air
   - Base of all food chains

3. Factors affecting photosynthesis:
   - Amount of sunlight
   - Temperature
   - Water availability
   - Carbon dioxide concentration`
      };

  const handleDownload = () => {
    const content = `${currentTopic} - Study Material\n\n${lessonContent.summary}\n\nDetailed Notes:\n${lessonContent.notes}`;
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${currentTopic.toLowerCase().replace(/\s+/g, '-')}-notes.txt`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const handleFileUpload = () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.pdf,.doc,.docx,.txt';
    input.onchange = (e) => {
      const file = (e.target as HTMLInputElement).files?.[0];
      if (file) {
        console.log('Uploaded:', file.name);
      }
    };
    input.click();
  };

  const toggleAudio = () => {
    setIsAudioPlaying(!isAudioPlaying);
    // In a real implementation, this would control actual audio playback
  };

  return (
    <div className="min-h-screen bg-background p-4">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-4">
            <Button variant="outline" onClick={onBack}>
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back
            </Button>
            <div>
              <h1 className="text-xl">{currentTopic}</h1>
              <Badge variant="secondary">
                {user.role === 'ug' ? 'University Level' : 'School Level'}
              </Badge>
            </div>
          </div>
          
          <div className="flex gap-2">
            {user.role === 'ug' && (
              <Button variant="outline" onClick={toggleAudio} size="sm">
                {isAudioPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
                {isAudioPlaying ? 'Pause' : 'Play'} Audio
              </Button>
            )}
            <Button variant="outline" onClick={() => setIsMuted(!isMuted)} size="sm">
              {isMuted ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
            </Button>
            <Button variant="outline" onClick={handleDownload} size="sm">
              <Download className="w-4 h-4 mr-2" />
              Download
            </Button>
            <Button variant="outline" onClick={handleFileUpload} size="sm">
              <Upload className="w-4 h-4 mr-2" />
              Upload
            </Button>
          </div>
        </div>

        <Card>
          <CardContent className="p-6">
            <Tabs defaultValue="story" className="w-full">
              <TabsList className="grid w-full grid-cols-4">
                <TabsTrigger value="story">Story</TabsTrigger>
                <TabsTrigger value="summary">Summary</TabsTrigger>
                <TabsTrigger value="diagram">Diagram</TabsTrigger>
                <TabsTrigger value="notes">Notes</TabsTrigger>
              </TabsList>
              
              <TabsContent value="story" className="mt-6">
                <Card>
                  <CardHeader>
                    <CardTitle>The Story Behind {currentTopic}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="prose prose-sm max-w-none">
                      {lessonContent.story.split('\n\n').map((paragraph, index) => (
                        <p key={index} className="mb-4">{paragraph}</p>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
              
              <TabsContent value="summary" className="mt-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Quick Summary</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="whitespace-pre-line text-sm">
                      {lessonContent.summary}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
              
              <TabsContent value="diagram" className="mt-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Visual Diagram & Concepts</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="bg-accent/20 p-6 rounded border">
                      <pre className="text-sm whitespace-pre-wrap">
                        {lessonContent.diagram}
                      </pre>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
              
              <TabsContent value="notes" className="mt-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Detailed Study Notes</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="whitespace-pre-line text-sm">
                      {lessonContent.notes}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          </CardContent>
        </Card>

        <div className="mt-6 flex gap-4">
          <Button onClick={() => onNavigate('quiz')} className="flex-1">
            Take Quiz on This Topic
          </Button>
          <Button variant="outline" onClick={onBack} className="flex-1">
            Continue Learning
          </Button>
        </div>
      </div>
    </div>
  );
}