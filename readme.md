# GTM Tag and Trigger Extraction

This project extracts tags and triggers from a GTM container exported in JSON format and outputs them into an Excel file. The tags sheet contains information about each tag, including its name, type, firing triggers, and blocking triggers. The triggers sheet contains the names and IDs of the triggers. The variables sheet contains the names and IDs of the variables.

## Prerequisites

Ensure you have the following software installed:

- Python (version 3.x)
- `pip` (Python package manager)

## Setup Instructions

Follow these steps to set up the project environment:

### 1. Create a Virtual Environment

It's recommended to use a virtual environment to manage project dependencies and avoid version conflicts with other projects.

Run the following commands to create and activate a virtual environment:

**On Windows:**
```bash
python -m venv myenv
myenv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv myenv
source myenv/bin/activate
```

### 2. Install Dependencies

Once the virtual environment is activated, install the necessary dependencies using the requirements.txt file.

```bash
pip install -r requirements.txt
```

### 3. Running the Script
After installing the dependencies, you can run the Python script to process the GTM container JSON file. Make sure to replace the path to your JSON file in the script with the actual path to your GTM exported container file. The JSON exported file must be inside the containers folder. The variable name to change is json_file.

```bash
python extract_gtm_tags.py
```

This will generate an Excel file with two sheets:

Tags: Contains the Tag Name, Tag Type, Firing Triggers, and Blocking Triggers.

Triggers: Contains the Trigger Name and Trigger ID.

## Additional Notes
Make sure your GTM container JSON file is correctly formatted before running the script. Ensure that by exporting your container in the Admin section of your Google Tag Manager property.

This script currently assumes the GTM container is structured in a specific way. If your container structure differs, some modifications may be needed in the script.

The Excel file is saved in the excel directory unless you specify a different path.

## Note on Built-In Triggers

Some built-in triggers, such as **All Pages PageView** and **Initialization - All Pages**, are pre-configured in Google Tag Manager (GTM) and are not included in the exported GTM container JSON by default. These built-in triggers are part of GTM's default setup and are automatically applied to tags in your container.

### Manual Addition of Built-In Triggers

In this script, certain **built-in triggers** (such as **All Pages PageView** and **Initialization - All Pages**) are manually added to the list of triggers. This is necessary because built-in triggers do not appear in the GTM container's exported JSON with trigger IDs.

For example, the following built-in triggers are manually added:

- **All Pages - Page View** (Trigger ID: 2147479553)
- **Initialization - All Pages** (Trigger ID: 2147479573)

These manually added triggers will be included in the output Excel file under the **Triggers** sheet, allowing you to see the corresponding tags and their associated triggers.

### Why Manual Addition?

Built-in triggers like **Page View** and **Click** are not exported with their trigger IDs in the GTM container's JSON. Therefore, we manually include their names and IDs in the script to ensure that they are represented in the final data output.

If you need to add more built-in triggers, simply update the `built_in_triggers` list in the script with the trigger name and corresponding ID.

```python
built_in_triggers = [
    {'name': 'All Pages - Page View', 'triggerId': 2147479553},
    {'name': 'Initialization - All Pages', 'triggerId': 2147479573},
    # Add more built-in triggers here if needed
]
