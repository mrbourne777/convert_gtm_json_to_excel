import json
import pandas as pd
from datetime import datetime
import os

# Load the GTM JSON file
def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Create a dictionary to map variable types to their descriptive names
variable_type_dict = {
    'v': 'DataLayer Variable',
    'c': 'Constant',
    'gas': 'Google Analytics Setting',
    'u': 'URL',
    'j': 'JavaScript Variable',
    'jsm': 'Custom JavaScript',
    'd': 'DOM Element',
    'k': 'First Party Cookie',
    'remm': 'RegEx Table',
    'aev': 'Auto-Event Variable',
    'awec': 'User-Provided Data',
    'smm': 'Lookup Table',
    'gtcs': 'Google Tag Configuration Setting',
    'gtes': 'Google Tag Event Setting',
}

# Process the GTM data to extract tags and triggers
def process_gtm_data(json_data):
    # Extract tags and triggers
    tags = json_data['containerVersion']['tag']
    triggers = json_data['containerVersion']['trigger']
    variables = json_data['containerVersion']['variable']

    # Manually add built-in triggers (All Pages PageView)
    built_in_triggers = [
        {'name': 'All Pages - Page View', 'triggerId': '2147479553'},
        {'name': 'Initialization - All Pages', 'triggerId': '2147479573'},
        {'name': 'Consent Initialization - All Pages', 'triggerId': '2147479572'},
        # You can add more built-in triggers here if needed
    ]
    # Add the built-in triggers to the list
    triggers.extend(built_in_triggers)
    
    # Prepare data for the first sheet: Tags (Name, Type, Firing Triggers, Blocking Triggers)
    tag_data = []
    for tag in tags:
        tag_id = tag.get('tagId', 'N/A')
        tag_name = tag.get('name', 'N/A')
        tag_type = tag.get('type', 'N/A')
        
        # Retrieve firing triggers by ID
        firing_triggers = [trigger['name'] for trigger in triggers if trigger['triggerId'] in tag.get('firingTriggerId', [])]
        blocking_triggers = [trigger['name'] for trigger in triggers if trigger['triggerId'] in tag.get('blockingTriggerId', [])]
        
        tag_data.append([tag_id, tag_name, tag_type, ', '.join(firing_triggers), ', '.join(blocking_triggers)])
    
    # Prepare data for the second sheet: Triggers (Name, ID)
    trigger_data = []
    for trigger in triggers:
        trigger_data.append([trigger.get('triggerId', 'N/A'), trigger.get('name', 'N/A')])

    # Variables
    variable_data = []
    for variable in variables:
        # Check if the variable starts with 'cvt_'
        var_name = variable.get('name', 'N/A')
        var_type = variable.get('type', 'N/A')

        if var_name.startswith('cvt_'):
            var_description = 'Custom Variable'  # For custom variables
        else:
            var_description = variable_type_dict.get(var_type, 'Unknown Type')

        variable_data.append([variable.get('variableId', 'N/A'), variable.get('name', 'N/A'), variable.get('type', 'N/A'), var_description])
    
    # Convert to DataFrames for Excel output
    tag_df = pd.DataFrame(tag_data, columns=['Tag ID', 'Tag Name', 'Tag Type', 'Firing Triggers', 'Blocking Triggers'])
    trigger_df = pd.DataFrame(trigger_data, columns=['Trigger ID', 'Trigger Name'])
    variable_df = pd.DataFrame(variable_data, columns=['Variable ID', 'Variable Name', 'Variable Type', 'Variable Description'])

    # Convert to DataFrames for Excel output
    tag_df = pd.DataFrame(tag_data, columns=['Tag ID', 'Tag Name', 'Tag Type', 'Firing Triggers', 'Blocking Triggers'])
    trigger_df = pd.DataFrame(trigger_data, columns=['Trigger ID', 'Trigger Name'])
    variable_df = pd.DataFrame(variable_data, columns=['Variable ID', 'Variable Name', 'Variable Type', 'Variable Description'])
    
    return tag_df, trigger_df, variable_df

# Save the data to an Excel file
def save_to_excel(tag_df, trigger_df, variable_df, output_file):
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        tag_df.to_excel(writer, sheet_name='Tags', index=False)
        trigger_df.to_excel(writer, sheet_name='Triggers', index=False)
        variable_df.to_excel(writer, sheet_name='Variables', index=False)

# Main function to run the script
def main(json_file):
    # Extract the base filename (without extension) from the JSON file path
    base_filename = os.path.splitext(os.path.basename(json_file))[0]

    # Generate timestamp for the output filename
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    output_excel_file = f'excel/{base_filename}_{timestamp}.xlsx'  # Output file with timestamp
    
    # Load JSON data
    json_data = load_json(json_file)
    
    # Process the data and get DataFrames
    tag_df, trigger_df, variable_df = process_gtm_data(json_data)
    
    # Save the DataFrames to Excel
    save_to_excel(tag_df, trigger_df, variable_df, output_excel_file)
    print(f"Excel file saved as {output_excel_file}")

# Specify the input and output files
json_file = 'containers/GTM-XXXXXX.json'  # Change this to the name of your GTM container JSON file

# Execute the script
main(json_file)
