#!/usr/bin/env python3
"""
Check Environment Variables for n8n
====================================
Check if all required environment variables are set for workflows.

Usage:
  python3 check_env.py --workflow-id <id>
  python3 check_env.py --all
  python3 check_env.py --missing-only
"""

import sys
import json
import argparse
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from n8n_api import N8nClient


class EnvChecker:
    """Check environment variables for n8n workflows"""
    
    # Known environment variables used in adsdrop workflows
    KNOWN_VARS = {
        'N8N_API_KEY': 'n8n API Key',
        'N8N_BASE_URL': 'n8n Base URL',
        'AIRTABLE_API_KEY': 'Airtable API Key',
        'AIRTABLE_BASE_ID': 'Airtable Base ID',
        'STRIPE_API_KEY': 'Stripe API Key',
        'STRIPE_WEBHOOK_SECRET': 'Stripe Webhook Secret',
        'KLAVIYO_API_KEY': 'Klaviyo API Key',
        'GOOGLE_SERVICE_ACCOUNT_EMAIL': 'Google Service Account',
        'GOOGLE_PRIVATE_KEY': 'Google Private Key',
        'CLICKUP_API_TOKEN': 'ClickUp API Token',
        'TELEGRAM_BOT_TOKEN': 'Telegram Bot Token',
        'NOTION_API_KEY': 'Notion API Key',
        'SHOPIFY_ACCESS_TOKEN': 'Shopify Access Token',
        'SHOPIFY_SHOP_NAME': 'Shopify Shop Name',
        'META_ACCESS_TOKEN': 'Meta/Facebook Access Token',
        'META_AD_ACCOUNT_ID': 'Meta Ad Account ID',
        'GOOGLE_ADS_DEVELOPER_TOKEN': 'Google Ads Developer Token',
        'GOOGLE_ADS_CUSTOMER_ID': 'Google Ads Customer ID',
        'GOOGLE_ANALYTICS_PROPERTY_ID': 'GA4 Property ID',
        'GTM_CONTAINER_ID': 'GTM Container ID',
    }
    
    def __init__(self):
        self.client = N8nClient()
    
    def check_workflow_env(self, workflow_id):
        """Check environment variables for a specific workflow"""
        try:
            wf = self.client.get_workflow(workflow_id)
        except Exception as e:
            return {'error': str(e)}
        
        nodes = wf.get('nodes', [])
        required_vars = self._extract_env_vars(nodes)
        
        # Also check for credentials that might need env vars
        credential_types = self._extract_credential_types(nodes)
        
        # Map credentials to likely env vars
        cred_to_env = {
            'airtableApi': ['AIRTABLE_API_KEY', 'AIRTABLE_BASE_ID'],
            'stripeApi': ['STRIPE_API_KEY', 'STRIPE_WEBHOOK_SECRET'],
            'klaviyoApi': ['KLAVIYO_API_KEY'],
            'googleApi': ['GOOGLE_SERVICE_ACCOUNT_EMAIL', 'GOOGLE_PRIVATE_KEY'],
            'clickUpApi': ['CLICKUP_API_TOKEN'],
            'telegramApi': ['TELEGRAM_BOT_TOKEN'],
            'notionApi': ['NOTION_API_KEY'],
            'shopifyApi': ['SHOPIFY_ACCESS_TOKEN', 'SHOPIFY_SHOP_NAME'],
            'facebookGraphApi': ['META_ACCESS_TOKEN', 'META_AD_ACCOUNT_ID'],
            'googleAdsApi': ['GOOGLE_ADS_DEVELOPER_TOKEN', 'GOOGLE_ADS_CUSTOMER_ID'],
        }
        
        for cred_type in credential_types:
            if cred_type in cred_to_env:
                required_vars.update(cred_to_env[cred_type])
        
        # Check which are set
        import os
        status = {}
        for var in sorted(required_vars):
            value = os.getenv(var)
            status[var] = {
                'set': value is not None,
                'description': self.KNOWN_VARS.get(var, 'Unknown'),
                'preview': value[:10] + '...' if value and len(value) > 10 else value
            }
        
        return {
            'workflow_id': workflow_id,
            'workflow_name': wf.get('name'),
            'variables': status,
            'all_set': all(s['set'] for s in status.values()),
            'missing': [var for var, s in status.items() if not s['set']]
        }
    
    def check_all_workflows(self):
        """Check environment variables for all workflows"""
        workflows = self.client.list_workflows()
        results = []
        
        all_required = set()
        for wf in workflows.get('data', []):
            wf_id = wf.get('id')
            try:
                wf_detail = self.client.get_workflow(wf_id)
                nodes = wf_detail.get('nodes', [])
                wf_vars = self._extract_env_vars(nodes)
                all_required.update(wf_vars)
            except:
                continue
        
        # Check status of all found variables
        import os
        status = {}
        for var in sorted(all_required):
            value = os.getenv(var)
            status[var] = {
                'set': value is not None,
                'description': self.KNOWN_VARS.get(var, 'Unknown'),
            }
        
        return {
            'total_workflows': len(workflows.get('data', [])),
            'variables_found': len(all_required),
            'variables': status,
            'all_set': all(s['set'] for s in status.values()),
            'missing': [var for var, s in status.items() if not s['set']]
        }
    
    def _extract_env_vars(self, nodes):
        """Extract environment variable names from workflow nodes"""
        env_vars = set()
        
        def search_obj(obj):
            if isinstance(obj, str):
                # Match patterns like $env.VAR_NAME or process.env.VAR_NAME
                patterns = [
                    r'\$env\.(\w+)',
                    r'process\.env\.(\w+)',
                    r'{{\$env\.(\w+)}}',
                ]
                for pattern in patterns:
                    matches = re.findall(pattern, obj)
                    env_vars.update(matches)
            elif isinstance(obj, dict):
                for v in obj.values():
                    search_obj(v)
            elif isinstance(obj, list):
                for item in obj:
                    search_obj(item)
        
        for node in nodes:
            search_obj(node.get('parameters', {}))
            search_obj(node.get('credentials', {}))
            search_obj(node.get('name', ''))
        
        return env_vars
    
    def _extract_credential_types(self, nodes):
        """Extract credential types from nodes"""
        types = set()
        for node in nodes:
            creds = node.get('credentials', {})
            types.update(creds.keys())
        return types


def main():
    parser = argparse.ArgumentParser(description='Check n8n Environment Variables')
    parser.add_argument('--workflow-id', help='Check specific workflow')
    parser.add_argument('--all', action='store_true', help='Check all workflows')
    parser.add_argument('--missing-only', action='store_true', help='Show only missing vars')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    checker = EnvChecker()
    
    if args.workflow_id:
        result = checker.check_workflow_env(args.workflow_id)
        
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
            sys.exit(1)
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"🔍 Environment Check: {result['workflow_name']}")
            print("=" * 60)
            
            if args.missing_only:
                if result['missing']:
                    print(f"\n❌ Missing Variables:")
                    for var in result['missing']:
                        print(f"   - {var}")
                else:
                    print("\n✅ All required variables are set!")
            else:
                print(f"\nVariables ({len(result['variables'])} total):")
                for var, status in result['variables'].items():
                    icon = "✅" if status['set'] else "❌"
                    print(f"   {icon} {var}: {status['description']}")
                
                if result['all_set']:
                    print("\n✅ All required environment variables are set!")
                else:
                    print(f"\n❌ Missing: {', '.join(result['missing'])}")
    
    elif args.all:
        result = checker.check_all_workflows()
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("🔍 Global Environment Check")
            print("=" * 60)
            print(f"Workflows checked: {result['total_workflows']}")
            print(f"Variables found: {result['variables_found']}")
            
            if args.missing_only:
                if result['missing']:
                    print(f"\n❌ Missing Variables:")
                    for var in result['missing']:
                        desc = checker.KNOWN_VARS.get(var, 'Unknown')
                        print(f"   - {var} ({desc})")
            else:
                print(f"\nVariables:")
                for var, status in result['variables'].items():
                    icon = "✅" if status['set'] else "❌"
                    print(f"   {icon} {var}")
                
                if result['all_set']:
                    print("\n✅ All environment variables are set!")
                else:
                    print(f"\n❌ Missing {len(result['missing'])} variables")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
