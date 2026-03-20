---
name: clickup
description: Comprehensive ClickUp project management integration for task creation, management, time tracking, and team collaboration. Use when working with ClickUp workspaces, spaces, folders, lists, tasks, docs, time tracking, or any ClickUp-related operations including project planning, task automation, sprint management, and team coordination.
---

# ClickUp Integration

This skill provides comprehensive ClickUp API integration for project management, task tracking, and team collaboration.

## Quick Start

### Authentication Setup

The ClickUp skill requires an API token. Store it in:
```
~/.config/clickup/api_token
```

To get your API token:
1. Go to ClickUp → Settings (gear icon) → Apps
2. Click "Generate" next to API Token
3. Copy the token and save it to the file above

### Team/Workspace ID

Most operations require a Team ID. Find it in your ClickUp URL:
- URL: `https://app.clickup.com/12345678/home`
- Team ID: `12345678`

Or use the script to list your teams:
```bash
python3 ~/.openclaw/workspace/skills/clickup/scripts/list_teams.py
```

## Core Workflows

### 1. Task Management

#### Create a Task
```bash
cd ~/.openclaw/workspace/skills/clickup && python3 scripts/create_task.py \
  --list-id "LIST_ID" \
  --name "Task Name" \
  --description "Task description" \
  --assignees "USER_ID1,USER_ID2" \
  --due-date "2026-02-25" \
  --priority "high" \
  --tags "tag1,tag2"
```

#### Get Task Details
```bash
python3 scripts/get_task.py --task-id "TASK_ID"
```

#### Update Task
```bash
python3 scripts/update_task.py \
  --task-id "TASK_ID" \
  --status "in progress" \
  --assignees "USER_ID"
```

#### List Tasks
```bash
python3 scripts/list_tasks.py \
  --list-id "LIST_ID" \
  --status "open" \
  --assignee "USER_ID"
```

### 2. Time Tracking

#### Start Time Tracking
```bash
python3 scripts/start_timer.py --task-id "TASK_ID"
```

#### Stop Time Tracking
```bash
python3 scripts/stop_timer.py
```

#### Get Time Entries
```bash
python3 scripts/get_time_entries.py \
  --team-id "TEAM_ID" \
  --start-date "2026-02-01" \
  --end-date "2026-02-18"
```

### 3. List & Folder Management

#### Create List
```bash
python3 scripts/create_list.py \
  --folder-id "FOLDER_ID" \
  --name "Sprint 24" \
  --content "List description"
```

#### Create Folder
```bash
python3 scripts/create_folder.py \
  --space-id "SPACE_ID" \
  --name "Q1 2026"
```

### 4. Comments & Collaboration

#### Add Comment
```bash
python3 scripts/add_comment.py \
  --task-id "TASK_ID" \
  --comment "Great progress! Keep it up." \
  --notify-all
```

#### Get Comments
```bash
python3 scripts/get_comments.py --task-id "TASK_ID"
```

### 5. Custom Fields

#### Get Custom Fields
```bash
python3 scripts/get_custom_fields.py --list-id "LIST_ID"
```

#### Set Custom Field Value
```bash
python3 scripts/set_custom_field.py \
  --task-id "TASK_ID" \
  --field-id "FIELD_ID" \
  --value "Field Value"
```

## Advanced Features

### Bulk Operations

#### Bulk Create Tasks from JSON
```bash
python3 scripts/bulk_create_tasks.py \
  --list-id "LIST_ID" \
  --input-file "tasks.json"
```

**tasks.json format:**
```json
[
  {
    "name": "Task 1",
    "description": "Description",
    "assignees": ["USER_ID"],
    "due_date": "2026-02-25",
    "priority": 3
  }
]
```

#### Bulk Update Tasks
```bash
python3 scripts/bulk_update_tasks.py \
  --input-file "updates.json"
```

### Automation & Webhooks

#### Create Webhook
```bash
python3 scripts/create_webhook.py \
  --team-id "TEAM_ID" \
  --endpoint "https://your-webhook-endpoint.com" \
  --events "taskCreated,taskUpdated"
```

### Reporting & Analytics

#### Generate Sprint Report
```bash
python3 scripts/sprint_report.py \
  --list-id "LIST_ID" \
  --start-date "2026-02-01" \
  --end-date "2026-02-18"
```

#### Team Velocity Report
```bash
python3 scripts/velocity_report.py \
  --team-id "TEAM_ID" \
  --sprints 4
```

## ClickUp Hierarchy

ClickUp organizes work in a hierarchy:

```
Team/Workspace (highest level)
  └── Space (e.g., "Marketing", "Development")
        └── Folder (optional, e.g., "Q1 2026")
              └── List (e.g., "Sprint 24")
                    └── Task
                    └── Subtask
```

### Get Hierarchy Information

#### List All Teams
```bash
python3 scripts/list_teams.py
```

#### List Spaces
```bash
python3 scripts/list_spaces.py --team-id "TEAM_ID"
```

#### List Folders
```bash
python3 scripts/list_folders.py --space-id "SPACE_ID"
```

#### List Lists
```bash
python3 scripts/list_lists.py --folder-id "FOLDER_ID"
# or
python3 scripts/list_lists.py --space-id "SPACE_ID"
```

## Priority Levels

ClickUp uses numeric priority levels:
- `1` - Urgent (red)
- `2` - High (yellow)
- `3` - Normal (blue)
- `4` - Low (gray)

## Common Use Cases

### Sprint Planning

1. Create sprint list
2. Add tasks with story points (custom field)
3. Assign team members
4. Set due dates for sprint end
5. Start time tracking

### Daily Standup

1. Get tasks updated today
2. Check time entries
3. Identify blockers (tasks with specific tag/status)

### Retrospective

1. Generate sprint report
2. Analyze completed vs planned tasks
3. Review time tracking data

## Integration with Other Tools

### Connect with Airtable
Sync ClickUp tasks with Airtable for advanced reporting:
```bash
python3 scripts/sync_to_airtable.py \
  --list-id "LIST_ID" \
  --airtable-base "BASE_ID" \
  --airtable-table "Tasks"
```

### Connect with Slack
Send task updates to Slack:
```bash
python3 scripts/notify_slack.py \
  --task-id "TASK_ID" \
  --slack-webhook "WEBHOOK_URL"
```

## Error Handling

All scripts include:
- Input validation
- API error handling with retry logic
- Clear error messages
- Exit codes for automation

## Rate Limits

ClickUp API rate limits:
- 100 requests per minute per token
- Scripts implement automatic backoff

## Reference Documentation

For detailed API information, see:
- [API Reference](references/api_reference.md) - Complete ClickUp API documentation
- [Common Patterns](references/common_patterns.md) - Frequently used patterns and workflows
- [Data Models](references/data_models.md) - ClickUp entity structures

## Best Practices

1. **Use Custom Fields** for project-specific data (story points, sprint numbers, etc.)
2. **Tag Consistently** for easy filtering and reporting
3. **Set Due Dates** for all time-bound tasks
4. **Use Templates** for recurring task types
5. **Track Time** for accurate project costing and velocity

## Environment Variables

Set these in your environment or `.env` file:
- `CLICKUP_API_TOKEN` - Your ClickUp API token
- `CLICKUP_TEAM_ID` - Default team ID
- `CLICKUP_DEFAULT_LIST_ID` - Default list for new tasks

## Troubleshooting

### "Unauthorized" Error
- Check API token is valid and not expired
- Ensure token has access to the workspace/team

### "Not Found" Error
- Verify IDs (team, space, folder, list, task) are correct
- Check you have permission to access the resource

### Rate Limiting
- Scripts automatically retry with backoff
- For bulk operations, use bulk endpoints

## Security Notes

- Never commit API tokens to version control
- Use environment variables or secure credential storage
- Rotate tokens periodically
- Use least-privilege tokens (workspace-specific if possible)