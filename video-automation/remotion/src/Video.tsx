import React, { useEffect, useState } from 'react';
import { Sequence, useVideoConfig, AbsoluteFill, Video as RemotionVideo } from 'remotion';
import { AnimatedCaptions } from './components/AnimatedCaptions';
import { BRollOverlay } from './components/BRollOverlay';
import { Logo } from './components/Logo';

interface VideoProps {
  analysisPath: string;
  mainVideo: string;
}

interface AnalysisData {
  transcript: string;
  words: Array<{
    word: string;
    start: number;
    end: number;
    confidence: number;
  }>;
  pauses: Array<{
    start: number;
    end: number;
    duration: number;
  }>;
  scenes: Array<{
    type: string;
    start: number;
    end: number;
    confidence: number;
    keywords: string[];
  }>;
  keywords: string[];
  mood: string;
  duration: number;
  language: string;
}

export const Video: React.FC<VideoProps> = ({ analysisPath, mainVideo }) => {
  const { fps } = useVideoConfig();
  const [analysis, setAnalysis] = useState<AnalysisData | null>(null);

  // Lade Analyse-Daten
  useEffect(() => {
    fetch(analysisPath)
      .then(res => res.json())
      .then(data => setAnalysis(data))
      .catch(err => console.error('Fehler beim Laden:', err));
  }, [analysisPath]);

  if (!analysis) {
    return (
      <AbsoluteFill style={{ backgroundColor: '#000', color: '#fff' }}>
        <div style={{ 
          display: 'flex', 
          justifyContent: 'center', 
          alignItems: 'center',
          height: '100%',
          fontFamily: 'Inter, sans-serif',
          fontSize: 32
        }}>
          Lade Analyse...
        </div>
      </AbsoluteFill>
    );
  }

  const durationInFrames = Math.ceil(analysis.duration * fps);

  return (
    <AbsoluteFill style={{ backgroundColor: '#000' }}>
      {/* Haupt-Video (UGC/Talking Head) */}
      <RemotionVideo
        src={mainVideo}
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
        }}
      />

      {/* B-Roll Overlays (bei Pausen/Szenen) */}
      {analysis.scenes.map((scene, index) => {
        if (scene.type === 'broll_opportunity' && scene.duration > 1.0) {
          return (
            <Sequence
              key={`broll-${index}`}
              from={Math.floor(scene.start * fps)}
              durationInFrames={Math.floor((scene.end - scene.start) * fps)}
            >
              <BRollOverlay
                keywords={scene.keywords}
                duration={scene.end - scene.start}
              />
            </Sequence>
          );
        }
        return null;
      })}

      {/* Animated Captions */}
      <Sequence from={0} durationInFrames={durationInFrames}>
        <AnimatedCaptions
          words={analysis.words}
          fps={fps}
          mood={analysis.mood}
        />
      </Sequence>

      {/* Logo / Branding */}
      <Logo position="top-right" />

      {/* Debug Info (nur für Entwicklung) */}
      <div
        style={{
          position: 'absolute',
          bottom: 20,
          left: 20,
          color: 'rgba(255,255,255,0.5)',
          fontSize: 14,
          fontFamily: 'monospace',
        }}
      >
        Mood: {analysis.mood} | Keywords: {analysis.keywords.slice(0, 3).join(', ')}
      </div>
    </AbsoluteFill>
  );
};
