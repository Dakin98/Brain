#!/bin/bash
# Newsletter Automation v3 - Weekly Cronjob
# 
# Add to crontab:
# 0 9 * * 1 /Users/denizakin/.openclaw/workspace/scripts/cron_newsletter.sh

set -e

export KLAVIYO_API_KEY="${KLAVIYO_API_KEY:-pk_dfc4dd8deb22827d0244a251f315db13c3}"
export PATH="/usr/local/bin:$PATH"

cd /Users/denizakin/.openclaw/workspace

echo "=========================================="
echo "📧 Newsletter Automation v3 - $(date)"
echo "=========================================="

# Run automation
python3 scripts/newsletter_automation_v3.py

echo ""
echo "✅ Automation completed at $(date)"
echo "=========================================="