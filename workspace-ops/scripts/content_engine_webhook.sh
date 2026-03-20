#!/bin/bash
#
# Content Engine Webhook Handler
# Wird von n8n aufgerufen wenn Status = "Claude Generate"
#

TASK_ID="$1"

if [ -z "$TASK_ID" ]; then
    echo "Usage: $0 <clickup_task_id>"
    exit 1
fi

LOG_FILE="/tmp/content_engine.log"
echo "$(date): Starting content generation for task $TASK_ID" >> "$LOG_FILE"

cd /Users/denizakin/.openclaw/workspace

# Run the generator
python3 scripts/content_engine_generator.py --task-id "$TASK_ID" 2>&1 | tee -a "$LOG_FILE"

EXIT_CODE=${PIPESTATUS[0]}

if [ $EXIT_CODE -eq 0 ]; then
    echo "$(date): ✅ Content generated successfully for task $TASK_ID" >> "$LOG_FILE"
    
    # Update task status to "Content Generated"
    curl -s -X PUT \
        "https://api.clickup.com/api/v2/task/$TASK_ID" \
        -H "Authorization: $(cat ~/.config/clickup/api_token)" \
        -H "Content-Type: application/json" \
        -d '{"status": "content generated"}' > /dev/null
    
    echo "✅ Content Engine complete! Check ClickUp for generated content."
else
    echo "$(date): ❌ Error generating content for task $TASK_ID" >> "$LOG_FILE"
    
    # Add error comment
    curl -s -X POST \
        "https://api.clickup.com/api/v2/task/$TASK_ID/comment" \
        -H "Authorization: $(cat ~/.config/clickup/api_token)" \
        -H "Content-Type: application/json" \
        -d '{"comment_text": "❌ Error generating content. Please check logs or run manually.", "notify_all": true}' > /dev/null
    
    exit 1
fi
