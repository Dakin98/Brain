#!/usr/bin/env python3
"""
Apply Template for n8n
======================
Apply adsdrop-specific workflow templates with parameters.

Usage:
  python3 apply_template.py --list
  python3 apply_template.py --template closing --name "Kunde XYZ" --airtable-record recXXX
  python3 apply_template.py --template onboarding --name "Kunde ABC"
"""

import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from n8n_api import N8nClient


TEMPLATES_DIR = Path(__file__).parent.parent / 'templates'


class TemplateApplier:
    """Apply workflow templates with parameter substitution"""
    
    def __init__(self):
        self.client = N8nClient()
    
    def list_templates(self):
        """List available templates"""
        templates = []
        if TEMPLATES_DIR.exists():
            for template_file in TEMPLATES_DIR.glob('*.json'):
                try:
                    with open(template_file) as f:
                        data = json.load(f)
                        templates.append({
                            'name': template_file.stem,
                            'file': str(template_file),
                            'description': data.get('description', 'No description'),
                            'parameters': data.get('parameters', [])
                        })
                except:
                    pass
        return templates
    
    def load_template(self, template_name):
        """Load a template by name"""
        template_file = TEMPLATES_DIR / f"{template_name}.json"
        if not template_file.exists():
            raise FileNotFoundError(f"Template not found: {template_name}")
        
        with open(template_file) as f:
            return json.load(f)
    
    def apply_template(self, template_name, parameters, activate=False):
        """
        Apply a template with parameter substitution.
        
        Args:
            template_name: Name of the template (closing, onboarding)
            parameters: Dict of parameters to substitute
            activate: Whether to activate the workflow after creation
        """
        template = self.load_template(template_name)
        
        # Get the workflow structure
        workflow = template.get('workflow', {})
        
        # Substitute parameters in name and nodes
        workflow = self._substitute_params(workflow, parameters)
        
        # Create the workflow
        result = self.client.create_workflow(workflow)
        workflow_id = result.get('id')
        
        if activate and workflow_id:
            self.client.activate_workflow(workflow_id)
        
        return {
            'success': True,
            'workflow_id': workflow_id,
            'workflow_name': result.get('name'),
            'activated': activate,
            'parameters_used': parameters
        }
    
    def _substitute_params(self, obj, params):
        """Recursively substitute parameters in workflow object"""
        if isinstance(obj, str):
            result = obj
            for key, value in params.items():
                placeholder = f"{{{{{key}}}}}"
                result = result.replace(placeholder, str(value))
            return result
        elif isinstance(obj, dict):
            return {k: self._substitute_params(v, params) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._substitute_params(item, params) for item in obj]
        else:
            return obj


def main():
    parser = argparse.ArgumentParser(description='Apply n8n Workflow Templates')
    parser.add_argument('--list', action='store_true', help='List available templates')
    parser.add_argument('--template', help='Template name to apply')
    parser.add_argument('--name', help='Customer/project name')
    parser.add_argument('--airtable-record', help='Airtable record ID')
    parser.add_argument('--airtable-base', default='appbGhxy9I18oIS8E', help='Airtable base ID')
    parser.add_argument('--activate', action='store_true', help='Activate after creation')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    applier = TemplateApplier()
    
    if args.list:
        templates = applier.list_templates()
        if args.json:
            print(json.dumps(templates, indent=2))
        else:
            print("📋 Available Templates:")
            print("=" * 60)
            for t in templates:
                print(f"\n{t['name']}")
                print(f"  File: {t['file']}")
                print(f"  Description: {t['description']}")
                if t['parameters']:
                    print(f"  Parameters: {', '.join(t['parameters'])}")
    
    elif args.template:
        if not args.name:
            print("❌ --name is required")
            sys.exit(1)
        
        # Build parameters
        params = {
            'name': args.name,
            'customer_name': args.name,
        }
        
        if args.airtable_record:
            params['airtable_record'] = args.airtable_record
            params['airtable_base'] = args.airtable_base
        
        try:
            result = applier.apply_template(args.template, params, args.activate)
            
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"✅ Template applied successfully!")
                print(f"   Workflow: {result['workflow_name']}")
                print(f"   ID: {result['workflow_id']}")
                print(f"   Activated: {'Yes' if result['activated'] else 'No'}")
        
        except FileNotFoundError as e:
            print(f"❌ {e}")
            print(f"\nRun with --list to see available templates")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
