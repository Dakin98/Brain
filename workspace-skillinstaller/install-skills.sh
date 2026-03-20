#!/bin/bash
# Skill Installation Script - Runs with delays to respect rate limits

SKILLS=(
  "academic-deep-research"
  "agentic-paper-digest"
  "b2c-marketing"
  "blog-writer"
  "ad-ready"
  "ad-ready-pro"
  "newsletter"
  "newsletter-writer"
  "newsletter-creation-curation"
  "blog-to-kindle"
  "bearblog"
)

LOG_FILE="$HOME/.openclaw/workspace-skillinstaller/installation-log.md"
DELAY=600  # 10 minutes between installs

echo "# Skill Installation Log - $(date)" > "$LOG_FILE"
echo "" >> "$LOG_FILE"

for skill in "${SKILLS[@]}"; do
  echo "Installing: $skill"
  echo "## $(date) - $skill" >> "$LOG_FILE"
  
  if clawhub install "$skill" 2>&1 | tee -a "$LOG_FILE"; then
    echo "✅ SUCCESS: $skill" >> "$LOG_FILE"
  else
    echo "❌ FAILED: $skill" >> "$LOG_FILE"
  fi
  
  echo "" >> "$LOG_FILE"
  echo "Waiting ${DELAY} seconds..."
  sleep $DELAY
done

echo "## Installation Complete - $(date)" >> "$LOG_FILE"