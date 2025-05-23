# GTM Tag and Trigger Extraction

This project extracts **Tags**, **Triggers**, and **Variables** from a GTM container exported in JSON format and outputs them into an Excel file. The script resolves custom template tag types (e.g., `cvt_`) and uses a YAML-based configuration to manage variable type labels and built-in triggers.

## 📦 Features

- CLI-based execution with `--json` parameter
- Resolves custom tag template IDs to their human-readable names
- Modular codebase with reusable functions
- Configuration-driven using `mappings.yaml`
- Outputs a clean Excel file with the following sheets:
  - **Tags:** Tag ID, Name, Type, Firing Triggers, Blocking Triggers
  - **Triggers:** Trigger ID, Name
  - **Variables:** Variable ID, Name, Type, Description

---

## ✅ Prerequisites

Ensure you have the following installed:

- Python 3.x
- `pip` (Python package manager)

---

## ⚙️ Setup Instructions

### 1. Create a Virtual Environment

**Windows:**
```bash
python -m venv myenv
myenv\Scripts\activate
```
**macOS/Linux:**
```bash
python3 -m venv myenv
source myenv/bin/activate
```
### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
## 🚀 Running the Script

Place your GTM container export file (JSON) into the `containers/` directory.

Run the script with the `--json` argument:

```bash
python extract_gtm_tags.py --json GTM-XXXXXX.json
```
## 📝 Notes on Built-In Triggers

Some default GTM triggers (like **All Pages - Page View**) are not included in JSON exports. These are manually injected using the YAML config.

### Example Built-In Triggers (defined in `config/mappings.yaml`):

```yaml
built_in_triggers:
  - name: All Pages - Page View
    triggerId: '2147479553'
  - name: Initialization - All Pages
    triggerId: '2147479573'
```
## 📌 Example Output Columns

### 🏷️ Tags Sheet
- Tag ID  
- Tag Name  
- Tag Type *(including custom template name)*  
- Firing Triggers  
- Blocking Triggers  

### 🎯 Triggers Sheet
- Trigger ID  
- Trigger Name  

### 🧩 Variables Sheet
- Variable ID  
- Variable Name  
- Variable Type  
- Variable Description  
