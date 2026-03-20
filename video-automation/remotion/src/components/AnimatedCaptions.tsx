import React from 'react';
import { useCurrentFrame, useVideoConfig, interpolate, Easing } from 'remotion';

interface AnimatedCaptionsProps {
  words: Array<{
    word: string;
    start: number;
    end: number;
    confidence: number;
  }>;
  fps: number;
  mood: string;
}

export const AnimatedCaptions: React.FC<AnimatedCaptionsProps> = ({
  words,
  fps,
  mood,
}) => {
  const frame = useCurrentFrame();
  const currentTime = frame / fps;

  // Finde aktuelle Wörter (max 3-4 auf einmal)
  const visibleWords = words.filter(
    (w) => currentTime >= w.start - 0.2 && currentTime <= w.end + 0.5
  );

  if (visibleWords.length === 0) return null;

  // Style basierend auf Mood
  const getMoodStyle = () => {
    switch (mood) {
      case 'excited':
        return {
          color: '#FFD700',
          textShadow: '4px 4px 0px #FF6B35',
          transform: 'rotate(-2deg)',
        };
      case 'urgent':
        return {
          color: '#FF4444',
          textShadow: '3px 3px 0px #8B0000',
        };
      case 'calm':
        return {
          color: '#FFFFFF',
          textShadow: '2px 2px 4px rgba(0,0,0,0.8)',
        };
      default:
        return {
          color: '#FFFFFF',
          textShadow: '3px 3px 0px rgba(0,0,0,0.9)',
        };
    }
  };

  return (
    <div
      style={{
        position: 'absolute',
        bottom: 150,
        left: 0,
        right: 0,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 20,
        padding: '0 40px',
      }}
    >
      {visibleWords.slice(0, 3).map((word, index) => {
        const wordProgress =
          (currentTime - word.start) / (word.end - word.start);

        // Animation: Pop-in
        const scale = interpolate(
          wordProgress,
          [0, 0.3, 1],
          [0.5, 1.1, 1],
          {
            easing: Easing.out(Easing.back(1.2)),
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          }
        );

        const opacity = interpolate(
          wordProgress,
          [0, 0.1, 0.9, 1],
          [0, 1, 1, 0],
          {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          }
        );

        // Highlight aktuelles Wort
        const isCurrent = currentTime >= word.start && currentTime <= word.end;
        const highlightScale = isCurrent ? 1.15 : 1;

        return (
          <span
            key={`${word.word}-${index}`}
            style={{
              fontFamily: 'Inter, system-ui, sans-serif',
              fontSize: 80,
              fontWeight: 900,
              textTransform: 'uppercase',
              letterSpacing: 2,
              transform: `scale(${scale * highlightScale})`,
              opacity,
              ...getMoodStyle(),
            }}
          >
            {word.word}
          </span>
        );
      })}
    </div>
  );
};
