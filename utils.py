import json
import yaml
import pandas as pd
import os
import re

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def load_config_yaml(config_path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def resolve_tag_type(tag_type, custom_templates):
    if tag_type.startswith("cvt_"):
        for tmpl in custom_templates:
            template_data = tmpl.get('templateData', '')
            match = re.search(r'"id"\s*:\s*"' + re.escape(tag_type) + '"', template_data)
            if match:
                return tmpl.get('name', f"Custom Template ({tag_type})")
        return f"Custom Template ({tag_type})"
    return tag_type

def process_gtm_data(json_data, config):
    tags = json_data['containerVersion']['tag']
    triggers = json_data['containerVersion']['trigger']
    variables = json_data['containerVersion']['variable']
    custom_templates = json_data['containerVersion'].get('customTemplate', [])

    # Load from config
    built_in_triggers = config['built_in_triggers']
    variable_type_dict = config['variable_types']

    # Append built-in triggers
    triggers.extend(built_in_triggers)

    tag_data = []
    for tag in tags:
        tag_id = tag.get('tagId', 'N/A')
        tag_name = tag.get('name', 'N/A')
        raw_tag_type = tag.get('type', 'N/A')
        tag_type = resolve_tag_type(raw_tag_type, custom_templates)

        firing_triggers = [trigger['name'] for trigger in triggers if trigger['triggerId'] in tag.get('firingTriggerId', [])]
        blocking_triggers = [trigger['name'] for trigger in triggers if trigger['triggerId'] in tag.get('blockingTriggerId', [])]

        tag_data.append([tag_id, tag_name, tag_type, ', '.join(firing_triggers), ', '.join(blocking_triggers)])

    trigger_data = [[trigger.get('triggerId', 'N/A'), trigger.get('name', 'N/A')] for trigger in triggers]

    variable_data = []
    for variable in variables:
        var_name = variable.get('name', 'N/A')
        var_type = variable.get('type', 'N/A')
        var_description = 'Custom Variable' if var_type.startswith('cvt_') else variable_type_dict.get(var_type, 'Unknown Type')
        variable_data.append([variable.get('variableId', 'N/A'), var_name, var_type, var_description])

    tag_df = pd.DataFrame(tag_data, columns=['Tag ID', 'Tag Name', 'Tag Type', 'Firing Triggers', 'Blocking Triggers'])
    trigger_df = pd.DataFrame(trigger_data, columns=['Trigger ID', 'Trigger Name'])
    variable_df = pd.DataFrame(variable_data, columns=['Variable ID', 'Variable Name', 'Variable Type', 'Variable Description'])

    return tag_df, trigger_df, variable_df

def save_to_excel(tag_df, trigger_df, variable_df, output_file):
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        tag_df.to_excel(writer, sheet_name='Tags', index=False)
        trigger_df.to_excel(writer, sheet_name='Triggers', index=False)
        variable_df.to_excel(writer, sheet_name='Variables', index=False)
