# ClickUp Cold Mail Automation - Server Deployment

## Schnellstart

```bash
# 1. Auf Server kopieren
rsync -avz ~/.openclaw/workspace/scripts/clickup-coldmail-*.py server:~/.openclaw/workspace/scripts/
rsync -avz ~/.openclaw/workspace/scripts/clickup-coldmail-cron.sh server:~/.openclaw/workspace/scripts/

# 2. Credentials einrichten
ssh server "mkdir -p ~/.config/clickup ~/.config/airtable"
# Dann API Keys kopieren...

# 3. Cronjob installieren
ssh server "crontab -l 2>/dev/null > /tmp/cron; echo '*/10 * * * * /bin/bash ~/.openclaw/workspace/scripts/clickup-coldmail-cron.sh' >> /tmp/cron; crontab /tmp/cron"
```

## Requirements

- Python 3.8+
- curl
- crontab

## Verzeichnisstruktur auf Server

```
~/.openclaw/workspace/
├── scripts/
│   ├── clickup-coldmail-setup.py      # Haupt-Script
│   ├── clickup-coldmail-cron.sh       # Cron Wrapper
│   └── clickup-coldmail-onboarding.sh # Alternative (ohne Airtable)
├── logs/
│   └── clickup-coldmail-cron.log      # Log-Datei
└── config/
    └── crontab-entry.txt              # Cron-Beispiel
```

## Credentials

### ClickUp API Token

```bash
mkdir -p ~/.config/clickup
echo "pk_xxx_your_token_here" > ~/.config/clickup/api_token
chmod 600 ~/.config/clickup/api_token
```

### Airtable API Key

```bash
mkdir -p ~/.config/airtable
echo "patxxx.your_key_here" > ~/.config/airtable/api_key
chmod 600 ~/.config/airtable/api_key
```

## Crontab

```bash
# Bearbeiten
crontab -e

# Eintrag hinzufügen:
*/10 * * * * /bin/bash ~/.openclaw/workspace/scripts/clickup-coldmail-cron.sh

# Oder für Testing alle 2 Minuten:
*/2 * * * * /bin/bash ~/.openclaw/workspace/scripts/clickup-coldmail-cron.sh

# Status prüfen
crontab -l
```

## Logs

```bash
# Live Log ansehen
tail -f ~/.openclaw/workspace/logs/clickup-coldmail-cron.log

# Letzte Ausführung
tail -50 ~/.openclaw/workspace/logs/clickup-coldmail-cron.log
```

## Manuelles Testen

```bash
# Ohne Airtable (nur ClickUp)
python3 ~/.openclaw/workspace/scripts/clickup-coldmail-setup.py "Test Kunde" --dry-run

# Mit Airtable Integration
~/.openclaw/workspace/scripts/clickup-coldmail-cron.sh
```

## Troubleshooting

### Permission denied
```bash
chmod +x ~/.openclaw/workspace/scripts/*.sh
chmod +x ~/.openclaw/workspace/scripts/*.py
```

### Python nicht gefunden
```bash
# In Scripts anpassen:
# python3 -> /usr/bin/python3
which python3
```

### Cron läuft nicht
```bash
# Cron-Service prüfen (Linux)
systemctl status cron

# Oder (je nach Distro)
service cron status
```

### Lock-File hängt
```bash
rm /tmp/clickup-coldmail-cron.lock
```

## Migration vom Mac

```bash
# Alles packen
tar -czf clickup-automation.tar.gz \
  ~/.openclaw/workspace/scripts/clickup-coldmail-* \
  ~/.openclaw/workspace/docs/clickup-coldmail-automation.md

# Auf Server kopieren
scp clickup-automation.tar.gz server:~/

# Entpacken
ssh server "tar -xzf clickup-automation.tar.gz"
```

## Systemd Alternative (Linux)

Für Server mit systemd statt cron:

```ini
# ~/.config/systemd/user/clickup-coldmail.service
[Unit]
Description=ClickUp Cold Mail Automation

[Service]
Type=oneshot
ExecStart=/bin/bash %h/.openclaw/workspace/scripts/clickup-coldmail-cron.sh

[Install]
WantedBy=default.target
```

```ini
# ~/.config/systemd/user/clickup-coldmail.timer
[Unit]
Description=Run ClickUp Cold Mail every 10 minutes

[Timer]
OnBootSec=5min
OnUnitActiveSec=10min

[Install]
WantedBy=timers.target
```

```bash
systemctl --user daemon-reload
systemctl --user enable clickup-coldmail.timer
systemctl --user start clickup-coldmail.timer
systemctl --user list-timers
```
