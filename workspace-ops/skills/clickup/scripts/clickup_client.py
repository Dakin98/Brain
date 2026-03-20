#!/usr/bin/env python3
"""
ClickUp API Client - Core functions for interacting with ClickUp API
"""

import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timedelta
import ssl

# Constants
BASE_URL = "https://api.clickup.com/api/v2"
DEFAULT_TIMEOUT = 30

class ClickUpClient:
    """Client for interacting with ClickUp API"""
    
    def __init__(self, api_token=None):
        """Initialize with API token"""
        if api_token is None:
            api_token = self._get_api_token()
        
        self.api_token = api_token
        self.headers = {
            "Authorization": api_token,
            "Content-Type": "application/json"
        }
    
    def _get_api_token(self):
        """Get API token from config file or environment"""
        # Try config file first
        config_path = os.path.expanduser("~/.config/clickup/api_token")
        if os.path.exists(config_path):
            with open(config_path) as f:
                return f.read().strip()
        
        # Try environment variable
        token = os.environ.get("CLICKUP_API_TOKEN")
        if token:
            return token
        
        raise ValueError(
            "ClickUp API token not found. "
            "Set CLICKUP_API_TOKEN environment variable or "
            f"create {config_path}"
        )
    
    def _request(self, method, endpoint, data=None, params=None):
        """Make API request with error handling and retries"""
        url = f"{BASE_URL}{endpoint}"
        
        # Add query parameters
        if params:
            query_string = "&".join(f"{k}={urllib.parse.quote(str(v))}" 
                                   for k, v in params.items() if v is not None)
            if query_string:
                url += f"?{query_string}"
        
        # Create request
        req = urllib.request.Request(
            url,
            headers=self.headers,
            method=method
        )
        
        # Add body for POST/PUT requests
        if data and method in ["POST", "PUT", "PATCH"]:
            req.data = json.dumps(data).encode()
        
        # Execute with retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Create SSL context that doesn't verify certificates
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                
                with urllib.request.urlopen(req, timeout=DEFAULT_TIMEOUT, context=ctx) as response:
                    return json.loads(response.read())
            
            except urllib.error.HTTPError as e:
                error_body = e.read().decode()
                error_data = json.loads(error_body) if error_body else {}
                
                # Handle rate limiting
                if e.code == 429:
                    if attempt < max_retries - 1:
                        import time
                        time.sleep(2 ** attempt)  # Exponential backoff
                        continue
                
                # Handle authentication errors
                if e.code in [401, 403]:
                    raise ClickUpAuthError(f"Authentication failed: {error_data.get('err', 'Unknown error')}")
                
                # Handle not found
                if e.code == 404:
                    raise ClickUpNotFoundError(f"Resource not found: {endpoint}")
                
                raise ClickUpAPIError(f"API Error {e.code}: {error_data.get('err', error_body)}")
            
            except Exception as e:
                if attempt < max_retries - 1:
                    import time
                    time.sleep(2 ** attempt)
                    continue
                raise ClickUpAPIError(f"Request failed: {str(e)}")
        
        raise ClickUpAPIError("Max retries exceeded")
    
    def get(self, endpoint, params=None):
        """Make GET request"""
        return self._request("GET", endpoint, params=params)
    
    def post(self, endpoint, data=None, params=None):
        """Make POST request"""
        return self._request("POST", endpoint, data=data, params=params)
    
    def put(self, endpoint, data=None, params=None):
        """Make PUT request"""
        return self._request("PUT", endpoint, data=data, params=params)
    
    def delete(self, endpoint, params=None):
        """Make DELETE request"""
        return self._request("DELETE", endpoint, params=params)
    
    # ==================== Team Methods ====================
    
    def list_teams(self):
        """Get all teams/workspaces"""
        return self.get("/team")
    
    # ==================== Space Methods ====================
    
    def list_spaces(self, team_id, archived=False):
        """List spaces in a team"""
        return self.get(f"/team/{team_id}/space", params={"archived": archived})
    
    def create_space(self, team_id, name, **kwargs):
        """Create a new space"""
        data = {"name": name, **kwargs}
        return self.post(f"/team/{team_id}/space", data=data)
    
    # ==================== Folder Methods ====================
    
    def list_folders(self, space_id, archived=False):
        """List folders in a space"""
        return self.get(f"/space/{space_id}/folder", params={"archived": archived})
    
    def create_folder(self, space_id, name):
        """Create a new folder"""
        return self.post(f"/space/{space_id}/folder", data={"name": name})
    
    # ==================== List Methods ====================
    
    def get_lists(self, folder_id=None, space_id=None, archived=False):
        """Get lists (either from folder or space)"""
        if folder_id:
            return self.get(f"/folder/{folder_id}/list", params={"archived": archived})
        elif space_id:
            return self.get(f"/space/{space_id}/list", params={"archived": archived})
        else:
            raise ValueError("Either folder_id or space_id must be provided")
    
    def create_list(self, name, folder_id=None, space_id=None, **kwargs):
        """Create a new list"""
        data = {"name": name, **kwargs}
        
        if folder_id:
            return self.post(f"/folder/{folder_id}/list", data=data)
        elif space_id:
            return self.post(f"/space/{space_id}/list", data=data)
        else:
            raise ValueError("Either folder_id or space_id must be provided")
    
    # ==================== Task Methods ====================
    
    def get_tasks(self, list_id, **filters):
        """Get tasks from a list with optional filters"""
        params = {k: v for k, v in filters.items() if v is not None}
        return self.get(f"/list/{list_id}/task", params=params)
    
    def get_task(self, task_id, include_subtasks=False, include_markdown=False):
        """Get a specific task"""
        params = {
            "include_subtasks": include_subtasks,
            "include_markdown_content": include_markdown
        }
        return self.get(f"/task/{task_id}", params=params)
    
    def create_task(self, list_id, name, **kwargs):
        """Create a new task"""
        data = {"name": name, **kwargs}
        return self.post(f"/list/{list_id}/task", data=data)
    
    def update_task(self, task_id, **kwargs):
        """Update an existing task"""
        return self.put(f"/task/{task_id}", data=kwargs)
    
    def delete_task(self, task_id):
        """Delete a task"""
        return self.delete(f"/task/{task_id}")
    
    # ==================== Time Tracking Methods ====================
    
    def get_time_entries(self, team_id, start_date, end_date, **filters):
        """Get time entries for a team"""
        params = {
            "start_date": start_date,
            "end_date": end_date,
            **filters
        }
        return self.get(f"/team/{team_id}/time_entries", params=params)
    
    def start_timer(self, team_id, task_id, description=None, billable=True):
        """Start tracking time for a task"""
        data = {
            "tid": task_id,
            "billable": billable
        }
        if description:
            data["description"] = description
        return self.post(f"/team/{team_id}/time_entries/start", data=data)
    
    def stop_timer(self, team_id):
        """Stop the current timer"""
        return self.post(f"/team/{team_id}/time_entries/stop", data={})
    
    def create_time_entry(self, team_id, task_id, start, end, duration, 
                         description=None, billable=False, tags=None):
        """Create a manual time entry"""
        data = {
            "tid": task_id,
            "start": start,
            "end": end,
            "duration": duration,
            "billable": billable
        }
        if description:
            data["description"] = description
        if tags:
            data["tags"] = tags
        return self.post(f"/team/{team_id}/time_entries", data=data)
    
    # ==================== Comment Methods ====================
    
    def get_comments(self, task_id=None, view_id=None):
        """Get comments for a task or view"""
        if task_id:
            return self.get(f"/task/{task_id}/comment")
        elif view_id:
            return self.get(f"/view/{view_id}/comment")
        else:
            raise ValueError("Either task_id or view_id must be provided")
    
    def create_comment(self, task_id, comment_text, assignee=None, notify_all=False):
        """Add a comment to a task"""
        data = {
            "comment_text": comment_text,
            "notify_all": notify_all
        }
        if assignee:
            data["assignee"] = assignee
        return self.post(f"/task/{task_id}/comment", data=data)
    
    # ==================== Custom Field Methods ====================
    
    def get_custom_fields(self, list_id):
        """Get custom fields for a list"""
        return self.get(f"/list/{list_id}/field")
    
    def set_custom_field(self, task_id, field_id, value):
        """Set a custom field value"""
        return self.post(f"/task/{task_id}/field/{field_id}", data={"value": value})
    
    # ==================== Webhook Methods ====================
    
    def create_webhook(self, team_id, endpoint, events, **kwargs):
        """Create a webhook"""
        data = {
            "endpoint": endpoint,
            "events": events,
            **kwargs
        }
        return self.post(f"/team/{team_id}/webhook", data=data)
    
    def list_webhooks(self, team_id):
        """List webhooks for a team"""
        return self.get(f"/team/{team_id}/webhook")
    
    def delete_webhook(self, webhook_id):
        """Delete a webhook"""
        return self.delete(f"/webhook/{webhook_id}")
    
    # ==================== User Methods ====================
    
    def get_team_members(self, team_id):
        """Get team members"""
        return self.get(f"/team/{team_id}/user")


class ClickUpError(Exception):
    """Base exception for ClickUp errors"""
    pass

class ClickUpAPIError(ClickUpError):
    """API error from ClickUp"""
    pass

class ClickUpAuthError(ClickUpError):
    """Authentication error"""
    pass

class ClickUpNotFoundError(ClickUpError):
    """Resource not found"""
    pass


# Utility functions
def timestamp_to_datetime(timestamp_ms):
    """Convert ClickUp timestamp (milliseconds) to datetime"""
    return datetime.fromtimestamp(timestamp_ms / 1000)

def datetime_to_timestamp(dt):
    """Convert datetime to ClickUp timestamp (milliseconds)"""
    return int(dt.timestamp() * 1000)

def format_duration(milliseconds):
    """Format duration in milliseconds to human readable string"""
    seconds = milliseconds // 1000
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60
    
    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if remaining_seconds > 0 and hours == 0:
        parts.append(f"{remaining_seconds}s")
    
    return " ".join(parts) if parts else "0m"


def parse_priority(priority):
    """Parse priority value to string"""
    priority_map = {
        1: "urgent",
        2: "high",
        3: "normal",
        4: "low"
    }
    return priority_map.get(priority, "none")


if __name__ == "__main__":
    # Test the client
    try:
        client = ClickUpClient()
        print("✓ ClickUp client initialized successfully")
        
        # Try to list teams
        teams = client.list_teams()
        print(f"✓ Found {len(teams.get('teams', []))} teams")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)