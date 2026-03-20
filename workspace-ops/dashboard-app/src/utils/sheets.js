const SHEET_ID = '1XTMtZwPRQVR7pRZv2ZZQC_pC5_61JIhkclOsCn1uESA';

export async function fetchSheet(tab) {
  const url = `https://docs.google.com/spreadsheets/d/${SHEET_ID}/gviz/tq?tqx=out:json&sheet=${encodeURIComponent(tab)}`;
  const resp = await fetch(url);
  const text = await resp.text();
  const json = JSON.parse(text.match(/google\.visualization\.Query\.setResponse\((.*)\)/s)[1]);
  const cols = json.table.cols.map(c => c.label);
  return json.table.rows.map(r => {
    const obj = {};
    r.c.forEach((cell, i) => {
      obj[cols[i]] = cell ? (cell.v ?? '') : '';
    });
    return obj;
  });
}

export function fmt(n, type) {
  const v = Number(n) || 0;
  switch (type) {
    case 'money': return '€' + v.toLocaleString('de-DE', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    case 'pct': return v.toFixed(2) + '%';
    case 'num': return v.toLocaleString('de-DE');
    case 'x': return v.toFixed(2) + 'x';
    default: return String(n);
  }
}

export function aggregate(data) {
  const spend = data.reduce((s, d) => s + Number(d.Spend || 0), 0);
  const impressions = data.reduce((s, d) => s + Number(d.Impressions || 0), 0);
  const reach = data.reduce((s, d) => s + Number(d.Reach || 0), 0);
  const clicks = data.reduce((s, d) => s + Number(d.Clicks || 0), 0);
  const conversions = data.reduce((s, d) => s + Number(d.Conversions || 0), 0);
  const revenueWeighted = data.reduce((s, d) => s + Number(d.ROAS || 0) * Number(d.Spend || 0), 0);
  return {
    spend, impressions, reach, clicks, conversions,
    ctr: impressions > 0 ? (clicks / impressions * 100) : 0,
    cpm: impressions > 0 ? (spend / impressions * 1000) : 0,
    cpc: clicks > 0 ? (spend / clicks) : 0,
    costPerConv: conversions > 0 ? (spend / conversions) : 0,
    roas: spend > 0 ? (revenueWeighted / spend) : 0,
    frequency: reach > 0 ? (impressions / reach) : 0,
  };
}
