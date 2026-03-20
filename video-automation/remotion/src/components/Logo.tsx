import React from 'react';

interface LogoProps {
  position?: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left';
}

export const Logo: React.FC<LogoProps> = ({ position = 'top-right' }) => {
  const getPosition = () => {
    switch (position) {
      case 'top-right':
        return { top: 40, right: 40 };
      case 'top-left':
        return { top: 40, left: 40 };
      case 'bottom-right':
        return { bottom: 40, right: 40 };
      case 'bottom-left':
        return { bottom: 40, left: 40 };
      default:
        return { top: 40, right: 40 };
    }
  };

  return (
    <div
      style={{
        position: 'absolute',
        ...getPosition(),
        padding: '12px 24px',
        backgroundColor: 'rgba(0,0,0,0.6)',
        borderRadius: 8,
        backdropFilter: 'blur(10px)',
      }}
    >
      <span
        style={{
          color: '#fff',
          fontFamily: 'Inter, system-ui, sans-serif',
          fontSize: 24,
          fontWeight: 700,
          letterSpacing: 1,
        }}
      >
        ADSDROP
      </span>
    </div>
  );
};
