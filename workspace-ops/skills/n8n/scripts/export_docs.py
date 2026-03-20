#!/usr/bin/env python3
"""
Export Workflow Documentation for n8n
=====================================
Export workflow as markdown documentation with diagram description.

Usage:
  python3 export_docs.py --workflow-id <id>
  python3 export_docs.py --workflow-id <id> --output docs.md
  python3 export_docs.py --all --output-dir ./docs
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from n8n_api import N8nClient


class WorkflowDocsExporter:
    """Export workflow documentation"""
    
    def __init__(self):
        self.client = N8nClient()
    
    def export_workflow(self, workflow_id):
        """Export a single workflow as markdown documentation"""
        try:
            wf = self.client.get_workflow(workflow_id)
        except Exception as e:
            return {'error': str(e)}
        
        nodes = wf.get('nodes', [])
        connections = wf.get('connections', {})
        
        # Build documentation
        doc = []
        doc.append(f"# {wf.get('name', 'Untitled Workflow')}")
        doc.append("")
        doc.append(f"**Workflow ID:** `{workflow_id}`  ")
        doc.append(f"**Active:** {'✅ Yes' if wf.get('active') else '❌ No'}  ")
        doc.append(f"**Version:** {wf.get('versionId', 'N/A')}  ")
        doc.append(f"**Exported:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        doc.append("")
        
        if wf.get('settings'):
            doc.append("## Settings")
            for key, value in wf['settings'].items():
                doc.append(f"- **{key}:** {value}")
            doc.append("")
        
        # Nodes section
        doc.append("## Nodes")
        doc.append("")
        
        trigger_nodes = []
        regular_nodes = []
        
        for node in nodes:
            node_type = node.get('type', '')
            if 'trigger' in node_type.lower():
                trigger_nodes.append(node)
            else:
                regular_nodes.append(node)
        
        if trigger_nodes:
            doc.append("### Triggers")
            doc.append("")
            for node in trigger_nodes:
                doc.extend(self._describe_node(node))
            doc.append("")
        
        if regular_nodes:
            doc.append("### Processing Nodes")
            doc.append("")
            for node in regular_nodes:
                doc.extend(self._describe_node(node))
            doc.append("")
        
        # Flow diagram
        doc.append("## Flow Diagram")
        doc.append("")
        doc.append("```")
        doc.extend(self._generate_flow_diagram(nodes, connections))
        doc.append("```")
        doc.append("")
        
        # Environment variables
        env_vars = self._extract_env_vars(nodes)
        if env_vars:
            doc.append("## Environment Variables Required")
            doc.append("")
            for var in sorted(env_vars):
                doc.append(f"- `{var}`")
            doc.append("")
        
        # Credentials
        credentials = self._extract_credentials(nodes)
        if credentials:
            doc.append("## Credentials Required")
            doc.append("")
            for cred in sorted(credentials):
                doc.append(f"- {cred}")
            doc.append("")
        
        return '\n'.join(doc)
    
    def _describe_node(self, node):
        """Generate description for a node"""
        lines = []
        lines.append(f"#### {node.get('name', 'Unnamed')}")
        lines.append("")
        lines.append(f"- **Type:** `{node.get('type', 'Unknown')}`")
        lines.append(f"- **Position:** ({node.get('position', [0, 0])[0]}, {node.get('position', [0, 0])[1]})")
        
        # Extract key parameters
        params = node.get('parameters', {})
        if params:
            lines.append("")
            lines.append("**Key Parameters:**")
            for key, value in list(params.items())[:5]:  # Limit to 5 params
                if isinstance(value, str) and len(value) < 100:
                    lines.append(f"- {key}: `{value}`")
                elif isinstance(value, (int, float, bool)):
                    lines.append(f"- {key}: `{value}`")
        
        lines.append("")
        return lines
    
    def _generate_flow_diagram(self, nodes, connections):
        """Generate ASCII flow diagram"""
        lines = []
        
        # Build a simple representation
        lines.append("Flow:")
        
        # Find trigger nodes (starting points)
        trigger_names = [n['name'] for n in nodes if 'trigger' in n.get('type', '').lower()]
        
        if trigger_names:
            lines.append(f"  [Trigger] {' -> '.join(trigger_names[:3])}")
        
        # Follow connections
        processed = set()
        
        def follow_flow(node_name, depth=0):
            if node_name in processed or depth > 10:
                return
            processed.add(node_name)
            
            node_conns = connections.get(node_name, {})
            if isinstance(node_conns, dict):
                for output_type, targets in node_conns.items():
                    if isinstance(targets, list):
                        for target in targets:
                            if isinstance(target, list) and len(target) > 0:
                                target_node = target[0].get('node', 'Unknown')
                                lines.append(f"  {'  ' * depth}{node_name} -> {target_node}")
                                follow_flow(target_node, depth + 1)
        
        for trigger in trigger_names:
            follow_flow(trigger)
        
        return lines
    
    def _extract_env_vars(self, nodes):
        """Extract environment variable references from nodes"""
        env_vars = set()
        
        def search_for_env(obj):
            if isinstance(obj, str):
                # Look for $env. or process.env patterns
                import re
                matches = re.findall(r'\$env\.(\w+)', obj)
                env_vars.update(matches)
            elif isinstance(obj, dict):
                for v in obj.values():
                    search_for_env(v)
            elif isinstance(obj, list):
                for item in obj:
                    search_for_env(item)
        
        for node in nodes:
            search_for_env(node.get('parameters', {}))
            search_for_env(node.get('credentials', {}))
        
        return env_vars
    
    def _extract_credentials(self, nodes):
        """Extract credential types from nodes"""
        credentials = set()
        
        for node in nodes:
            creds = node.get('credentials', {})
            for cred_type in creds.keys():
                credentials.add(cred_type)
        
        return credentials


def main():
    parser = argparse.ArgumentParser(description='Export n8n Workflow Documentation')
    parser.add_argument('--workflow-id', help='Workflow ID to export')
    parser.add_argument('--all', action='store_true', help='Export all workflows')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--output-dir', help='Output directory for multiple exports')
    
    args = parser.parse_args()
    
    exporter = WorkflowDocsExporter()
    
    if args.workflow_id:
        doc = exporter.export_workflow(args.workflow_id)
        
        if 'error' in doc:
            print(f"❌ Error: {doc['error']}")
            sys.exit(1)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(doc)
            print(f"✅ Documentation exported to: {args.output}")
        else:
            print(doc)
    
    elif args.all:
        client = N8nClient()
        workflows = client.list_workflows()
        
        output_dir = Path(args.output_dir or './n8n-docs')
        output_dir.mkdir(exist_ok=True)
        
        print(f"📁 Exporting all workflows to: {output_dir}")
        
        for wf in workflows.get('data', []):
            wf_id = wf.get('id')
            wf_name = wf.get('name', 'untitled').replace(' ', '-').lower()
            
            try:
                doc = exporter.export_workflow(wf_id)
                if 'error' not in doc:
                    filename = output_dir / f"{wf_name}-{wf_id[:8]}.md"
                    with open(filename, 'w') as f:
                        f.write(doc)
                    print(f"  ✅ {wf_name}")
            except Exception as e:
                print(f"  ❌ {wf_name}: {e}")
        
        print(f"\n✅ Export complete!")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
