#!/usr/bin/env python3
"""
Health Monitor for n8n
======================
Continuously monitors workflow health and sends alerts for repeated failures.

Usage:
  python3 monitor_health.py --check-now
  python3 monitor_health.py --daemon --interval 300
  python3 monitor_health.py --workflow-id <id> --alert-threshold 3
"""

import sys
import json
import time
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent))
from n8n_api import N8nClient


class HealthMonitor:
    """Monitor n8n workflow health and alert on issues"""
    
    def __init__(self, alert_threshold=3, history_hours=24):
        self.client = N8nClient()
        self.alert_threshold = alert_threshold
        self.history_hours = history_hours
        self.state_file = Path.home() / '.n8n_health_state.json'
        self.state = self._load_state()
    
    def check_all_workflows(self):
        """Check health of all active workflows"""
        workflows = self.client.list_workflows(active=True)
        health_report = []
        
        for workflow in workflows.get('data', []):
            wf_id = workflow.get('id')
            wf_name = workflow.get('name')
            
            # Get recent executions
            executions = self.client.list_executions(
                workflow_id=wf_id,
                limit=20
            )
            
            exec_data = executions.get('data', [])
            if not exec_data:
                continue
            
            # Calculate health metrics
            total = len(exec_data)
            failed = sum(1 for e in exec_data if e.get('status') == 'error')
            success = sum(1 for e in exec_data if e.get('status') == 'success')
            
            # Calculate failure rate
            failure_rate = (failed / total * 100) if total > 0 else 0
            
            # Determine health status
            if failure_rate == 0:
                health = 'healthy'
            elif failure_rate < 20:
                health = 'warning'
            elif failure_rate < 50:
                health = 'critical'
            else:
                health = 'failing'
            
            # Check for consecutive failures
            consecutive_failures = self._count_consecutive_failures(exec_data)
            
            # Alert if threshold exceeded
            alert = consecutive_failures >= self.alert_threshold
            
            report = {
                'workflow_id': wf_id,
                'workflow_name': wf_name,
                'health': health,
                'failure_rate': round(failure_rate, 1),
                'total_executions': total,
                'failed': failed,
                'successful': success,
                'consecutive_failures': consecutive_failures,
                'alert': alert,
                'last_execution': exec_data[0].get('startedAt') if exec_data else None
            }
            
            health_report.append(report)
            
            # Update state for tracking
            self._update_alert_state(wf_id, alert, consecutive_failures)
        
        return health_report
    
    def _count_consecutive_failures(self, executions):
        """Count consecutive failures from most recent"""
        count = 0
        for exec in executions:
            if exec.get('status') == 'error':
                count += 1
            else:
                break
        return count
    
    def _update_alert_state(self, workflow_id, alert_triggered, consecutive_failures):
        """Track alert state to avoid spam"""
        now = datetime.now().isoformat()
        
        if workflow_id not in self.state:
            self.state[workflow_id] = {
                'last_alert': None,
                'alert_count': 0,
                'consecutive_failures': 0
            }
        
        wf_state = self.state[workflow_id]
        
        if alert_triggered:
            # Only alert if it's a new failure streak or 1 hour passed
            last_alert = wf_state.get('last_alert')
            should_alert = True
            
            if last_alert:
                last_time = datetime.fromisoformat(last_alert)
                if datetime.now() - last_time < timedelta(hours=1):
                    should_alert = False
            
            if should_alert:
                wf_state['last_alert'] = now
                wf_state['alert_count'] += 1
        
        wf_state['consecutive_failures'] = consecutive_failures
        self._save_state()
    
    def _load_state(self):
        """Load alert state from disk"""
        if self.state_file.exists():
            try:
                with open(self.state_file) as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def _save_state(self):
        """Save alert state to disk"""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2, default=str)
    
    def send_alert(self, workflow_id, workflow_name, failures, failure_rate):
        """
        Send alert notification.
        Override this method or use webhook to integrate with your notification system.
        """
        alert_msg = f"""
🚨 n8n Workflow Alert

Workflow: {workflow_name}
ID: {workflow_id}
Status: FAILING
Consecutive Failures: {failures}
Failure Rate: {failure_rate}%

Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Please check the workflow execution logs.
"""
        print(alert_msg)
        
        # Could integrate with:
        # - Telegram Bot (@adsdrop_brainbot)
        # - Email
        # - Slack webhook
        # - Push notification
        
        return alert_msg
    
    def run_daemon(self, interval=300):
        """Run continuous monitoring"""
        print(f"👁️  Health Monitor started")
        print(f"   Check interval: {interval}s")
        print(f"   Alert threshold: {self.alert_threshold} consecutive failures")
        print(f"   Press Ctrl+C to stop\n")
        
        try:
            while True:
                print(f"🔍 Checking at {datetime.now().strftime('%H:%M:%S')}...")
                
                report = self.check_all_workflows()
                
                # Print summary
                healthy = sum(1 for r in report if r['health'] == 'healthy')
                warning = sum(1 for r in report if r['health'] == 'warning')
                critical = sum(1 for r in report if r['health'] in ['critical', 'failing'])
                
                print(f"   Healthy: {healthy} | Warning: {warning} | Critical: {critical}")
                
                # Send alerts for critical workflows
                for r in report:
                    if r['alert']:
                        self.send_alert(
                            r['workflow_id'],
                            r['workflow_name'],
                            r['consecutive_failures'],
                            r['failure_rate']
                        )
                
                print(f"   Next check in {interval}s...\n")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n👋 Monitor stopped")


def main():
    parser = argparse.ArgumentParser(description='n8n Health Monitor')
    parser.add_argument('--check-now', action='store_true', help='Run one health check')
    parser.add_argument('--daemon', action='store_true', help='Run continuously')
    parser.add_argument('--interval', type=int, default=300, help='Check interval in seconds')
    parser.add_argument('--workflow-id', help='Check specific workflow only')
    parser.add_argument('--alert-threshold', type=int, default=3, 
                        help='Consecutive failures before alert')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    monitor = HealthMonitor(alert_threshold=args.alert_threshold)
    
    if args.check_now:
        if args.workflow_id:
            # Check specific workflow
            executions = monitor.client.list_executions(
                workflow_id=args.workflow_id,
                limit=20
            )
            exec_data = executions.get('data', [])
            failed = sum(1 for e in exec_data if e.get('status') == 'error')
            total = len(exec_data)
            rate = (failed / total * 100) if total > 0 else 0
            consecutive = monitor._count_consecutive_failures(exec_data)
            
            result = {
                'workflow_id': args.workflow_id,
                'total_executions': total,
                'failed': failed,
                'failure_rate': round(rate, 1),
                'consecutive_failures': consecutive,
                'health': 'failing' if consecutive >= args.alert_threshold else 'ok'
            }
            
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"Health Check: {args.workflow_id}")
                print(f"  Executions: {total}")
                print(f"  Failed: {failed}")
                print(f"  Failure Rate: {rate:.1f}%")
                print(f"  Consecutive Failures: {consecutive}")
        else:
            # Check all workflows
            report = monitor.check_all_workflows()
            if args.json:
                print(json.dumps(report, indent=2))
            else:
                print(f"📊 Health Report ({len(report)} workflows)")
                print("=" * 60)
                for r in report:
                    icon = {"healthy": "🟢", "warning": "🟡", "critical": "🟠", "failing": "🔴"}.get(r['health'], "⚪")
                    print(f"{icon} {r['workflow_name']}")
                    print(f"   Health: {r['health'].upper()}")
                    print(f"   Failure Rate: {r['failure_rate']}% ({r['failed']}/{r['total_executions']})")
                    if r['consecutive_failures'] > 0:
                        print(f"   Consecutive Failures: {r['consecutive_failures']}")
                    print()
    
    elif args.daemon:
        monitor.run_daemon(interval=args.interval)
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
