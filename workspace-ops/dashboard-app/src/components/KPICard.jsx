import { TrendingUp, TrendingDown } from 'lucide-react';
import { fmt } from '../utils/sheets';

const style = {
  card: {
    background: '#fff',
    borderRadius: 16,
    padding: '24px',
    border: '1px solid #e2e8f0',
    display: 'flex',
    flexDirection: 'column',
    gap: 4,
  },
  label: {
    fontSize: 12,
    fontWeight: 500,
    color: '#94a3b8',
    textTransform: 'uppercase',
    letterSpacing: '0.05em',
  },
  value: {
    fontSize: 28,
    fontWeight: 700,
    color: '#0f172a',
    lineHeight: 1.2,
  },
  change: {
    display: 'flex',
    alignItems: 'center',
    gap: 4,
    fontSize: 13,
    fontWeight: 500,
    marginTop: 4,
  },
};

export default function KPICard({ label, value, change, invert }) {
  const isPositive = invert ? change < 0 : change > 0;
  const color = change === null || change === undefined ? '#94a3b8' : isPositive ? '#22c55e' : '#ef4444';

  return (
    <div style={style.card}>
      <div style={style.label}>{label}</div>
      <div style={style.value}>{value}</div>
      {change !== null && change !== undefined && (
        <div style={{ ...style.change, color }}>
          {isPositive ? <TrendingUp size={14} /> : <TrendingDown size={14} />}
          {change > 0 ? '+' : ''}{change}%
        </div>
      )}
    </div>
  );
}
