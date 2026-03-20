import { fmt } from '../utils/sheets';
import { Image } from 'lucide-react';

const s = {
  card: {
    background: '#fff',
    borderRadius: 16,
    border: '1px solid #e2e8f0',
    overflow: 'hidden',
    transition: 'box-shadow 0.2s, transform 0.2s',
    cursor: 'default',
  },
  imgWrap: {
    width: '100%',
    height: 200,
    background: '#f1f5f9',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    overflow: 'hidden',
  },
  img: {
    width: '100%',
    height: '100%',
    objectFit: 'cover',
  },
  placeholder: {
    color: '#cbd5e1',
  },
  info: {
    padding: '16px 20px 20px',
  },
  name: {
    fontSize: 14,
    fontWeight: 600,
    marginBottom: 12,
    whiteSpace: 'nowrap',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
    color: '#0f172a',
  },
  metrics: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: 10,
  },
  metricLabel: {
    fontSize: 11,
    color: '#94a3b8',
    textTransform: 'uppercase',
    letterSpacing: '0.04em',
  },
  metricValue: {
    fontSize: 15,
    fontWeight: 600,
    color: '#0f172a',
    marginTop: 2,
  },
};

export default function CreativeCard({ ad }) {
  const thumb = ad['Thumbnail URL'] || '';
  const hookRate = ad['Hook Rate'];
  const holdRate = ad['Hold Rate'];

  return (
    <div style={s.card}
      onMouseEnter={e => { e.currentTarget.style.boxShadow = '0 8px 30px rgba(0,0,0,0.08)'; e.currentTarget.style.transform = 'translateY(-2px)'; }}
      onMouseLeave={e => { e.currentTarget.style.boxShadow = 'none'; e.currentTarget.style.transform = 'none'; }}
    >
      <div style={s.imgWrap}>
        {thumb ? (
          <img src={thumb} alt={ad['Ad Name']} style={s.img} loading="lazy" />
        ) : (
          <Image size={40} style={s.placeholder} />
        )}
      </div>
      <div style={s.info}>
        <div style={s.name} title={ad['Ad Name']}>{ad['Ad Name'] || 'Unnamed'}</div>
        <div style={s.metrics}>
          <div><div style={s.metricLabel}>Spend</div><div style={s.metricValue}>{fmt(ad.Spend, 'money')}</div></div>
          <div><div style={s.metricLabel}>CTR</div><div style={s.metricValue}>{fmt(ad['CTR (Link)'] || ad.CTR, 'pct')}</div></div>
          <div><div style={s.metricLabel}>CPM</div><div style={s.metricValue}>{fmt(ad.CPM, 'money')}</div></div>
          <div><div style={s.metricLabel}>CPC</div><div style={s.metricValue}>{fmt(ad.CPC, 'money')}</div></div>
          {hookRate ? <div><div style={s.metricLabel}>Hook Rate</div><div style={s.metricValue}>{hookRate}%</div></div> : null}
          {holdRate ? <div><div style={s.metricLabel}>Hold Rate</div><div style={s.metricValue}>{holdRate}%</div></div> : null}
        </div>
      </div>
    </div>
  );
}
