import { useState, useEffect, useMemo } from 'react';
import {
  BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Legend, ComposedChart, Area
} from 'recharts';
import { Loader2, BarChart3, Image, Table2, ChevronDown } from 'lucide-react';
import { fetchSheet, fmt, aggregate } from './utils/sheets';
import KPICard from './components/KPICard';
import CreativeCard from './components/CreativeCard';

const css = {
  header: {
    padding: '32px 48px 24px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    flexWrap: 'wrap',
    gap: 16,
  },
  title: { fontSize: 26, fontWeight: 700 },
  subtitle: { fontSize: 14, color: '#94a3b8', marginTop: 4 },
  filters: { display: 'flex', gap: 12, alignItems: 'center' },
  select: {
    padding: '10px 16px',
    border: '1px solid #e2e8f0',
    borderRadius: 10,
    fontSize: 14,
    background: '#fff',
    color: '#0f172a',
    cursor: 'pointer',
    fontFamily: 'Inter, sans-serif',
    appearance: 'none',
    paddingRight: 32,
    backgroundImage: 'url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'12\' height=\'12\' viewBox=\'0 0 24 24\' fill=\'none\' stroke=\'%2394a3b8\' stroke-width=\'2\'%3E%3Cpath d=\'M6 9l6 6 6-6\'/%3E%3C/svg%3E")',
    backgroundRepeat: 'no-repeat',
    backgroundPosition: 'right 12px center',
  },
  container: { padding: '0 48px 48px', maxWidth: 1440, margin: '0 auto' },
  kpiGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
    gap: 16,
    marginBottom: 32,
  },
  chartRow: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: 24,
    marginBottom: 32,
  },
  chartCard: {
    background: '#fff',
    border: '1px solid #e2e8f0',
    borderRadius: 16,
    padding: 24,
  },
  chartTitle: { fontSize: 15, fontWeight: 600, marginBottom: 20, color: '#0f172a' },
  tabs: { display: 'flex', gap: 6, marginBottom: 24 },
  tab: (active) => ({
    padding: '10px 24px',
    border: '1px solid ' + (active ? '#0f172a' : '#e2e8f0'),
    borderRadius: 10,
    background: active ? '#0f172a' : '#fff',
    color: active ? '#fff' : '#0f172a',
    cursor: 'pointer',
    fontSize: 14,
    fontWeight: 500,
    fontFamily: 'Inter, sans-serif',
    transition: 'all 0.15s',
  }),
  creativeGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
    gap: 20,
    marginBottom: 32,
  },
  tableWrap: {
    background: '#fff',
    border: '1px solid #e2e8f0',
    borderRadius: 16,
    padding: 24,
    overflowX: 'auto',
  },
  table: { width: '100%', borderCollapse: 'collapse', fontSize: 13 },
  th: {
    textAlign: 'left',
    padding: '12px 14px',
    borderBottom: '2px solid #e2e8f0',
    color: '#94a3b8',
    fontSize: 11,
    textTransform: 'uppercase',
    letterSpacing: '0.05em',
    fontWeight: 600,
  },
  td: {
    padding: '12px 14px',
    borderBottom: '1px solid #f1f5f9',
  },
  loading: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    height: '60vh',
    color: '#94a3b8',
    gap: 12,
    fontSize: 16,
  },
};

const CHART_COLORS = {
  spend: '#3b82f6',
  roas: '#22c55e',
  conversions: '#8b5cf6',
  costPerConv: '#ef4444',
  impressions: '#3b82f6',
  reach: '#a78bfa',
  ctr: '#f59e0b',
  cpc: '#ef4444',
};

function calcChange(a, b) {
  if (!b || b === 0) return null;
  return ((a - b) / b * 100).toFixed(1);
}

export default function App() {
  const [campaigns, setCampaigns] = useState([]);
  const [adsets, setAdsets] = useState([]);
  const [creatives, setCreatives] = useState([]);
  const [loading, setLoading] = useState(true);
  const [month, setMonth] = useState('all');
  const [compare, setCompare] = useState('');
  const [tab, setTab] = useState('creatives');

  useEffect(() => {
    Promise.all([fetchSheet('Campaigns'), fetchSheet('Ad Sets'), fetchSheet('Creatives')])
      .then(([c, a, cr]) => {
        setCampaigns(c);
        setAdsets(a);
        setCreatives(cr);
        setLoading(false);
      });
  }, []);

  const months = useMemo(() => [...new Set(campaigns.map(d => d.Monat))].sort(), [campaigns]);

  const filtered = useMemo(() => {
    const f = m => m === 'all' ? campaigns : campaigns.filter(d => d.Monat === m);
    return { campaigns: f(month), adsets: month === 'all' ? adsets : adsets.filter(d => d.Monat === month), creatives: month === 'all' ? creatives : creatives.filter(d => d.Monat === month) };
  }, [month, campaigns, adsets, creatives]);

  const current = useMemo(() => aggregate(filtered.campaigns), [filtered.campaigns]);
  const compareAgg = useMemo(() => compare ? aggregate(campaigns.filter(d => d.Monat === compare)) : null, [compare, campaigns]);

  const trendData = useMemo(() => months.map(m => {
    const agg = aggregate(campaigns.filter(d => d.Monat === m));
    return { month: m, ...agg };
  }), [months, campaigns]);

  if (loading) return (
    <div style={css.loading}>
      <Loader2 size={24} className="spin" style={{ animation: 'spin 1s linear infinite' }} />
      Dashboard lädt...
      <style>{`@keyframes spin { to { transform: rotate(360deg) } }`}</style>
    </div>
  );

  const kpis = [
    { label: 'Spend', value: fmt(current.spend, 'money'), change: compareAgg ? calcChange(current.spend, compareAgg.spend) : null },
    { label: 'Impressions', value: fmt(current.impressions, 'num'), change: compareAgg ? calcChange(current.impressions, compareAgg.impressions) : null },
    { label: 'Clicks', value: fmt(current.clicks, 'num'), change: compareAgg ? calcChange(current.clicks, compareAgg.clicks) : null },
    { label: 'CTR', value: fmt(current.ctr, 'pct'), change: compareAgg ? calcChange(current.ctr, compareAgg.ctr) : null },
    { label: 'CPM', value: fmt(current.cpm, 'money'), change: compareAgg ? calcChange(current.cpm, compareAgg.cpm) : null, invert: true },
    { label: 'CPC', value: fmt(current.cpc, 'money'), change: compareAgg ? calcChange(current.cpc, compareAgg.cpc) : null, invert: true },
    { label: 'Conversions', value: fmt(current.conversions, 'num'), change: compareAgg ? calcChange(current.conversions, compareAgg.conversions) : null },
    { label: 'Cost/Conv', value: fmt(current.costPerConv, 'money'), change: compareAgg ? calcChange(current.costPerConv, compareAgg.costPerConv) : null, invert: true },
    { label: 'ROAS', value: fmt(current.roas, 'x'), change: compareAgg ? calcChange(current.roas, compareAgg.roas) : null },
    { label: 'Reach', value: fmt(current.reach, 'num'), change: compareAgg ? calcChange(current.reach, compareAgg.reach) : null },
    { label: 'Frequency', value: current.frequency.toFixed(2), change: compareAgg ? calcChange(current.frequency, compareAgg.frequency) : null, invert: true },
  ];

  const topCreatives = [...filtered.creatives].sort((a, b) => Number(b.Spend || 0) - Number(a.Spend || 0)).slice(0, 24);
  const topCampaigns = [...filtered.campaigns].sort((a, b) => Number(b.Spend || 0) - Number(a.Spend || 0));
  const topAdsets = [...filtered.adsets].sort((a, b) => Number(b.Spend || 0) - Number(a.Spend || 0));

  const tooltipStyle = { contentStyle: { borderRadius: 10, border: '1px solid #e2e8f0', fontSize: 13 } };

  return (
    <>
      <div style={css.header}>
        <div>
          <div style={css.title}>Meta Ads Dashboard</div>
          <div style={css.subtitle}>Razeco UG — Performance Overview</div>
        </div>
        <div style={css.filters}>
          <select style={css.select} value={month} onChange={e => setMonth(e.target.value)}>
            <option value="all">Alle Monate</option>
            {months.map(m => <option key={m} value={m}>{m}</option>)}
          </select>
          <select style={css.select} value={compare} onChange={e => setCompare(e.target.value)}>
            <option value="">Vergleich: —</option>
            {months.map(m => <option key={m} value={m}>{m}</option>)}
          </select>
        </div>
      </div>

      <div style={css.container}>
        {/* KPIs */}
        <div style={css.kpiGrid}>
          {kpis.map(k => <KPICard key={k.label} {...k} />)}
        </div>

        {/* Charts Row 1 */}
        <div style={css.chartRow}>
          <div style={css.chartCard}>
            <div style={css.chartTitle}>Spend & ROAS</div>
            <ResponsiveContainer width="100%" height={280}>
              <ComposedChart data={trendData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="month" tick={{ fontSize: 12, fill: '#94a3b8' }} />
                <YAxis yAxisId="left" tick={{ fontSize: 12, fill: '#94a3b8' }} />
                <YAxis yAxisId="right" orientation="right" tick={{ fontSize: 12, fill: '#94a3b8' }} />
                <Tooltip {...tooltipStyle} />
                <Legend />
                <Bar yAxisId="left" dataKey="spend" name="Spend (€)" fill={CHART_COLORS.spend} radius={[6, 6, 0, 0]} />
                <Line yAxisId="right" dataKey="roas" name="ROAS" stroke={CHART_COLORS.roas} strokeWidth={2.5} dot={{ r: 4 }} />
              </ComposedChart>
            </ResponsiveContainer>
          </div>
          <div style={css.chartCard}>
            <div style={css.chartTitle}>Conversions & Cost/Conversion</div>
            <ResponsiveContainer width="100%" height={280}>
              <ComposedChart data={trendData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="month" tick={{ fontSize: 12, fill: '#94a3b8' }} />
                <YAxis yAxisId="left" tick={{ fontSize: 12, fill: '#94a3b8' }} />
                <YAxis yAxisId="right" orientation="right" tick={{ fontSize: 12, fill: '#94a3b8' }} />
                <Tooltip {...tooltipStyle} />
                <Legend />
                <Bar yAxisId="left" dataKey="conversions" name="Conversions" fill={CHART_COLORS.conversions} radius={[6, 6, 0, 0]} />
                <Line yAxisId="right" dataKey="costPerConv" name="Cost/Conv (€)" stroke={CHART_COLORS.costPerConv} strokeWidth={2.5} dot={{ r: 4 }} />
              </ComposedChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Charts Row 2 */}
        <div style={css.chartRow}>
          <div style={css.chartCard}>
            <div style={css.chartTitle}>Impressions & Reach</div>
            <ResponsiveContainer width="100%" height={280}>
              <LineChart data={trendData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="month" tick={{ fontSize: 12, fill: '#94a3b8' }} />
                <YAxis tick={{ fontSize: 12, fill: '#94a3b8' }} />
                <Tooltip {...tooltipStyle} />
                <Legend />
                <Line dataKey="impressions" name="Impressions" stroke={CHART_COLORS.impressions} strokeWidth={2.5} dot={{ r: 4 }} />
                <Line dataKey="reach" name="Reach" stroke={CHART_COLORS.reach} strokeWidth={2.5} dot={{ r: 4 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
          <div style={css.chartCard}>
            <div style={css.chartTitle}>CTR & CPC</div>
            <ResponsiveContainer width="100%" height={280}>
              <ComposedChart data={trendData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="month" tick={{ fontSize: 12, fill: '#94a3b8' }} />
                <YAxis yAxisId="left" tick={{ fontSize: 12, fill: '#94a3b8' }} />
                <YAxis yAxisId="right" orientation="right" tick={{ fontSize: 12, fill: '#94a3b8' }} />
                <Tooltip {...tooltipStyle} />
                <Legend />
                <Line yAxisId="left" dataKey="ctr" name="CTR (%)" stroke={CHART_COLORS.ctr} strokeWidth={2.5} dot={{ r: 4 }} />
                <Line yAxisId="right" dataKey="cpc" name="CPC (€)" stroke={CHART_COLORS.cpc} strokeWidth={2.5} dot={{ r: 4 }} />
              </ComposedChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Tabs */}
        <div style={css.tabs}>
          <button style={css.tab(tab === 'creatives')} onClick={() => setTab('creatives')}>
            <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}><Image size={14} /> Top Creatives</span>
          </button>
          <button style={css.tab(tab === 'campaigns')} onClick={() => setTab('campaigns')}>
            <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}><BarChart3 size={14} /> Campaigns</span>
          </button>
          <button style={css.tab(tab === 'adsets')} onClick={() => setTab('adsets')}>
            <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}><Table2 size={14} /> Ad Sets</span>
          </button>
        </div>

        {/* Creative Gallery */}
        {tab === 'creatives' && (
          <div style={css.creativeGrid}>
            {topCreatives.map((ad, i) => <CreativeCard key={i} ad={ad} />)}
          </div>
        )}

        {/* Campaign Table */}
        {tab === 'campaigns' && (
          <div style={css.tableWrap}>
            <table style={css.table}>
              <thead>
                <tr>
                  {['Campaign', 'Spend', 'Impressions', 'Clicks', 'CTR', 'CPM', 'Conversions', 'Cost/Conv', 'ROAS'].map(h => (
                    <th key={h} style={css.th}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {topCampaigns.map((c, i) => (
                  <tr key={i} onMouseEnter={e => e.currentTarget.style.background='#f8fafc'} onMouseLeave={e => e.currentTarget.style.background='transparent'}>
                    <td style={{ ...css.td, fontWeight: 500, maxWidth: 250, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{c['Campaign Name']}</td>
                    <td style={css.td}>{fmt(c.Spend, 'money')}</td>
                    <td style={css.td}>{fmt(c.Impressions, 'num')}</td>
                    <td style={css.td}>{fmt(c.Clicks, 'num')}</td>
                    <td style={css.td}>{fmt(c.CTR, 'pct')}</td>
                    <td style={css.td}>{fmt(c.CPM, 'money')}</td>
                    <td style={css.td}>{c.Conversions}</td>
                    <td style={css.td}>{fmt(c['Cost/Conversion'], 'money')}</td>
                    <td style={{ ...css.td, fontWeight: 600, color: Number(c.ROAS) >= 1 ? '#22c55e' : '#ef4444' }}>{fmt(c.ROAS, 'x')}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Ad Set Table */}
        {tab === 'adsets' && (
          <div style={css.tableWrap}>
            <table style={css.table}>
              <thead>
                <tr>
                  {['Ad Set', 'Campaign', 'Spend', 'Impressions', 'Clicks', 'CTR', 'CPM', 'Conversions', 'Cost/Conv'].map(h => (
                    <th key={h} style={css.th}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {topAdsets.map((c, i) => (
                  <tr key={i} onMouseEnter={e => e.currentTarget.style.background='#f8fafc'} onMouseLeave={e => e.currentTarget.style.background='transparent'}>
                    <td style={{ ...css.td, fontWeight: 500, maxWidth: 200, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{c['Ad Set Name']}</td>
                    <td style={{ ...css.td, maxWidth: 200, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{c['Campaign Name']}</td>
                    <td style={css.td}>{fmt(c.Spend, 'money')}</td>
                    <td style={css.td}>{fmt(c.Impressions, 'num')}</td>
                    <td style={css.td}>{fmt(c.Clicks, 'num')}</td>
                    <td style={css.td}>{fmt(c.CTR, 'pct')}</td>
                    <td style={css.td}>{fmt(c.CPM, 'money')}</td>
                    <td style={css.td}>{c.Conversions}</td>
                    <td style={css.td}>{fmt(c['Cost/Conversion'], 'money')}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </>
  );
}
