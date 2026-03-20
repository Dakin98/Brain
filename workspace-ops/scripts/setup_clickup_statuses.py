#!/usr/bin/env python3
"""
Content Engine - Complete Status Setup Guide
Dieses Script erstellt alle benötigten Status für den Content Ideas Workflow
"""

print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║           🎬 CONTENT ENGINE - STATUS SETUP GUIDE                          ║
╚═══════════════════════════════════════════════════════════════════════════╝

Da die ClickUp API Status-Updates nicht zuverlässig unterstützt,
musst du diese manuell im ClickUp UI erstellen.

═══════════════════════════════════════════════════════════════════════════
📋 SCHRITT 1: Öffne die Liste
═══════════════════════════════════════════════════════════════════════════

1. Gehe zu: https://app.clickup.com/9006104573/v/li/901521521000
   (Growth Space → 🎬 Content Engine → 💡 Content Ideas)

2. Klicke auf die drei Punkte "..." (oben rechts im Listen-Header)

3. Wähle: "Customize" → "Statuses"

═══════════════════════════════════════════════════════════════════════════
📊 SCHRITT 2: Erstelle diese 7 Status (in dieser Reihenfolge)
═══════════════════════════════════════════════════════════════════════════

┌──────────────────────┬────────────────┬──────────┬─────────────────────────┐
│ Status Name          │ Farbe          │ Type     │ Zweck                   │
├──────────────────────┼────────────────┼──────────┼─────────────────────────┤
│ 1. Idea              │ #6B7280 (Grau) │ Open     │ Rohe Idee, Backlog      │
│ 2. Researching       │ #F59E0B (Gelb) │ Custom   │ Recherche läuft         │
│ 3. Ready             │ #3B82F6 (Blau) │ Custom   │ Bereit für Generation   │
│ 4. 🤖 Claude Generate│ #7C3AED (Lila) │ Custom   │ ⭐ AUTOMATION TRIGGER   │
│ 5. Content Generated │ #10B981 (Grün) │ Custom   │ Content erstellt        │
│ 6. Scheduled         │ #F97316 (Oran) │ Custom   │ Im Kalender eingeplant  │
│ 7. Archived          │ #9CA3AF (Hell) │ Closed   │ Published/Verworfen     │
└──────────────────────┴────────────────┴──────────┴─────────────────────────┘

═══════════════════════════════════════════════════════════════════════════
📸 SCHRITT 3: So erstellst du einen Status
═══════════════════════════════════════════════════════════════════════════

In ClickUp:
1. Klicke "+ Add Status"
2. Name: (siehe Tabelle oben)
3. Farbe: Klicke auf den Farbkreis → "Custom" → Hex Code eingeben
4. Type: 
   - "Open" für Idea
   - "Custom" für alle anderen
   - "Closed" für Archived
5. Klicke "Save"

═══════════════════════════════════════════════════════════════════════════
🔄 SCHRITT 4: Status-Reihenfolge anpassen
═══════════════════════════════════════════════════════════════════════════

Ziehe die Status per Drag & Drop in diese Reihenfolge:

Idea → Researching → Ready → 🤖 Claude Generate → Content Generated → Scheduled → Archived

═══════════════════════════════════════════════════════════════════════════
✅ SCHRITT 5: Testen
═══════════════════════════════════════════════════════════════════════════

1. Erstelle einen Test-Task
2. Setze alle Custom Fields:
   - Content Pillar: Meta Ads Tutorials
   - Target Audience: E-Com Brands  
   - Keywords: meta ads, facebook ads
   - Priority Score: 8

3. Ändere Status zu: "🤖 Claude Generate"

4. Warte 5 Minuten (Cronjob läuft alle 5 Min)

5. Prüfe die Kommentare am Task

═══════════════════════════════════════════════════════════════════════════
🔧 TROUBLESHOOTING
═══════════════════════════════════════════════════════════════════════════

Falls die Automation nicht triggert:
→ Manuelles Ausführen:
   python3 scripts/content_engine_generator_v2.py --task-id "TASK_ID"

→ Logs checken:
   tail -f /tmp/content_engine_cron.log

→ Cronjob prüfen:
   crontab -l | grep content_engine

═══════════════════════════════════════════════════════════════════════════
📚 WORKFLOW ÜBERSICHT
═══════════════════════════════════════════════════════════════════════════

Montag 9 Uhr:
  ├─ Content Ideas öffnen
  ├─ Idee auswählen (Priority Score)
  ├─ Status: "🤖 Claude Generate"
  └─ Warten (max 5 Min)

Nach Generation:
  ├─ YouTube Script reviewen
  ├─ LinkedIn Posts anpassen  
  ├─ Newsletter finalisieren
  └─ Follow-Up Tasks erscheinen automatisch

Publishing:
  ├─ Dienstag: LinkedIn Long-Form
  ├─ Mittwoch: Short #1
  ├─ Donnerstag: LinkedIn Carousel + Newsletter
  ├─ Freitag: LinkedIn Short + Short #2
  └─ Sonntag: YouTube Video + Short #3

═══════════════════════════════════════════════════════════════════════════

🎬 Fertig! Deine Content Engine ist bereit.

Fragen? Sag einfach Bescheid.
""")
