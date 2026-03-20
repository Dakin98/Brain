#!/usr/bin/env python3
"""
Error Recovery for n8n
======================
Handles retry logic and auto-recovery for failed workflow executions.

Usage:
  python3 error_recovery.py --list-failed --hours 24
  python3 error_recovery.py --retry --execution-id <id>
  python3 error_recovery.py --auto-retry --workflow-id <id> --max-retries 3
  python3 error_recovery.py --monitor --interval 300
"""

import sys
import json
import time
import argparse
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from n8n_api import N8nClient


class ErrorRecovery:
    """Handle error recovery and retry logic for n8n workflows"""
    
    def __init__(self):
        self.client = N8nClient()
        self.retry_log = Path.home() / '.n8n_retry_log.json'
    
    def get_failed_executions(self, hours=24, workflow_id=None):
        """Get list of failed executions in the last N hours"""
        try:
            # Get executions
            executions = self.client.list_executions(
                workflow_id=workflow_id,
                limit=100
            )
            
            failed = []
            cutoff = datetime.now() - timedelta(hours=hours)
            
            for exec in executions.get('data', []):
                if exec.get('status') == 'error':
                    # Parse execution timestamp
                    started_at = exec.get('startedAt')
                    if started_at:
                        try:
                            exec_time = datetime.fromisoformat(started_at.replace('Z', '+00:00'))
                            if exec_time >= cutoff:
                                failed.append({
                                    'execution_id': exec.get('id'),
                                    'workflow_id': exec.get('workflowId'),
                                    'workflow_name': exec.get('workflowName'),
                                    'started_at': started_at,
                                    'status': exec.get('status'),
                                    'error_message': self._get_error_message(exec.get('id'))
                                })
                        except:
                            failed.append({
                                'execution_id': exec.get('id'),
                                'workflow_id': exec.get('workflowId'),
                                'workflow_name': exec.get('workflowName'),
                                'started_at': started_at,
                                'status': exec.get('status'),
                                'error_message': 'Unknown'
                            })
            
            return failed
            
        except Exception as e:
            return {'error': str(e)}
    
    def _get_error_message(self, execution_id):
        """Get detailed error message from execution"""
        try:
            exec_detail = self.client.get_execution(execution_id)
            # Try to extract error from execution data
            data = exec_detail.get('data', {})
            result_data = data.get('resultData', {})
            run_data = result_data.get('runData', {})
            
            # Look for error in node executions
            for node_name, node_data in run_data.items():
                if isinstance(node_data, list):
                    for run in node_data:
                        if run.get('error'):
                            return run['error'].get('message', 'Unknown error')
            
            return 'No detailed error available'
        except:
            return 'Could not fetch error details'
    
    def retry_execution(self, execution_id, wait_time=5):
        """
        Retry a failed execution by triggering the workflow again.
        Note: We can't retry with same data easily, so we trigger fresh execution.
        """
        try:
            # Get the failed execution to find workflow ID
            exec_detail = self.client.get_execution(execution_id)
            workflow_id = exec_detail.get('workflowId')
            
            if not workflow_id:
                return {'success': False, 'error': 'Could not find workflow ID'}
            
            print(f"🔄 Retrying workflow {workflow_id} (original execution: {execution_id})")
            print(f"   Waiting {wait_time}s before retry...")
            time.sleep(wait_time)
            
            # Trigger new execution
            result = self.client.execute_workflow(workflow_id)
            
            return {
                'success': True,
                'original_execution': execution_id,
                'new_execution': result.get('executionId'),
                'workflow_id': workflow_id
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e), 'original_execution': execution_id}
    
    def auto_retry_workflow(self, workflow_id, max_retries=3, retry_delay=60):
        """
        Automatically retry recent failed executions for a workflow.
        Only retries each unique failure once.
        """
        failed = self.get_failed_executions(hours=1, workflow_id=workflow_id)
        
        if isinstance(failed, dict) and 'error' in failed:
            return failed
        
        # Load retry log to avoid infinite retries
        retry_history = self._load_retry_log()
        
        results = []
        for failure in failed:
            exec_id = failure['execution_id']
            
            # Check if we've already retried this execution enough
            retries = retry_history.get(exec_id, 0)
            if retries >= max_retries:
                print(f"⏭️  Skipping {exec_id} - already retried {retries} times")
                continue
            
            print(f"🔄 Auto-retrying {exec_id} (attempt {retries + 1}/{max_retries})")
            result = self.retry_execution(exec_id, wait_time=retry_delay)
            
            # Update retry log
            retry_history[exec_id] = retries + 1
            results.append(result)
            
            if result['success']:
                print(f"   ✅ New execution: {result['new_execution']}")
            else:
                print(f"   ❌ Failed: {result['error']}")
        
        # Save retry log
        self._save_retry_log(retry_history)
        
        return results
    
    def monitor_and_alert(self, check_interval=300, alert_callback=None):
        """
        Continuously monitor for failures and alert/notify.
        Run this as a background process or cron job.
        """
        print(f"👁️  Starting health monitor (checking every {check_interval}s)")
        print("Press Ctrl+C to stop")
        print()
        
        try:
            while True:
                failed = self.get_failed_executions(hours=1)
                
                if isinstance(failed, dict) and 'error' in failed:
                    print(f"❌ Monitor error: {failed['error']}")
                elif failed:
                    print(f"⚠️  Found {len(failed)} failed executions in last hour:")
                    for f in failed:
                        print(f"   • {f['workflow_name']} ({f['workflow_id']})")
                        print(f"     Error: {f['error_message'][:100]}")
                    
                    if alert_callback:
                        alert_callback(failed)
                else:
                    print(f"✅ {datetime.now().strftime('%H:%M:%S')} - All healthy")
                
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            print("\n👋 Monitor stopped")
    
    def _load_retry_log(self):
        """Load retry history from disk"""
        if self.retry_log.exists():
            try:
                with open(self.retry_log) as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def _save_retry_log(self, data):
        """Save retry history to disk"""
        # Clean old entries (older than 24 hours would need timestamp tracking)
        # For now just keep last 100 entries
        if len(data) > 100:
            # Keep only recent entries (this is simplified)
            data = dict(list(data.items())[-100:])
        
        with open(self.retry_log, 'w') as f:
            json.dump(data, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description='n8n Error Recovery')
    parser.add_argument('--list-failed', action='store_true', help='List failed executions')
    parser.add_argument('--hours', type=int, default=24, help='Hours to look back')
    parser.add_argument('--workflow-id', help='Filter by workflow ID')
    parser.add_argument('--retry', action='store_true', help='Retry a specific execution')
    parser.add_argument('--execution-id', help='Execution ID to retry')
    parser.add_argument('--auto-retry', action='store_true', help='Auto-retry recent failures')
    parser.add_argument('--max-retries', type=int, default=3, help='Max retries per execution')
    parser.add_argument('--retry-delay', type=int, default=60, help='Seconds between retries')
    parser.add_argument('--monitor', action='store_true', help='Continuous monitoring mode')
    parser.add_argument('--interval', type=int, default=300, help='Monitor check interval (seconds)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    recovery = ErrorRecovery()
    
    if args.list_failed:
        failed = recovery.get_failed_executions(args.hours, args.workflow_id)
        if args.json:
            print(json.dumps(failed, indent=2))
        else:
            if isinstance(failed, dict) and 'error' in failed:
                print(f"❌ Error: {failed['error']}")
            else:
                print(f"❌ Failed Executions (last {args.hours}h): {len(failed)}")
                print("=" * 60)
                for f in failed:
                    print(f"\n🔴 {f['workflow_name']}")
                    print(f"   Execution: {f['execution_id']}")
                    print(f"   Workflow: {f['workflow_id']}")
                    print(f"   Time: {f['started_at']}")
                    print(f"   Error: {f['error_message'][:200]}")
    
    elif args.retry:
        if not args.execution_id:
            print("❌ --execution-id required")
            sys.exit(1)
        
        result = recovery.retry_execution(args.execution_id)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if result['success']:
                print(f"✅ Retry successful!")
                print(f"   New execution: {result['new_execution']}")
            else:
                print(f"❌ Retry failed: {result['error']}")
    
    elif args.auto_retry:
        if not args.workflow_id:
            print("❌ --workflow-id required for auto-retry")
            sys.exit(1)
        
        results = recovery.auto_retry_workflow(
            args.workflow_id,
            max_retries=args.max_retries,
            retry_delay=args.retry_delay
        )
        
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            success = sum(1 for r in results if r.get('success'))
            failed = sum(1 for r in results if not r.get('success'))
            print(f"📊 Auto-retry complete: {success} succeeded, {failed} failed")
    
    elif args.monitor:
        recovery.monitor_and_alert(check_interval=args.interval)
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
