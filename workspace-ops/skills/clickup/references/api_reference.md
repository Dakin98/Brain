# ClickUp API Reference

Complete reference for the ClickUp API v2.

## Base URL
```
https://api.clickup.com/api/v2
```

## Authentication

All requests require an Authorization header:
```
Authorization: pk_your_api_token_here
```

## Rate Limits
- 100 requests per minute per token
- Rate limit headers included in responses:
  - `X-RateLimit-Limit`: 100
  - `X-RateLimit-Remaining`: Requests remaining
  - `X-RateLimit-Reset`: Unix timestamp when limit resets

## Core Endpoints

### Teams / Workspaces

#### List Teams
```http
GET /team
```

**Response:**
```json
{
  "teams": [
    {
      "id": "12345678",
      "name": "My Team",
      "color": "#000000",
      "avatar": "https://...",
      "members": [...]
    }
  ]
}
```

### Spaces

#### List Spaces
```http
GET /team/{team_id}/space
```

**Query Parameters:**
- `archived` (boolean): Include archived spaces

#### Create Space
```http
POST /team/{team_id}/space
```

**Request Body:**
```json
{
  "name": "Space Name",
  "multiple_assignees": true,
  "features": {
    "due_dates": {
      "enabled": true,
      "start_date": true,
      "remap_due_dates": true
    },
    "time_tracking": {
      "enabled": true
    }
  }
}
```

### Folders

#### List Folders
```http
GET /space/{space_id}/folder
```

#### Create Folder
```http
POST /space/{space_id}/folder
```

**Request Body:**
```json
{
  "name": "Folder Name"
}
```

### Lists

#### List Lists (in Folder)
```http
GET /folder/{folder_id}/list
```

#### List Lists (in Space)
```http
GET /space/{space_id}/list
```

#### Create List
```http
POST /folder/{folder_id}/list
# or
POST /space/{space_id}/list
```

**Request Body:**
```json
{
  "name": "List Name",
  "content": "List description",
  "due_date": 1706745600000,
  "due_date_time": false,
  "priority": 3,
  "assignee": 123,
  "status": "red"
}
```

### Tasks

#### Get Tasks
```http
GET /list/{list_id}/task
```

**Query Parameters:**
- `archived` (boolean): Include archived tasks
- `page` (integer): Page number (0-indexed)
- `order_by` (string): `created`, `updated`, `due_date`
- `reverse` (boolean): Reverse order
- `subtasks` (boolean): Include subtasks
- `statuses[]` (array): Filter by statuses
- `include_closed` (boolean): Include closed tasks
- `assignees[]` (array): Filter by assignees
- `tags[]` (array): Filter by tags
- `due_date_gt` (timestamp): Due date greater than
- `due_date_lt` (timestamp): Due date less than
- `date_created_gt` (timestamp): Created after
- `date_updated_gt` (timestamp): Updated after

#### Get Task
```http
GET /task/{task_id}
```

**Query Parameters:**
- `include_subtasks` (boolean)
- `include_markdown_content` (boolean)

#### Create Task
```http
POST /list/{list_id}/task
```

**Request Body:**
```json
{
  "name": "Task Name",
  "description": "Task description",
  "assignees": [123, 456],
  "tags": ["tag1", "tag2"],
  "status": "To Do",
  "priority": 3,
  "due_date": 1706745600000,
  "due_date_time": false,
  "start_date": 1706659200000,
  "start_date_time": false,
  "notify_all": true,
  "parent": null,
  "links_to": null,
  "custom_fields": [
    {
      "id": "custom_field_id",
      "value": "field value"
    }
  ]
}
```

#### Update Task
```http
PUT /task/{task_id}
```

#### Delete Task
```http
DELETE /task/{task_id}
```

### Time Tracking

#### Get Time Entries
```http
GET /team/{team_id}/time_entries
```

**Query Parameters:**
- `start_date` (timestamp, required): Start of range
- `end_date` (timestamp, required): End of range
- `assignee` (integer): Filter by assignee
- `include_task_tags` (boolean)
- `include_location_names` (boolean)
- `space_id` (string): Filter by space
- `folder_id` (string): Filter by folder
- `list_id` (string): Filter by list
- `task_id` (string): Filter by task
- `custom_task_ids` (boolean)
- `query` (string): Search query
- `client_id` (string): Filter by client
- `tag_ids[]` (array): Filter by tags

#### Start Time Entry
```http
POST /team/{team_id}/time_entries/start
```

**Request Body:**
```json
{
  "tid": "task_id",
  "description": "Working on feature X",
  "billable": true
}
```

#### Stop Time Entry
```http
POST /team/{team_id}/time_entries/stop
```

**Request Body:**
```json
{
  "tid": "task_id"
}
```

#### Create Time Entry
```http
POST /team/{team_id}/time_entries
```

**Request Body:**
```json
{
  "tid": "task_id",
  "start": 1706745600000,
  "end": 1706749200000,
  "duration": 3600000,
  "description": "Worked on feature",
  "billable": true,
  "tags": ["tag1"],
  "source": "api"
}
```

### Comments

#### Get Comments
```http
GET /task/{task_id}/comment
# or
GET /view/{view_id}/comment
```

#### Create Comment
```http
POST /task/{task_id}/comment
```

**Request Body:**
```json
{
  "comment_text": "Great progress!",
  "assignee": 123,
  "notify_all": true
}
```

#### Update Comment
```http
PUT /comment/{comment_id}
```

#### Delete Comment
```http
DELETE /comment/{comment_id}
```

### Custom Fields

#### Get Custom Fields
```http
GET /list/{list_id}/field
```

#### Set Custom Field Value
```http
POST /task/{task_id}/field/{field_id}
```

**Request Body:**
```json
{
  "value": "field value"
}
```

#### Remove Custom Field Value
```http
DELETE /task/{task_id}/field/{field_id}
```

### Users

#### Get Team Members
```http
GET /team/{team_id}/user
```

#### Get User
```http
GET /user/{user_id}
```

### Goals

#### List Goals
```http
GET /team/{team_id}/goal
```

#### Create Goal
```http
POST /team/{team_id}/goal
```

**Request Body:**
```json
{
  "name": "Goal Name",
  "due_date": 1706745600000,
  "description": "Goal description",
  "multiple_owners": true,
  "owners": [123],
  "color": "#000000"
}
```

### Webhooks

#### Create Webhook
```http
POST /team/{team_id}/webhook
```

**Request Body:**
```json
{
  "endpoint": "https://your-endpoint.com/webhook",
  "events": [
    "taskCreated",
    "taskUpdated",
    "taskDeleted"
  ],
  "space_id": "space_id",
  "folder_id": "folder_id",
  "list_id": "list_id"
}
```

**Available Events:**
- `taskCreated`
- `taskUpdated`
- `taskDeleted`
- `taskPriorityUpdated`
- `taskStatusUpdated`
- `taskAssigneeUpdated`
- `taskDueDateUpdated`
- `taskTagUpdated`
- `taskMoved`
- `taskCommentPosted`
- `taskCommentUpdated`
- `listCreated`
- `listUpdated`
- `listDeleted`
- `folderCreated`
- `folderUpdated`
- `folderDeleted`
- `spaceCreated`
- `spaceUpdated`
- `spaceDeleted`

#### List Webhooks
```http
GET /team/{team_id}/webhook
```

#### Delete Webhook
```http
DELETE /webhook/{webhook_id}
```

## Data Types

### Priority
- `1` - Urgent (red)
- `2` - High (yellow)
- `3` - Normal (blue)
- `4` - Low (gray)
- `null` - No priority

### Status
Status values are custom per space, but common defaults:
- `"to do"`
- `"in progress"`
- `"review"`
- `"done"`
- `"closed"`

### Dates
All dates are Unix timestamps in milliseconds.

## Error Responses

### 400 Bad Request
```json
{
  "err": "Invalid input",
  "ECODE": "INPUT_002"
}
```

### 401 Unauthorized
```json
{
  "err": "Token invalid",
  "ECODE": "OAUTH_002"
}
```

### 403 Forbidden
```json
{
  "err": "Not permitted",
  "ECODE": "ACCESS_002"
}
```

### 404 Not Found
```json
{
  "err": "Task not found",
  "ECODE": "NOT_FOUND"
}
```

### 429 Rate Limited
```json
{
  "err": "Rate limit exceeded",
  "ECODE": "RATE_LIMIT"
}
```

## Pagination

List endpoints support pagination:

**Query Parameters:**
- `page` (integer): Page number (0-indexed)
- `limit` (integer): Items per page (max 100)

**Response:**
```json
{
  "tasks": [...],
  "page": 0,
  "pages": 5,
  "total": 47
}
```

## Filtering & Search

### Task Search
```http
GET /team/{team_id}/task
```

**Query Parameters:**
- `tags[]`: Filter by tags
- `statuses[]`: Filter by status
- `assignees[]`: Filter by assignee
- `due_date_gt`: Due date greater than (timestamp)
- `due_date_lt`: Due date less than (timestamp)
- `date_created_gt`: Created after (timestamp)
- `date_updated_gt`: Updated after (timestamp)
- `custom_fields`: JSON string of custom field filters

### Full Text Search
```http
GET /team/{team_id}/task?q=search%20query
```

## Batch Operations

ClickUp supports limited batch operations. For bulk updates, make multiple parallel requests with appropriate rate limiting.

Recommended approach:
1. Use connection pooling
2. Limit to 10 concurrent requests
3. Implement exponential backoff on 429 responses

## Webhook Payloads

### Task Created
```json
{
  "event": "taskCreated",
  "task_id": "abc123",
  "webhook_id": "wh_123"
}
```

### Task Updated
```json
{
  "event": "taskUpdated",
  "task_id": "abc123",
  "webhook_id": "wh_123",
  "history_items": [...]
}
```