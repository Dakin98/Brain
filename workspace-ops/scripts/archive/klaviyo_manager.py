#!/usr/bin/env python3
"""
Klaviyo Campaign Manager
Handles template and campaign creation with smart workarounds for API limitations.
"""

import os
import json
import base64
import urllib.request
import urllib.error
from datetime import datetime, timezone
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass

# Optional requests support
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

@dataclass
class KlaviyoConfig:
    api_key: str
    base_url: str = "https://a.klaviyo.com/api"
    revision: str = "2024-10-15"

@dataclass
class NewsletterConfig:
    name: str
    subject: str
    preview_text: str
    send_date: str  # ISO format: 2026-02-26
    send_time: str  # 24h format: 09:00
    html_content: str
    text_content: str
    list_id: str
    from_email: str = "hello@razeco.de"
    from_label: str = "Razeco"

class KlaviyoClient:
    """Klaviyo API Client with helper methods"""
    
    def __init__(self, config: KlaviyoConfig):
        self.config = config
        if HAS_REQUESTS:
            self.session = requests.Session()
            self.session.headers.update({
                "Authorization": f"Klaviyo-API-Key {config.api_key}",
                "revision": config.revision,
                "Content-Type": "application/json"
            })
        self._use_requests = HAS_REQUESTS
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """Make authenticated request"""
        url = f"{self.config.base_url}{endpoint}"
        
        if self._use_requests:
            response = self.session.request(method, url, **kwargs)
            if response.status_code >= 400:
                print(f"❌ Error {response.status_code}: {response.text[:500]}")
                return {"error": response.text}
            return response.json() if response.text else {}
        else:
            # Use urllib as fallback
            return self._urllib_request(method, url, **kwargs)
    
    def _urllib_request(self, method: str, url: str, json_data: Dict = None) -> Dict:
        """Make request using urllib (no external dependencies)"""
        headers = {
            "Authorization": f"Klaviyo-API-Key {self.config.api_key}",
            "revision": self.config.revision,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        data = None
        if json_data:
            data = json.dumps(json_data).encode('utf-8')
        
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        
        try:
            with urllib.request.urlopen(req) as response:
                body = response.read().decode('utf-8')
                return json.loads(body) if body else {}
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            print(f"❌ Error {e.code}: {error_body[:500]}")
            return {"error": error_body}
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return {"error": str(e)}
    
    # ============ TEMPLATES ============
    
    def create_template(self, name: str, html: str, text: str) -> Dict:
        """Create a new email template"""
        data = {
            "data": {
                "type": "template",
                "attributes": {
                    "name": name,
                    "editor_type": "CODE",
                    "html": html,
                    "text": text
                }
            }
        }
        return self._request("POST", "/templates", json=data)
    
    def get_template(self, template_id: str) -> Dict:
        """Get template by ID"""
        return self._request("GET", f"/templates/{template_id}")
    
    def list_templates(self, page_size: int = 100) -> List[Dict]:
        """List all templates"""
        result = self._request("GET", f"/templates?page[size]={page_size}")
        return result.get("data", [])
    
    def update_template(self, template_id: str, name: Optional[str] = None, 
                       html: Optional[str] = None, text: Optional[str] = None) -> Dict:
        """Update existing template"""
        attrs = {}
        if name:
            attrs["name"] = name
        if html:
            attrs["html"] = html
        if text:
            attrs["text"] = text
            
        data = {
            "data": {
                "type": "template",
                "id": template_id,
                "attributes": attrs
            }
        }
        return self._request("PATCH", f"/templates/{template_id}", json=data)
    
    def delete_template(self, template_id: str) -> bool:
        """Delete template"""
        result = self._request("DELETE", f"/templates/{template_id}")
        return "error" not in result
    
    # ============ CAMPAIGNS ============
    
    def create_campaign(self, name: str, list_id: str, subject: str, 
                       preview_text: str, send_datetime: str,
                       from_email: str = "hello@razeco.de",
                       from_label: str = "Razeco") -> Dict:
        """
        Create campaign with message structure.
        Note: HTML content must be linked manually in UI or use templates.
        """
        data = {
            "data": {
                "type": "campaign",
                "attributes": {
                    "name": name,
                    "audiences": {
                        "included": [list_id],
                        "excluded": []
                    },
                    "send_strategy": {
                        "method": "static",
                        "options_static": {
                            "datetime": send_datetime
                        }
                    },
                    "campaign-messages": {
                        "data": [{
                            "type": "campaign-message",
                            "attributes": {
                                "channel": "email",
                                "label": "Default",
                                "content": {
                                    "subject": subject,
                                    "preview_text": preview_text,
                                    "from_email": from_email,
                                    "from_label": from_label
                                }
                            }
                        }]
                    }
                }
            }
        }
        return self._request("POST", "/campaigns", json=data)
    
    def get_campaign(self, campaign_id: str) -> Dict:
        """Get campaign by ID"""
        return self._request("GET", f"/campaigns/{campaign_id}")
    
    def list_campaigns(self, page_size: int = 100) -> List[Dict]:
        """List all campaigns"""
        result = self._request("GET", f"/campaigns?page[size]={page_size}")
        return result.get("data", [])
    
    def update_campaign(self, campaign_id: str, **kwargs) -> Dict:
        """Update campaign attributes"""
        attrs = {}
        if "name" in kwargs:
            attrs["name"] = kwargs["name"]
        if "audiences" in kwargs:
            attrs["audiences"] = kwargs["audiences"]
        if "send_strategy" in kwargs:
            attrs["send_strategy"] = kwargs["send_strategy"]
            
        data = {
            "data": {
                "type": "campaign",
                "id": campaign_id,
                "attributes": attrs
            }
        }
        return self._request("PATCH", f"/campaigns/{campaign_id}", json=data)
    
    def delete_campaign(self, campaign_id: str) -> bool:
        """Delete campaign"""
        result = self._request("DELETE", f"/campaigns/{campaign_id}")
        return "error" not in result
    
    # ============ CAMPAIGN MESSAGES ============
    
    def update_message_content(self, message_id: str, subject: Optional[str] = None,
                              preview_text: Optional[str] = None,
                              from_email: Optional[str] = None,
                              from_label: Optional[str] = None) -> Dict:
        """Update message metadata (NOT HTML content)"""
        content = {}
        if subject:
            content["subject"] = subject
        if preview_text:
            content["preview_text"] = preview_text
        if from_email:
            content["from_email"] = from_email
        if from_label:
            content["from_label"] = from_label
            
        data = {
            "data": {
                "type": "campaign-message",
                "id": message_id,
                "attributes": {
                    "content": content
                }
            }
        }
        return self._request("PATCH", f"/campaign-messages/{message_id}", json=data)
    
    def get_message(self, message_id: str) -> Dict:
        """Get campaign message"""
        return self._request("GET", f"/campaign-messages/{message_id}")
    
    # ============ LISTS ============
    
    def list_lists(self) -> List[Dict]:
        """Get all lists/audiences"""
        result = self._request("GET", "/lists")
        return result.get("data", [])
    
    def get_list(self, list_id: str) -> Dict:
        """Get list by ID"""
        return self._request("GET", f"/lists/{list_id}")
    
    # ============ IMAGES ============
    
    def list_images(self, page_size: int = 100) -> List[Dict]:
        """List all uploaded images"""
        result = self._request("GET", f"/images?page[size]={page_size}")
        return result.get("data", [])
    
    def upload_image(self, name: str, image_data: bytes, 
                    content_type: str = "image/png") -> Dict:
        """Upload image to Klaviyo"""
        # Note: This requires multipart/form-data which is more complex
        # Use direct API for now
        import base64
        b64_data = base64.b64encode(image_data).decode()
        
        data = {
            "data": {
                "type": "image",
                "attributes": {
                    "name": name,
                    "image": b64_data,
                    "content_type": content_type
                }
            }
        }
        return self._request("POST", "/images", json=data)
    
    # ============ WORKFLOW METHODS ============
    
    def create_newsletter_workflow(self, config: NewsletterConfig) -> Tuple[Dict, Dict]:
        """
        Complete workflow: Create template + campaign
        Returns (template_result, campaign_result)
        """
        print(f"📧 Creating newsletter: {config.name}")
        
        # 1. Create Template
        template_name = f"{config.name} | {config.send_date}"
        print(f"  📝 Creating template: {template_name}")
        template = self.create_template(
            name=template_name,
            html=config.html_content,
            text=config.text_content
        )
        
        if "error" in template:
            print(f"  ❌ Template creation failed")
            return template, {}
        
        template_id = template.get("data", {}).get("id")
        print(f"  ✅ Template created: {template_id}")
        
        # 2. Create Campaign
        print(f"  📨 Creating campaign...")
        send_datetime = f"{config.send_date}T{config.send_time}:00Z"
        campaign = self.create_campaign(
            name=f"{config.name} | {config.send_date}",
            list_id=config.list_id,
            subject=config.subject,
            preview_text=config.preview_text,
            send_datetime=send_datetime,
            from_email=config.from_email,
            from_label=config.from_label
        )
        
        if "error" in campaign:
            print(f"  ❌ Campaign creation failed")
            return template, campaign
        
        campaign_id = campaign.get("data", {}).get("id")
        message_id = campaign.get("data", {}).get("relationships", {}).get("campaign-messages", {}).get("data", [{}])[0].get("id")
        
        print(f"  ✅ Campaign created: {campaign_id}")
        print(f"  📧 Message ID: {message_id}")
        
        # 3. Print manual linking instructions
        print(f"\n⚠️  MANUAL STEP REQUIRED:")
        print(f"   1. Go to: https://www.klaviyo.com/campaigns")
        print(f"   2. Open campaign: '{config.name} | {config.send_date}'")
        print(f"   3. Click 'Edit Content'")
        print(f"   4. Select template: '{template_name}'")
        
        return template, campaign
    
    def duplicate_campaign(self, campaign_id: str, new_name: str, 
                          new_send_date: str) -> Dict:
        """Duplicate existing campaign with new date"""
        # Get original campaign
        original = self.get_campaign(campaign_id)
        if "error" in original:
            return original
        
        attrs = original.get("data", {}).get("attributes", {})
        messages = original.get("data", {}).get("relationships", {}).get("campaign-messages", {}).get("data", [])
        
        # Get message content from first message
        message_content = {}
        if messages:
            msg = self.get_message(messages[0].get("id"))
            message_content = msg.get("data", {}).get("attributes", {}).get("content", {})
        
        # Create new campaign
        return self.create_campaign(
            name=new_name,
            list_id=attrs.get("audiences", {}).get("included", [""])[0],
            subject=message_content.get("subject", ""),
            preview_text=message_content.get("preview_text", ""),
            send_datetime=f"{new_send_date}T09:00:00Z",
            from_email=message_content.get("from_email", "hello@razeco.de"),
            from_label=message_content.get("from_label", "Razeco")
        )
    
    def get_campaign_report(self, campaign_id: str) -> Dict:
        """Get campaign metrics/reports"""
        campaign = self.get_campaign(campaign_id)
        if "error" in campaign:
            return campaign
        
        attrs = campaign.get("data", {}).get("attributes", {})
        return {
            "name": attrs.get("name"),
            "status": attrs.get("status"),
            "created_at": attrs.get("created_at"),
            "updated_at": attrs.get("updated_at"),
            "send_strategy": attrs.get("send_strategy"),
            "tracking": attrs.get("tracking_options")
        }


# ============ CLI INTERFACE ============

def main():
    """CLI for Klaviyo Campaign Manager"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Klaviyo Campaign Manager")
    parser.add_argument("--api-key", default=os.getenv("KLAVIYO_API_KEY"),
                       help="Klaviyo API Key")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List resources")
    list_parser.add_argument("resource", choices=["templates", "campaigns", "lists", "images"])
    
    # Create campaign command
    create_parser = subparsers.add_parser("create", help="Create newsletter")
    create_parser.add_argument("--name", required=True)
    create_parser.add_argument("--subject", required=True)
    create_parser.add_argument("--preview", required=True)
    create_parser.add_argument("--date", required=True, help="YYYY-MM-DD")
    create_parser.add_argument("--time", default="09:00")
    create_parser.add_argument("--html-file", required=True)
    create_parser.add_argument("--text-file")
    create_parser.add_argument("--list-id", required=True)
    
    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete resource")
    delete_parser.add_argument("resource", choices=["template", "campaign"])
    delete_parser.add_argument("id", help="Resource ID")
    
    # Report command
    report_parser = subparsers.add_parser("report", help="Get campaign report")
    report_parser.add_argument("campaign_id")
    
    args = parser.parse_args()
    
    if not args.api_key:
        print("❌ Error: API key required. Use --api-key or set KLAVIYO_API_KEY env var")
        return
    
    config = KlaviyoConfig(api_key=args.api_key)
    client = KlaviyoClient(config)
    
    if args.command == "list":
        if args.resource == "templates":
            items = client.list_templates()
            print(f"\n📄 Templates ({len(items)}):")
            for item in items:
                attrs = item.get("attributes", {})
                print(f"   {item.get('id')}: {attrs.get('name')}")
                
        elif args.resource == "campaigns":
            items = client.list_campaigns()
            print(f"\n📨 Campaigns ({len(items)}):")
            for item in items:
                attrs = item.get("attributes", {})
                print(f"   {item.get('id')}: {attrs.get('name')} [{attrs.get('status')}]")
                
        elif args.resource == "lists":
            items = client.list_lists()
            print(f"\n📋 Lists ({len(items)}):")
            for item in items:
                attrs = item.get("attributes", {})
                print(f"   {item.get('id')}: {attrs.get('name')}")
                
        elif args.resource == "images":
            items = client.list_images()
            print(f"\n🖼️  Images ({len(items)}):")
            for item in items[:20]:  # Limit output
                attrs = item.get("attributes", {})
                print(f"   {item.get('id')}: {attrs.get('name')}")
    
    elif args.command == "create":
        with open(args.html_file, 'r') as f:
            html = f.read()
        
        text = ""
        if args.text_file:
            with open(args.text_file, 'r') as f:
                text = f.read()
        else:
            # Generate simple text version
            text = f"{args.subject}\n\nView this email in your browser: https://razeco.de"
        
        newsletter = NewsletterConfig(
            name=args.name,
            subject=args.subject,
            preview_text=args.preview,
            send_date=args.date,
            send_time=args.time,
            html_content=html,
            text_content=text,
            list_id=args.list_id
        )
        
        template, campaign = client.create_newsletter_workflow(newsletter)
        
        if "error" not in template and "error" not in campaign:
            print("\n✅ Success! Summary:")
            print(f"   Template: {template.get('data', {}).get('id')}")
            print(f"   Campaign: {campaign.get('data', {}).get('id')}")
            print(f"   Message:  {campaign.get('data', {}).get('relationships', {}).get('campaign-messages', {}).get('data', [{}])[0].get('id')}")
    
    elif args.command == "delete":
        if args.resource == "template":
            success = client.delete_template(args.id)
            print(f"{'✅' if success else '❌'} Template {args.id}")
        elif args.resource == "campaign":
            success = client.delete_campaign(args.id)
            print(f"{'✅' if success else '❌'} Campaign {args.id}")
    
    elif args.command == "report":
        report = client.get_campaign_report(args.campaign_id)
        print(f"\n📊 Campaign Report: {args.campaign_id}")
        print(json.dumps(report, indent=2, default=str))
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()