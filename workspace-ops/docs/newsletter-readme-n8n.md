# Newsletter-Automatisierung mit n8n

Wir haben einen vollständigen n8n Workflow für die Newsletter-Automatisierung erstellt, der das verbesserte Python-Script integriert und zusätzliche Funktionen wie Fehlerbehandlung und Benachrichtigungen bietet.

## Vorteile des n8n-Ansatzes

1. **Visuelle Übersicht**: Einfache Visualisierung des kompletten Prozesses
2. **Fehlerbehandlung**: Automatische Benachrichtigungen bei Problemen
3. **Bedingte Verzweigungen**: IF-Logik für verschiedene Szenarien
4. **Integrations-Hub**: Verbindung von Airtable, Notion, Klaviyo und Benachrichtigungssystemen
5. **Kein SSH/Cron nötig**: Alles läuft über die n8n-Instanz

## Workflow-Komponenten

Der Workflow umfasst folgende Schritte:

1. **Zeitplan-Trigger**: Jeden Montag um 8:30 Uhr
2. **Airtable-Integration**: Holt aktive Kunden mit Klaviyo-API-Keys
3. **Notion-Abfrage**: Prüft nach Newsletter-Themen für die aktuelle Woche
4. **Themen-Verarbeitung**: Filtert und bereitet Themen auf
5. **Bedingte Ausführung**: Verzweigt je nachdem, ob Themen gefunden wurden
6. **Script-Ausführung**: Führt das verbesserte Python-Script aus
7. **Ergebnis-Analyse**: Verarbeitet die Script-Ausgabe
8. **Benachrichtigungen**: Sendet Erfolgs-, Fehler- oder "Keine Themen"-Nachrichten

## Installation

1. Öffne die n8n-Instanz (http://n8n.adsdrop.de)
2. Erstelle einen neuen Workflow
3. Importiere die JSON-Definition aus dem Dokumentationsordner oder erstelle die Nodes manuell
4. Aktiviere den Workflow im n8n-UI

## Wichtig: Webhook-Aktivierung

Der wichtigste Schritt: **Der Workflow muss über die UI aktiviert werden**. Die reine API-Aktivierung reicht bei n8n-Workflows nicht aus, insbesondere bei Webhooks. Stelle sicher, dass der Toggle-Schalter im UI eingeschaltet ist.

## Zusätzliche Features

Im Vergleich zum reinen Cron-Job bietet der n8n-Workflow zusätzlich:

1. **Intelligente Themenprüfung**: Prüft vor der Ausführung, ob überhaupt Themen für die aktuelle Woche existieren
2. **Admin-Links**: Benachrichtigungen enthalten direkte Links zu den erstellten Kampagnen
3. **Fehlerbehandlung**: Detaillierte Fehlerberichte bei Problemen
4. **Kein Telegram-Token nötig**: Authentifizierung wird von n8n übernommen

## Erweiterungsmöglichkeiten

Der Workflow kann leicht erweitert werden:

1. **A/B-Testing**: Zusätzlicher Node für verschiedene Betreffzeilen
2. **Performance-Tracking**: Integration mit Google Analytics oder anderen Tracking-Tools
3. **Feedback-Loop**: Automatisches Erfassen von Öffnungsraten und Klicks
4. **Multi-Kanal**: Erweiterung um zusätzliche Kanäle wie SMS oder Social Media

## Workflow-Diagramm

Ein visuelles Diagramm des Workflows findest du in der Datei `n8n-newsletter-diagramm.excalidraw`.

---

Die vollständige technische Dokumentation zum n8n-Workflow findest du in `n8n-newsletter-workflow.md`.