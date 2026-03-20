#!/usr/bin/env python3
"""
Webhook Manager for n8n
=======================
Manages webhook registration and status for n8n workflows.

Addresses the known issue: Production webhooks don't reliably register via API,
only formTrigger works consistently.

Usage:
  python3 webhook_manager.py --list
  python3 webhook_manager.py --check --workflow-id <id>
  python3 webhook_manager.py --fix --workflow-id <id>
  python3 webhook_manager.py --fix-all
"""

import sys
import json
import argparse
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from n8n_api import N8nClient


class WebhookManager:
    """Manage n8n webhooks and form triggers"""
    
    def __init__(self):
        self.client = N8nClient()
    
    def list_webhook_workflows(self):
        """Find all workflows with webhook or form trigger nodes"""
        workflows = self.client.list_workflows()
        webhook_workflows = []
        
        for workflow in workflows.get('data', []):
            wf_id = workflow.get('id')
            try:
                wf_detail = self.client.get_workflow(wf_id)
                nodes = wf_detail.get('nodes', [])
                
                for node in nodes:
                    node_type = node.get('type', '')
                    if 'webhook' in node_type.lower() or 'form' in node_type.lower():
                        webhook_workflows.append({
                            'workflow_id': wf_id,
                            'workflow_name': workflow.get('name'),
                            'node_name': node.get('name'),
                            'node_type': node_type,
                            'active': workflow.get('active', False),
                            'webhook_id': node.get('webhookId'),
                            'path': node.get('parameters', {}).get('path'),
                        })
                        break  # Only report once per workflow
                        
            except Exception as e:
                print(f"⚠️  Could not check workflow {wf_id}: {e}")
                continue
        
        return webhook_workflows
    
    def check_webhook_status(self, workflow_id):
        """Check if a workflow's webhook is properly registered"""
        try:
            wf = self.client.get_workflow(workflow_id)
            nodes = wf.get('nodes', [])
            
            webhook_nodes = [n for n in nodes if 'webhook' in n.get('type', '').lower()]
            form_nodes = [n for n in nodes if 'form' in n.get('type', '').lower()]
            
            status = {
                'workflow_id': workflow_id,
                'workflow_name': wf.get('name'),
                'active': wf.get('active', False),
                'webhook_nodes': len(webhook_nodes),
                'form_nodes': len(form_nodes),
                'issues': []
            }
            
            # Check if workflow is active but has no registered webhooks
            if wf.get('active') and (webhook_nodes or form_nodes):
                # Webhooks should auto-register when workflow is activated
                # If they're missing, that's the known n8n bug
                for node in webhook_nodes + form_nodes:
                    if not node.get('webhookId'):
                        status['issues'].append({
                            'node': node.get('name'),
                            'type': node.get('type'),
                            'problem': 'No webhookId assigned - may not be registered',
                            'fix': 'Deactivate and reactivate workflow'
                        })
            
            return status
            
        except Exception as e:
            return {'error': str(e), 'workflow_id': workflow_id}
    
    def fix_webhook(self, workflow_id):
        """
        Fix webhook registration by deactivating and reactivating workflow.
        This is the workaround for the known n8n bug.
        """
        try:
            wf = self.client.get_workflow(workflow_id)
            was_active = wf.get('active', False)
            
            if not was_active:
                return {
                    'workflow_id': workflow_id,
                    'status': 'skipped',
                    'reason': 'Workflow was not active'
                }
            
            print(f"🔧 Fixing webhook for workflow: {wf.get('name')} ({workflow_id})")
            
            # Step 1: Deactivate
            print("  → Deactivating...")
            self.client.deactivate_workflow(workflow_id)
            
            # Step 2: Small delay to ensure cleanup
            import time
            time.sleep(1)
            
            # Step 3: Reactivate (this triggers webhook registration)
            print("  → Reactivating...")
            self.client.activate_workflow(workflow_id)
            
            # Step 4: Verify
            time.sleep(1)
            wf_check = self.client.get_workflow(workflow_id)
            
            return {
                'workflow_id': workflow_id,
                'status': 'fixed',
                'workflow_name': wf.get('name'),
                'active': wf_check.get('active', False),
                'note': 'Webhook should now be registered. Test the endpoint.'
            }
            
        except Exception as e:
            return {
                'workflow_id': workflow_id,
                'status': 'error',
                'error': str(e)
            }
    
    def fix_all_webhooks(self):
        """Fix webhooks for all active workflows with webhook/form triggers"""
        workflows = self.list_webhook_workflows()
        results = []
        
        print(f"🔍 Found {len(workflows)} workflows with webhooks/forms")
        print()
        
        for wf in workflows:
            if wf.get('active'):
                result = self.fix_webhook(wf['workflow_id'])
                results.append(result)
                print()
        
        return results


def main():
    parser = argparse.ArgumentParser(description='n8n Webhook Manager')
    parser.add_argument('--list', action='store_true', help='List all webhook workflows')
    parser.add_argument('--check', action='store_true', help='Check webhook status')
    parser.add_argument('--fix', action='store_true', help='Fix webhook registration')
    parser.add_argument('--fix-all', action='store_true', help='Fix all active webhooks')
    parser.add_argument('--workflow-id', help='Target workflow ID')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    manager = WebhookManager()
    
    if args.list:
        workflows = manager.list_webhook_workflows()
        if args.json:
            print(json.dumps(workflows, indent=2))
        else:
            print(f"📡 Workflows with Webhooks/Forms ({len(workflows)} total)")
            print("=" * 60)
            for wf in workflows:
                status = "🟢" if wf['active'] else "🔴"
                print(f"{status} {wf['workflow_name']}")
                print(f"   ID: {wf['workflow_id']}")
                print(f"   Node: {wf['node_name']} ({wf['node_type']})")
                if wf.get('path'):
                    print(f"   Path: {wf['path']}")
                print()
    
    elif args.check:
        if not args.workflow_id:
            print("❌ --workflow-id required for check")
            sys.exit(1)
        
        status = manager.check_webhook_status(args.workflow_id)
        if args.json:
            print(json.dumps(status, indent=2))
        else:
            print(f"🔍 Webhook Status: {status.get('workflow_name')}")
            print(f"   Active: {'✅' if status.get('active') else '❌'}")
            print(f"   Webhook Nodes: {status.get('webhook_nodes', 0)}")
            print(f"   Form Nodes: {status.get('form_nodes', 0)}")
            if status.get('issues'):
                print(f"\n⚠️  Issues found:")
                for issue in status['issues']:
                    print(f"   • {issue['node']}: {issue['problem']}")
                    print(f"     Fix: {issue['fix']}")
            else:
                print("\n✅ No issues found")
    
    elif args.fix:
        if not args.workflow_id:
            print("❌ --workflow-id required for fix")
            sys.exit(1)
        
        result = manager.fix_webhook(args.workflow_id)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if result.get('status') == 'fixed':
                print(f"✅ Fixed: {result.get('workflow_name')}")
            elif result.get('status') == 'skipped':
                print(f"⏭️  Skipped: {result.get('reason')}")
            else:
                print(f"❌ Error: {result.get('error')}")
    
    elif args.fix_all:
        results = manager.fix_all_webhooks()
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            fixed = sum(1 for r in results if r.get('status') == 'fixed')
            errors = sum(1 for r in results if r.get('status') == 'error')
            print(f"\n{'='*60}")
            print(f"📊 Summary: {fixed} fixed, {errors} errors")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
