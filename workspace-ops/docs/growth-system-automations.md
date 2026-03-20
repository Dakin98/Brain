# Growth System — Automatisierungen

> Alle Automations für Content Engine + Outbound Engine

---

## Übersicht

| # | Automation | Trigger | Priorität |
|---|-----------|---------|-----------|
| 1 | YouTube → Reels Auto-Tasks | YouTube Status = "Published" | 🔴 Hoch |
| 2 | YouTube → LinkedIn Auto-Task | YouTube Status = "Published" | 🔴 Hoch |
| 3 | YouTube → Newsletter Reminder | YouTube Status = "Published" | 🟡 Mittel |
| 4 | YouTube → Distribution Tracker | YouTube Status = "Published" | 🟡 Mittel |
| 5 | Reply Alert → Meeting Task | Reply Type = "Interested" | 🔴 Hoch |
| 6 | Reply → CRM Prospect | Meeting Booked | 🔴 Hoch |
| 7 | Weekly Content Report | Montag 9:00 | 🟡 Mittel |
| 8 | Weekly Outbound Report | Montag 9:00 | 🟡 Mittel |
| 9 | Campaign Checklist Auto-Create | Neue Campaign erstellt | 🟢 Nice-to-have |

---

## Automation 1: YouTube → Reels Auto-Tasks

**Script-Name:** `youtube-to-reels.js`

**Trigger:** YouTube Pipeline Task → Status wechselt zu "Published"

**Action:** Erstelle 3 neue Tasks in "Reels Pipeline"

**Pseudo-Code:**
```javascript
// Trigger: Webhook on YouTube Pipeline status change to "Published"
async function youtubeToReels(youtubeTask) {
  const REELS_LIST_ID = "<reels-pipeline-list-id>";
  
  for (let i = 1; i <= 3; i++) {
    await clickup.createTask(REELS_LIST_ID, {
      name: `Reel ${i}/3 — ${youtubeTask.name}`,
      description: `Erstellt aus: ${youtubeTask.url}\n\nSource Video: ${youtubeTask.name}`,
      status: "Identified",
      custom_fields: [
        { id: "<source-video-field-id>", value: youtubeTask.id },
        { id: "<platform-field-id>", value: "Alle" }  // dropdown index
      ],
      // Copy due date + 3/5/7 days for staggered posting
      due_date: addDays(youtubeTask.custom_fields["publish_date"], i * 2)
    });
  }
  
  // Update YouTube task: Reels Created = 3
  await clickup.updateCustomField(youtubeTask.id, "<reels-created-field-id>", 3);
}
```

**API Calls:**
```bash
# 1. Create Webhook for YouTube Pipeline list
curl -X POST "https://api.clickup.com/api/v2/team/${TEAM_ID}/webhook" \
  -H "Authorization: ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint": "https://your-server.com/webhooks/youtube-published",
    "events": ["taskStatusUpdated"],
    "space_id": 90040244466
  }'

# 2. Create Task in Reels Pipeline (called 3x)
curl -X POST "https://api.clickup.com/api/v2/list/${REELS_LIST_ID}/task" \
  -H "Authorization: ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Reel 1/3 — Video Title",
    "status": "Identified",
    "due_date": 1709251200000,
    "custom_fields": [...]
  }'
```

---

## Automation 2: YouTube → LinkedIn Auto-Task

**Script-Name:** `youtube-to-linkedin.js`

**Trigger:** YouTube Pipeline Task → Status = "Published"

**Action:** 1 neuer Task in "LinkedIn Pipeline"

**Pseudo-Code:**
```javascript
async function youtubeToLinkedIn(youtubeTask) {
  const LINKEDIN_LIST_ID = "<linkedin-pipeline-list-id>";
  
  const videoUrl = youtubeTask.custom_fields["youtube_url"];
  const pillar = youtubeTask.custom_fields["content_pillar"];
  
  await clickup.createTask(LINKEDIN_LIST_ID, {
    name: `LinkedIn Post — ${youtubeTask.name}`,
    description: `Neues YouTube Video veröffentlicht!\n\n` +
      `Video: ${videoUrl}\n\n` +
      `Aufgabe: Schreibe einen LinkedIn Post der das Video promoted.\n` +
      `Optionen: Key Takeaway, Behind the Scenes, Kontroverse These`,
    status: "Draft",
    due_date: addDays(youtubeTask.custom_fields["publish_date"], 1),
    custom_fields: [
      { id: "<post-type-field-id>", value: "Text" },
      { id: "<pillar-field-id>", value: pillar },
      { id: "<source-field-id>", value: youtubeTask.id }
    ]
  });
}
```

---

## Automation 3: YouTube → Newsletter Reminder

**Script-Name:** `youtube-to-newsletter.js`

**Trigger:** YouTube Pipeline Task → Status = "Published" (prüfe ob Donnerstag oder später in der Woche)

**Action:** Erstelle Newsletter Task falls diese Woche noch keiner existiert

**Pseudo-Code:**
```javascript
async function youtubeToNewsletter(youtubeTask) {
  const NEWSLETTER_LIST_ID = "<newsletter-pipeline-list-id>";
  
  // Check: Gibt es diese Woche schon einen Newsletter Task?
  const thisWeekStart = getMonday(new Date());
  const thisWeekEnd = addDays(thisWeekStart, 7);
  
  const existingTasks = await clickup.getTasks(NEWSLETTER_LIST_ID, {
    due_date_gt: thisWeekStart.getTime(),
    due_date_lt: thisWeekEnd.getTime()
  });
  
  if (existingTasks.length === 0) {
    // Nächsten Donnerstag als Send-Date
    const nextThursday = getNextThursday();
    
    await clickup.createTask(NEWSLETTER_LIST_ID, {
      name: `Newsletter KW${getWeekNumber()} — ${youtubeTask.name}`,
      description: `Basierend auf dem neuen YouTube Video:\n${youtubeTask.name}\n\n` +
        `Checklist:\n- [ ] Subject Line\n- [ ] Content schreiben\n- [ ] Klaviyo Setup\n- [ ] Test senden\n- [ ] Schedule`,
      status: "Planning",
      due_date: nextThursday.getTime(),
      custom_fields: [
        { id: "<source-field-id>", value: youtubeTask.id },
        { id: "<pillar-field-id>", value: youtubeTask.custom_fields["content_pillar"] }
      ]
    });
  }
}
```

---

## Automation 4: YouTube → Distribution Tracker

**Script-Name:** `youtube-to-distribution.js`

**Trigger:** YouTube Pipeline Task → Status = "Published"

**Action:** Erstelle Distribution Tasks für jeden Kanal

**Pseudo-Code:**
```javascript
async function createDistributionTasks(youtubeTask) {
  const DIST_LIST_ID = "<distribution-tracker-list-id>";
  const channels = ["Reels", "LinkedIn", "Newsletter", "Twitter"];
  
  for (const channel of channels) {
    await clickup.createTask(DIST_LIST_ID, {
      name: `${channel} — ${youtubeTask.name}`,
      status: "Pending",
      custom_fields: [
        { id: "<source-field-id>", value: youtubeTask.id },
        { id: "<channel-field-id>", value: channel }
      ]
    });
  }
}
```

---

## Automation 5: Reply Alert → Meeting Task

**Script-Name:** `reply-to-meeting.js`

**Trigger:** Reply Management Task → Reply Type = "Interested"

**Action:** Erstelle Meeting-Booking Subtask + Benachrichtigung

**Pseudo-Code:**
```javascript
async function replyToMeeting(replyTask) {
  // 1. Create subtask for meeting booking
  await clickup.createTask(replyTask.list.id, {
    name: `📞 Meeting buchen — ${replyTask.custom_fields["lead_name"]}`,
    parent: replyTask.id,
    description: `Lead hat Interesse gezeigt!\n\n` +
      `Lead: ${replyTask.custom_fields["lead_name"]}\n` +
      `Company: ${replyTask.custom_fields["company"]}\n` +
      `Email: ${replyTask.custom_fields["lead_email"]}\n\n` +
      `Reply:\n${replyTask.custom_fields["reply_snippet"]}\n\n` +
      `→ Calendly Link senden oder direkt Termin vorschlagen`,
    status: "New Reply",
    priority: 1,  // Urgent
    due_date: addHours(Date.now(), 24)  // Innerhalb 24h antworten
  });

  // 2. Update reply task status
  await clickup.updateTask(replyTask.id, { status: "Meeting Booked" });
}
```

---

## Automation 6: Reply → CRM Prospect

**Script-Name:** `reply-to-crm.js`

**Trigger:** Reply Management Task → Status = "Meeting Booked"

**Action:** Erstelle CRM Task als Prospect

**Pseudo-Code:**
```javascript
async function replyToCRM(replyTask) {
  const CRM_LIST_ID = "901506196069";
  
  await clickup.createTask(CRM_LIST_ID, {
    name: replyTask.custom_fields["company"] || replyTask.custom_fields["lead_name"],
    status: "quali call - terminiert",
    custom_fields: [
      { id: "<email-field-id>", value: replyTask.custom_fields["lead_email"] },
      { id: "<firma-field-id>", value: replyTask.custom_fields["company"] },
      { id: "<quelle-field-id>", value: "Cold Email" },  // dropdown
      // Meeting Date → Due Date
    ],
    due_date: replyTask.custom_fields["meeting_date"]
  });
  
  // Link CRM task back to reply
  await clickup.updateCustomField(replyTask.id, "<crm-task-field-id>", newCrmTask.id);
}
```

---

## Automation 7: Weekly Content Report

**Script-Name:** `weekly-content-report.js`

**Trigger:** Cron — Montag 09:00

**Action:** Sammle Metriken, erstelle Report Task

**Pseudo-Code:**
```javascript
async function weeklyContentReport() {
  const now = new Date();
  const weekStart = getMonday(addDays(now, -7));
  const weekEnd = addDays(weekStart, 7);
  
  // 1. YouTube: Published videos this week
  const ytTasks = await clickup.getTasks(YOUTUBE_LIST_ID, {
    statuses: ["Published", "Analyzing"],
    due_date_gt: weekStart.getTime(),
    due_date_lt: weekEnd.getTime()
  });
  
  const ytStats = {
    videosPublished: ytTasks.length,
    totalViews: sum(ytTasks, "views_7d"),
    avgWatchTime: avg(ytTasks, "watch_time"),
    avgCTR: avg(ytTasks, "ctr"),
    subsGained: sum(ytTasks, "subscriber_delta")
  };
  
  // 2. Reels
  const reelTasks = await clickup.getTasks(REELS_LIST_ID, {
    statuses: ["Published"],
    due_date_gt: weekStart.getTime(),
    due_date_lt: weekEnd.getTime()
  });
  
  const reelStats = {
    reelsPublished: reelTasks.length,
    totalViews: sum(reelTasks, "views"),
    totalSaves: sum(reelTasks, "saves")
  };
  
  // 3. LinkedIn
  const liTasks = await clickup.getTasks(LINKEDIN_LIST_ID, {
    statuses: ["Published"],
    due_date_gt: weekStart.getTime(),
    due_date_lt: weekEnd.getTime()
  });
  
  const liStats = {
    postsPublished: liTasks.length,
    totalImpressions: sum(liTasks, "impressions"),
    avgEngagement: avg(liTasks, "engagement_rate")
  };
  
  // 4. Newsletter
  const nlTasks = await clickup.getTasks(NEWSLETTER_LIST_ID, {
    statuses: ["Sent"],
    due_date_gt: weekStart.getTime(),
    due_date_lt: weekEnd.getTime()
  });
  
  const nlStats = {
    sent: nlTasks.length,
    avgOpenRate: avg(nlTasks, "open_rate"),
    avgClickRate: avg(nlTasks, "click_rate")
  };
  
  // 5. Create report task
  const report = `# Content Report KW${getWeekNumber(weekStart)}

## YouTube
- Videos: ${ytStats.videosPublished}
- Views: ${ytStats.totalViews}
- Avg Watch Time: ${ytStats.avgWatchTime}h
- Avg CTR: ${ytStats.avgCTR}%
- New Subscribers: ${ytStats.subsGained}

## Reels
- Published: ${reelStats.reelsPublished}
- Total Views: ${reelStats.totalViews}
- Total Saves: ${reelStats.totalSaves}

## LinkedIn
- Posts: ${liStats.postsPublished}
- Impressions: ${liStats.totalImpressions}
- Avg Engagement: ${liStats.avgEngagement}%

## Newsletter
- Sent: ${nlStats.sent}
- Avg Open Rate: ${nlStats.avgOpenRate}%
- Avg Click Rate: ${nlStats.avgClickRate}%`;

  // Create in a "Reports" list or as comment
  console.log(report);
}
```

---

## Automation 8: Weekly Outbound Report

**Script-Name:** `weekly-outbound-report.js`

**Trigger:** Cron — Montag 09:00

**Pseudo-Code:**
```javascript
async function weeklyOutboundReport() {
  // 1. Active campaigns
  const campaigns = await clickup.getTasks(CAMPAIGNS_LIST_ID, {
    statuses: ["Active"]
  });
  
  const campaignStats = campaigns.map(c => ({
    name: c.name,
    sent: c.custom_fields["emails_sent"],
    openRate: c.custom_fields["open_rate"],
    replyRate: c.custom_fields["reply_rate"],
    meetings: c.custom_fields["meetings_booked"]
  }));
  
  // 2. Replies this week
  const replies = await clickup.getTasks(REPLY_LIST_ID, {
    date_created_gt: weekStart.getTime()
  });
  
  const replyBreakdown = {
    total: replies.length,
    interested: replies.filter(r => r.custom_fields["reply_type"] === "Interested").length,
    notInterested: replies.filter(r => r.custom_fields["reply_type"] === "Not Interested").length,
    ooo: replies.filter(r => r.custom_fields["reply_type"] === "OOO").length,
    meetingsBooked: replies.filter(r => r.status === "Meeting Booked").length
  };
  
  // 3. Domain health
  const domains = await clickup.getTasks(DOMAIN_LIST_ID);
  const domainHealth = domains.map(d => ({
    domain: d.custom_fields["domain"],
    health: d.custom_fields["health_score"]
  }));
  
  const report = `# Outbound Report KW${getWeekNumber()}
  
## Active Campaigns: ${campaigns.length}
${campaignStats.map(c => `- ${c.name}: ${c.sent} sent, ${c.openRate}% open, ${c.replyRate}% reply, ${c.meetings} meetings`).join('\n')}

## Replies This Week: ${replyBreakdown.total}
- Interested: ${replyBreakdown.interested}
- Not Interested: ${replyBreakdown.notInterested}
- OOO: ${replyBreakdown.ooo}
- Meetings Booked: ${replyBreakdown.meetingsBooked}

## Domain Health
${domainHealth.map(d => `- ${d.domain}: ${d.health}%`).join('\n')}`;

  console.log(report);
}
```

---

## Automation 9: Campaign Checklist Auto-Create

**Script-Name:** `campaign-auto-checklist.js`

**Trigger:** Neuer Task in Campaigns Liste erstellt

**Action:** Erstelle Standard-Subtasks

**Pseudo-Code:**
```javascript
async function campaignAutoChecklist(campaignTask) {
  const subtasks = [
    { name: "ICP & Segment definieren", due_offset: 0 },
    { name: "Lead-Liste in Apollo erstellen", due_offset: 1 },
    { name: "Lead-Liste exportieren & cleanen", due_offset: 1 },
    { name: "Sequence auswählen & personalisieren", due_offset: 2 },
    { name: "Campaign im Tool aufsetzen", due_offset: 2 },
    { name: "Test-Mails senden & prüfen", due_offset: 3 },
    { name: "Campaign starten", due_offset: 3 },
    { name: "Tag 3 Check: Open Rates", due_offset: 6 },
    { name: "Tag 7 Check: Reply Handling", due_offset: 10 },
    { name: "Campaign Review & Learnings", due_offset: 17 }
  ];
  
  for (const sub of subtasks) {
    await clickup.createTask(campaignTask.list.id, {
      name: sub.name,
      parent: campaignTask.id,
      due_date: addDays(campaignTask.start_date || Date.now(), sub.due_offset)
    });
  }
}
```

---

## Technische Implementierung

### Option A: ClickUp Native Automations (Empfohlen für Start)
- ClickUp hat eingebaute Automations: "When status changes → Create task"
- Reicht für Automations 1-6
- **Kein Code nötig**, alles in der ClickUp UI konfigurierbar
- Limitation: Keine API-Calls, kein Daten-Aggregation

### Option B: Node.js Scripts mit Webhooks (Für Reports)
- Webhooks für Trigger
- Node.js Scripts auf Server (z.B. Railway, Vercel Cron)
- Nötig für Automation 7 + 8 (Weekly Reports)

### Option C: Make.com / Zapier (Mittelweg)
- Visueller Builder für komplexere Flows
- Gut für Apollo → ClickUp Integration
- Kostet ~$20/Monat

### Empfehlung

| Phase | Approach |
|-------|----------|
| Woche 1-2 | ClickUp Native Automations für alles was geht |
| Woche 3 | Node.js Scripts für Weekly Reports |
| Woche 4+ | Make.com nur falls nötig für Tool-Integrationen |
