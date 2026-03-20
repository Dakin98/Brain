# ⚡ Outbound Quick Reference

## One-Pager für tägliche Nutzung

---

## 🎯 DIE 4 PHASEN

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   LEADS     │ →  │  SEQUENCE   │ →  │   LAUNCH    │ →  │   REPLIES   │
│   (10min)   │    │   (20min)   │    │   (10min)   │    │  (ongoing)  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
      │                   │                   │                   │
  ClickUp:            ClickUp:            ClickUp:            ClickUp:
  Lead Lists          Sequences           Campaigns           Reply Mgmt
      │                   │                   │                   │
  Apollo:             Template:           Apollo:             Gmail/Apollo:
  Search              5-Step Flow         Schedule            Respond
```

---

## 📝 SEQUENZ TEMPLATE (Copy-Paste)

### Subject Lines (3 Varianten)
```
V1: {{company}} + Meta Ads Question
V2: Quick question about {{company}}  
V3: Idea for {{company}}
```

### Email 1 (Cold Intro)
```
Hi {{first_name}},

Saw {{company}} is scaling fast in the DACH market. 

Quick question: Are you currently testing any new creative angles for your Meta Ads?

Reason I ask: We just helped [Similar Company] increase their ROAS by 40% with a specific video hook.

Worth a 5-min chat?

Best,
Deniz
```

### Email 2 (Value)
```
Hi {{first_name}},

Quick follow-up. I put together a 2-min Loom showing exactly how [Similar Company] structured their winning creative.

The key: They stopped selling the product and started selling the transformation.

Want me to send the full case study?

Deniz
```

### Email 3 (Social Proof)
```
Hi {{first_name}},

Here's the case study: [LINK]

Key results:
• 40% ROAS increase
• 25% lower CAC  
• 3 winning creatives

Open to a quick call to see if this works for {{company}}?

Deniz
```

### Email 4 (Soft Breakup)
```
Hi {{first_name}},

I don't want to keep emailing if there's no interest.

Should I close your file or is Meta Ads optimization still on your radar?

Either way, all good.

Deniz
```

### Email 5 (Final)
```
{{first_name}},

This is my last email. If you're not interested, I understand.

If you change your mind, just reply "interested" and I'll send the case study.

All the best,
Deniz
```

---

## 🏷️ REPLY KATEGORIEN

| Emoji | Type | Action | Priority |
|-------|------|--------|----------|
| 🔥 | Interested | Send Calendar Link | 🔴 High |
| ❓ | Question | Answer + CTA | 🟡 Normal |
| ❌ | Not Interested | Archive | 🟢 Low |
| 🏖️ | OOO | Wait 1 week | 🟢 Low |
| 🔗 | Referral | Ask for Intro | 🔴 High |

---

## 📊 BENCHMARKS

### Daily Targets
- **40 Emails sent** (per account)
- **2-3 Replies** expected
- **1 Interested** per day (Ziel)

### Weekly Targets
- **200-400 Leads** neue Suche
- **10-15 Replies** insgesamt
- **3-5 Meetings** gebucht

### Success Metrics
| Metric | Good | Bad |
|--------|------|-----|
| Open Rate | > 50% | < 35% |
| Reply Rate | > 5% | < 3% |
| Meeting Rate | > 1% | < 0.5% |

---

## ⚡ DAILY WORKFLOW (15 Min)

### Morning (9 Uhr)
```
☐ 1. Check Reply Management → Neue Antworten kategorisieren (5min)
☐ 2. Interested Replies → Kalender-Link senden (5min)
☐ 3. Campaign Health → Daily Limit erreicht? (2min)
☐ 4. Domain Health → Alle Accounts grün? (3min)
```

### Afternoon (optional)
```
☐ Neue Leads suchen (wenn < 200 in Pipeline)
☐ Sequences optimieren (basierend auf Replies)
```

---

## 🛠️ COMMANDS

### Lead Search
```bash
cd ~/.openclaw/workspace/scripts
./apollo-lead-search.sh "[TASK_ID]" "[ICP]" [COUNT]
```

### Weekly Report
```bash
./weekly-outbound-report.sh
```

### Reply Import
```bash
./apollo-reply-sync.sh replies.csv
```

---

## 🚨 QUICK FIXES

### Keine Replies?
→ Subject Lines ändern (mehr Curiosity)

### Hohe Bounce Rate?
→ Leads validieren (nur verified emails)

### Spam Folder?
→ SPF/DKIM checken, 40 Emails/Tag Limit

### Viele "Not Interested"?
→ ICP strenger filtern, früher qualifizieren

---

## 🔗 LINKS

**ClickUp:**
- Campaigns: https://app.clickup.com/901521519128
- Lead Lists: https://app.clickup.com/901521519130
- Reply Mgmt: https://app.clickup.com/901521519132

**Tools:**
- Apollo: https://app.apollo.io
- Gmail: https://mail.google.com

---

**Print this out and keep it handy!** 📋
