import React from 'react';
import { useVideoConfig, Video } from 'remotion';

interface BRollOverlayProps {
  keywords: string[];
  duration: number;
}

export const BRollOverlay: React.FC<BRollOverlayProps> = ({
  keywords,
  duration,
}) => {
  const { width, height } = useVideoConfig();

  // TODO: Hier würden wir das tatsächliche B-Roll Video laden
  // Für jetzt: Platzhalter mit Animation

  return (
    <div
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        backgroundColor: '#1a1a1a',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      {/* Platzhalter für B-Roll */}
      <div
        style={{
          color: '#fff',
          fontFamily: 'Inter, sans-serif',
          fontSize: 48,
          textAlign: 'center',
          padding: 40,
        }}
      >
        <div style={{ fontSize: 120, marginBottom: 20 }}>🎬</div>
        <div>B-Roll</div>
        <div style={{ fontSize: 24, opacity: 0.7, marginTop: 20 }}>
          {keywords.slice(0, 3).join(', ') || 'Lifestyle Footage'}
        </div>
      </div>

      {/* Transition Overlay (Fade) */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'linear-gradient(180deg, rgba(0,0,0,0.3) 0%, transparent 20%, transparent 80%, rgba(0,0,0,0.3) 100%)',
          pointerEvents: 'none',
        }}
      />
    </div>
  );
};
