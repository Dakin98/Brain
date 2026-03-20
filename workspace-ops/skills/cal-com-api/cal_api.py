#!/usr/bin/env python3
"""
Cal.com API Helper Script
Usage: python3 cal_api.py <command> [options]
"""

import os
import requests
import json
import sys
from datetime import datetime, timedelta

BASE_URL = "https://api.cal.com/v1"

def get_api_key():
    api_key = os.environ.get('CALCOM_API_KEY')
    if not api_key:
        print("Error: CALCOM_API_KEY environment variable not set")
        sys.exit(1)
    return api_key

def make_request(endpoint, method='GET', data=None):
    api_key = get_api_key()
    url = f"{BASE_URL}{endpoint}"
    params = {'apiKey': api_key}
    
    try:
        if method == 'GET':
            response = requests.get(url, params=params)
        elif method == 'POST':
            response = requests.post(url, params=params, json=data)
        elif method == 'PATCH':
            response = requests.patch(url, params=params, json=data)
        elif method == 'DELETE':
            response = requests.delete(url, params=params)
        
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        sys.exit(1)

def cmd_me():
    """Get user profile"""
    data = make_request('/me')
    print(f"👤 {data['username']} ({data['email']})")
    print(f"🕒 Timezone: {data.get('timeZone', 'N/A')}")

def cmd_event_types():
    """List event types"""
    data = make_request('/event-types')
    print("📅 EVENT TYPES:")
    for event in data.get('event_types', []):
        duration = event.get('length', 'N/A')
        print(f"  • {event['title']} ({duration}min) - ID: {event['id']}")

def cmd_bookings(status=None):
    """List bookings"""
    endpoint = '/bookings'
    if status:
        endpoint += f"?status={status}"
    
    data = make_request(endpoint)
    print("📋 BOOKINGS:")
    for booking in data.get('bookings', []):
        start = booking.get('startTime', 'N/A')
        title = booking.get('title', 'N/A')
        status = booking.get('status', 'N/A')
        attendee = booking.get('attendees', [{}])[0].get('email', 'N/A')
        print(f"  • {start} - {title} ({status}) - {attendee}")

def cmd_availability(date_from=None, date_to=None):
    """Check availability"""
    if not date_from:
        date_from = datetime.now().strftime('%Y-%m-%d')
    if not date_to:
        date_to = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    
    endpoint = f'/availability?dateFrom={date_from}&dateTo={date_to}'
    data = make_request(endpoint)
    print(f"🕒 AVAILABILITY ({date_from} to {date_to}):")
    
    for day in data.get('busy', []):
        print(f"  📅 {day['start']} - {day['end']}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 cal_api.py <command> [options]")
        print("Commands:")
        print("  me                    - Get user profile")
        print("  event-types           - List event types")
        print("  bookings [status]     - List bookings (optional status filter)")
        print("  availability [from] [to] - Check availability (YYYY-MM-DD)")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'me':
        cmd_me()
    elif command == 'event-types':
        cmd_event_types()
    elif command == 'bookings':
        status = sys.argv[2] if len(sys.argv) > 2 else None
        cmd_bookings(status)
    elif command == 'availability':
        date_from = sys.argv[2] if len(sys.argv) > 2 else None
        date_to = sys.argv[3] if len(sys.argv) > 3 else None
        cmd_availability(date_from, date_to)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()