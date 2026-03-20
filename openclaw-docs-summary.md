# OpenClaw Dokumentation – Strukturierte Zusammenfassung

> Erstellt am 2026-03-09 basierend auf dem Quellcode unter `/opt/openclaw`

---

## 1. Was ist OpenClaw?

OpenClaw ist ein **selbst-gehostetes Multi-Channel-Gateway für KI-Agenten**. Es verbindet Chat-Apps (WhatsApp, Telegram, Discord, iMessage, Slack, Signal u.v.m.) mit KI-Coding-Agenten wie Pi. Man betreibt einen einzelnen Gateway-Prozess auf dem eigenen Rechner oder Server – er wird zur Brücke zwischen Messaging-Apps und einem immer verfügbaren KI-Assistenten.

**Zielgruppe:** Entwickler und Power-User, die einen persönlichen KI-Assistenten wollen, den sie von überall anschreiben können – ohne Kontrolle über ihre Daten abzugeben.

**Kerneigenschaften:**
- **Self-hosted**: Läuft auf eigener Hardware, eigene Regeln
- **Multi-Channel**: Ein Gateway bedient WhatsApp, Telegram, Discord und mehr gleichzeitig
- **Agent-native**: Gebaut für Coding-Agenten mit Tool-Use, Sessions, Memory und Multi-Agent-Routing
- **Open Source**: MIT-Lizenz, Community-driven
- **TypeScript**: Hauptsächlich ein Orchestrierungssystem (Prompts, Tools, Protokolle, Integrationen)

**Vorgeschichte:** Warelay → Clawdbot → Moltbot → OpenClaw

---

## 2. Kernfeatures

### Channels (Messaging-Kanäle)
- **Nativ eingebaut:** WhatsApp (Baileys), Telegram (grammY), Discord (discord.js), Slack, Signal, iMessage (macOS), Google Chat, IRC, LINE, Nostr, Twitch
- **Als Plugins:** Mattermost, MS Teams, Matrix, Nextcloud Talk, Zalo, Feishu, Synology Chat
- Broadcast-Gruppen, Gruppenachrichten mit Mention-Gating

### Multi-Agent Routing
- Mehrere isolierte Agenten in einem Gateway (je mit eigenem Workspace, Sessions, Auth-Profilen)
- Bindings routen eingehende Nachrichten zum richtigen Agenten
- DM-Split: verschiedene WhatsApp-DMs an verschiedene Agenten (eine Nummer)
- Per-Agent Personas über `SOUL.md`, `AGENTS.md`, `USER.md`

### Session-Management
- DM-Scopes: `main` | `per-peer` | `per-channel-peer` | `per-account-channel-peer`
- Thread-Bindings (Discord: `/focus`, `/unfocus`)
- Auto-Reset: daily, idle-basiert
- Session-Compaction für lange Konversationen

### Media
- Bilder, Audio, Dokumente senden und empfangen
- Sprachnotiz-Transkription
- Media-Pipeline für Verarbeitung

### Tools & Skills
- **AgentSkills-kompatibles** Skill-System (SKILL.md mit YAML-Frontmatter)
- Skill-Quellen: Bundled → `~/.openclaw/skills` → `<workspace>/skills`
- **ClawHub** (clawhub.com): Öffentliches Skills-Registry zum Installieren/Updaten
- **MCP-Support** über `mcporter` (Bridge-Modell, entkoppelt von Core)
- Plugin-API: npm-Pakete + lokale Extension-Loading
- Browser-Tool, Exec-Tool, Read/Write/Edit, Subagenten

### Sandboxing
- Tool-Execution optional in Docker-Containern
- Modi: `off` | `non-main` | `all`
- Scopes: `session` | `agent` | `shared`
- Workspace-Access: `none` | `ro` | `rw`
- Sandbox-Browser mit noVNC-Observer

### Automation
- **Cron-Jobs**: Zeitgesteuerte Agent-Aufgaben
- **Heartbeats**: Periodische Check-ins (E-Mail, Kalender, Wetter etc.)
- **Hooks/Webhooks**: HTTP-Endpoints am Gateway für externe Events
- **Gmail PubSub**: Echtzeit-E-Mail-Benachrichtigungen

### Apps & UIs
- **Web Control UI**: Browser-Dashboard für Chat, Config, Sessions
- **macOS Menu-Bar App** mit bundled Gateway
- **iOS Node** mit Pairing und Canvas
- **Android Node** mit Pairing, Canvas, Chat, Kamera
- **TUI**: Terminal User Interface
- **WebChat**: Statische UI über Gateway-WebSocket

### Memory
- Plugin-Slot (ein Memory-Plugin aktiv)
- Memory-Indexierung und -Suche
- Workspace-Files als Langzeitgedächtnis (`MEMORY.md`, `memory/*.md`)

---

## 3. Architektur & Komponenten

### Übersicht
```
Chat-Apps + Plugins → Gateway → Pi Agent / CLI / Web UI / macOS App / iOS+Android Nodes
```

### Gateway (Daemon)
- **Zentraler Prozess**: Besitzt alle Messaging-Verbindungen
- **WebSocket-API**: Typisiert, JSON-Schema-validiert
- Bindet standardmäßig auf `127.0.0.1:18789` (Loopback)
- Events: `agent`, `chat`, `presence`, `health`, `heartbeat`, `cron`
- Hot-Reload: Config-Änderungen werden automatisch erkannt
- Strict Validation: Nur schema-konforme Configs werden akzeptiert

### Clients
- macOS App, CLI, Web UI verbinden sich per WebSocket
- Requests: `health`, `status`, `send`, `agent`, `system-presence`
- Events abonnieren: `tick`, `agent`, `presence`, `shutdown`

### Nodes
- macOS/iOS/Android/Headless verbinden sich auf **denselben WS-Server** mit `role: node`
- Device-basiertes Pairing mit Approval
- Capabilities: `canvas.*`, `camera.*`, `screen.record`, `location.get`

### Wire Protocol
- Transport: WebSocket, Text-Frames mit JSON
- Erster Frame muss `connect` sein
- Requests: `{type:"req", id, method, params}` → Response
- Events: `{type:"event", event, payload, seq?}`
- Auth via `OPENCLAW_GATEWAY_TOKEN` oder Config
- Idempotency-Keys für Side-Effects

### Canvas Host
- Served vom Gateway HTTP-Server
- `/__openclaw__/canvas/` (Agent-editierbares HTML/CSS/JS)
- `/__openclaw__/a2ui/` (A2UI Host)
- Gleicher Port wie Gateway (18789)

### Projekt-Struktur (Quellcode)
```
src/           – Quellcode (CLI, Commands, Provider, Infra, Media)
extensions/    – Plugin/Extension Packages
docs/          – Dokumentation (Mintlify-basiert)
apps/          – macOS, iOS, Android Apps
scripts/       – Build/Release/Utility-Scripts
dist/          – Build-Output
```

---

## 4. Wichtige Config-Optionen

Config-Datei: `~/.openclaw/openclaw.json` (JSON5, Kommentare erlaubt)

### Channels
```json5
{
  channels: {
    whatsapp: {
      enabled: true,
      allowFrom: ["+49..."],
      dmPolicy: "pairing",        // pairing | allowlist | open | disabled
      groups: { "*": { requireMention: true } }
    },
    telegram: { botToken: "...", dmPolicy: "pairing" },
    discord: { botToken: "...", dmPolicy: "pairing" }
  }
}
```

### Agents & Models
```json5
{
  agents: {
    defaults: {
      workspace: "~/.openclaw/workspace",
      model: {
        primary: "anthropic/claude-sonnet-4-5",
        fallbacks: ["openai/gpt-5.2"]
      },
      heartbeat: { every: "30m", target: "last" },
      sandbox: { mode: "off" }    // off | non-main | all
    },
    list: [
      { id: "main" },
      { id: "work", workspace: "~/.openclaw/workspace-work" }
    ]
  }
}
```

### Sessions
```json5
{
  session: {
    dmScope: "per-channel-peer",
    reset: { mode: "daily", atHour: 4, idleMinutes: 120 },
    threadBindings: { enabled: true, ttlHours: 24 }
  }
}
```

### Cron
```json5
{
  cron: {
    enabled: true,
    maxConcurrentRuns: 2,
    sessionRetention: "24h"
  }
}
```

### Hooks/Webhooks
```json5
{
  hooks: {
    enabled: true,
    token: "shared-secret",
    path: "/hooks",
    mappings: [{ match: { path: "gmail" }, action: "agent", agentId: "main" }]
  }
}
```

### Gateway
```json5
{
  gateway: {
    bind: "loopback",     // loopback | 0.0.0.0 (nicht empfohlen!)
    port: 18789,
    mode: "local",
    auth: { token: "..." }
  }
}
```

### Tools
```json5
{
  tools: {
    exec: {
      host: "sandbox",
      applyPatch: { workspaceOnly: true }
    },
    fs: { workspaceOnly: true },     // optional: restrict zu Workspace
    web: { search: { apiKey: "..." } }
  }
}
```

---

## 5. CLI-Befehle

### Installation & Setup
| Befehl | Beschreibung |
|--------|-------------|
| `openclaw onboard --install-daemon` | Setup-Wizard + Service installieren |
| `openclaw configure` | Config-Wizard |
| `openclaw setup` | Erweiterte Setup-Optionen |
| `openclaw doctor` | Diagnose & Reparatur |
| `openclaw update` | OpenClaw aktualisieren |
| `openclaw uninstall` | Deinstallation |

### Gateway
| Befehl | Beschreibung |
|--------|-------------|
| `openclaw gateway run --port 18789` | Gateway im Vordergrund starten |
| `openclaw gateway start/stop/restart` | Service-Steuerung |
| `openclaw gateway status` | Gateway-Status prüfen |
| `openclaw gateway install/uninstall` | Service installieren/entfernen |
| `openclaw dashboard` | Web Control UI öffnen |

### Channels
| Befehl | Beschreibung |
|--------|-------------|
| `openclaw channels list` | Alle Kanäle auflisten |
| `openclaw channels status --probe` | Kanal-Status mit Verbindungstest |
| `openclaw channels login` | Kanal einloggen (z.B. WhatsApp QR) |
| `openclaw channels logout` | Kanal ausloggen |

### Agents & Sessions
| Befehl | Beschreibung |
|--------|-------------|
| `openclaw agents list --bindings` | Agenten + Bindings anzeigen |
| `openclaw agents add <name>` | Neuen Agent erstellen |
| `openclaw agent -m "Hallo"` | Nachricht an Agent senden |
| `openclaw sessions` | Sessions auflisten |
| `openclaw status` | Gesamtstatus |

### Nachrichten
| Befehl | Beschreibung |
|--------|-------------|
| `openclaw message send --target <id> -m "..."` | Nachricht senden |

### Models
| Befehl | Beschreibung |
|--------|-------------|
| `openclaw models list` | Verfügbare Modelle |
| `openclaw models set <provider/model>` | Modell wechseln |
| `openclaw models auth add` | Provider-Auth hinzufügen |

### Automation
| Befehl | Beschreibung |
|--------|-------------|
| `openclaw cron list` | Cronjobs auflisten |
| `openclaw cron add` | Cronjob hinzufügen |
| `openclaw cron rm <id>` | Cronjob löschen |
| `openclaw system heartbeat last` | Letzten Heartbeat anzeigen |

### Tools & Skills
| Befehl | Beschreibung |
|--------|-------------|
| `openclaw skills list` | Installierte Skills |
| `openclaw plugins list` | Installierte Plugins |
| `openclaw plugins install <name>` | Plugin installieren |
| `openclaw sandbox list` | Sandbox-Container auflisten |
| `openclaw browser` | Browser-Tool |

### Weitere
| Befehl | Beschreibung |
|--------|-------------|
| `openclaw config get/set/unset <key>` | Config lesen/schreiben |
| `openclaw nodes` | Verbundene Nodes anzeigen |
| `openclaw devices` | Gepaarte Devices |
| `openclaw memory search <query>` | Memory durchsuchen |
| `openclaw logs` | Gateway-Logs |
| `openclaw security audit` | Sicherheitsaudit |
| `openclaw tui` | Terminal UI starten |
| `openclaw reset` | State zurücksetzen |

### Globale Flags
- `--dev` – Isolierter Dev-Modus (`~/.openclaw-dev`)
- `--profile <name>` – Isoliertes Profil (`~/.openclaw-<name>`)
- `--no-color` – Keine ANSI-Farben
- `--json` – JSON-Output
- `-V` / `--version` – Version anzeigen

---

## 6. Best Practices

### Sicherheit
- **Loopback-only**: Gateway immer auf `127.0.0.1` binden (Standard)
- **Nicht ins Internet exponieren** – stattdessen SSH-Tunnel oder Tailscale nutzen
- **Gateway-Token setzen** für Remote-Zugriff
- **DM-Policy**: `pairing` als Default (unbekannte Sender brauchen Bestätigungscode)
- **Sandboxing aktivieren** für nicht-vertrauenswürdige Workloads (`mode: "non-main"`)
- **Skills als untrusted Code behandeln** – vor Aktivierung lesen
- **Ein User pro Host/Gateway** – kein Multi-Tenant-Setup auf einem Gateway
- **`tools.exec.applyPatch.workspaceOnly: true`** für Dateisystem-Hardening

### Operations
- **Node 22+** verwenden (Sicherheitspatches)
- **`openclaw doctor`** bei Problemen als erste Anlaufstelle
- **Hot-Reload**: Config-Änderungen werden automatisch übernommen (kein Restart nötig)
- **Strict Validation**: Fehlerhafte Configs verhindern den Gateway-Start
- **Supervision**: launchd/systemd für Auto-Restart nutzen
- **`openclaw security audit --deep`** regelmäßig ausführen

### Agent-Design
- **Workspace-Files als Memory** nutzen (`MEMORY.md`, `memory/*.md`)
- **SOUL.md** für Persönlichkeit, **USER.md** für Kontext zum Nutzer
- **Heartbeats** für proaktive Checks (E-Mail, Kalender) – nicht zu häufig (30m+)
- **Cron für exakte Zeitpläne**, Heartbeats für flexible Batch-Checks
- **Multi-Agent**: Separate Workspaces pro Agent, keine `agentDir`-Wiederverwendung

### Entwicklung
- **TypeScript (ESM)**, Strict Typing, kein `any`
- **pnpm** als Package-Manager
- **Vitest** für Tests, 70% Coverage-Threshold
- **Oxlint + Oxfmt** für Linting/Formatting
- **Bun** für TypeScript-Execution in Dev
- **Plugins**: npm-Pakete, eigenes Repo; hohe Bar für Core-Additions
- **Skills**: Neue Skills auf ClawHub publizieren, nicht in Core

### Config-Tipps
- Minimale Config starten, nur hinzufügen was nötig ist
- `openclaw onboard` für interaktives Setup nutzen
- Channel-spezifische `allowFrom`-Listen für Zugriffskontrolle
- `mentionPatterns` in Gruppen konfigurieren
- Session-Resets aktivieren (`daily` oder `idle`) um Context-Bloat zu vermeiden

---

## 7. Wichtige Pfade

| Pfad | Beschreibung |
|------|-------------|
| `~/.openclaw/openclaw.json` | Haupt-Config (JSON5) |
| `~/.openclaw/workspace/` | Standard-Workspace (AGENTS.md, SOUL.md etc.) |
| `~/.openclaw/agents/<id>/` | Per-Agent State (Auth, Sessions) |
| `~/.openclaw/skills/` | Managed/Shared Skills |
| `~/.openclaw/credentials/` | Web-Provider Credentials |
| `/tmp/openclaw/` | Temp-Dateien (Media, Sandbox) |

---

## 8. Unterstützte Model-Provider

Anthropic, OpenAI, Bedrock, Google (Gemini/Qwen), Moonshot, Mistral, Ollama (lokal), OpenRouter, Together, Venice, HuggingFace, Nvidia, vLLM, LiteLLM, MiniMax, Xiaomi, GLM, Qianfan, Deepgram (Audio), GitHub Copilot, Cloudflare AI Gateway, Vercel AI Gateway, Kilocode

---

## 9. Docs-Struktur (Übersicht)

```
docs/
├── start/           – Getting Started, Quickstart, Wizard, Bootstrapping
├── concepts/        – Architektur, Features, Sessions, Models, Memory, Multi-Agent
├── gateway/         – Config, Security, Sandboxing, Protocol, Remote-Zugriff
├── channels/        – Kanal-spezifische Setup-Guides (WhatsApp, Telegram, ...)
├── cli/             – CLI-Referenz pro Command
├── tools/           – Skills, Plugins, Browser, Exec, Subagents
├── automation/      – Cron, Hooks, Webhooks, Heartbeat
├── nodes/           – iOS/Android Nodes, Camera, Audio
├── providers/       – Model-Provider Konfiguration
├── platforms/       – macOS, iOS, Android, Linux, Windows, Raspberry Pi
├── web/             – Control UI, Dashboard, WebChat, TUI
├── install/         – Installation (npm, Docker, Fly, Hetzner, Ansible, ...)
├── plugins/         – Plugin-System, Voice-Call, Community
├── security/        – Threat Model, Trust Boundaries
├── reference/       – API-Costs, Templates, Releasing, Credits
├── help/            – FAQ, Troubleshooting, Environment
└── zh-CN/           – Chinesische Übersetzung (auto-generiert)
```

Docs werden mit **Mintlify** gehostet auf `docs.openclaw.ai`.
