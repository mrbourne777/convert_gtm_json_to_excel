import json
import pandas as pd
from datetime import datetime
import os

# Load the GTM JSON file
def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

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
        tag_name = tag.get('name', 'N/A')
        tag_type = tag.get('type', 'N/A')
        
        # Retrieve firing triggers by ID
        firing_triggers = [trigger['name'] for trigger in triggers if trigger['triggerId'] in tag.get('firingTriggerId', [])]
        blocking_triggers = [trigger['name'] for trigger in triggers if trigger['triggerId'] in tag.get('blockingTriggerId', [])]
        
        tag_data.append([tag_name, tag_type, ', '.join(firing_triggers), ', '.join(blocking_triggers)])
    
    # Prepare data for the second sheet: Triggers (Name, ID)
    trigger_data = []
    for trigger in triggers:
        trigger_data.append([trigger.get('name', 'N/A'), trigger.get('triggerId', 'N/A')])

    # Variables
    variable_data = []
    for variable in variables:
        variable_data.append([variable.get('name', 'N/A'), variable.get('variableId', 'N/A'), variable.get('type', 'N/A')])
    
    # Convert to DataFrames for Excel output
    tag_df = pd.DataFrame(tag_data, columns=['Tag Name', 'Tag Type', 'Firing Triggers', 'Blocking Triggers'])
    trigger_df = pd.DataFrame(trigger_data, columns=['Trigger Name', 'Trigger ID'])
    variable_df = pd.DataFrame(variable_data, columns=['Variable Name', 'Variable ID', 'Variable Type'])

    # Convert to DataFrames for Excel output
    tag_df = pd.DataFrame(tag_data, columns=['Tag Name', 'Tag Type', 'Firing Triggers', 'Blocking Triggers'])
    trigger_df = pd.DataFrame(trigger_data, columns=['Trigger Name', 'Trigger ID'])
    variable_df = pd.DataFrame(variable_data, columns=['Variable Name', 'Variable ID', 'Variable Type'])
    
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
json_file = 'containers/your_file_name_here.json'  # Change this to the path of your GTM container JSON file

# Execute the script
main(json_file)
