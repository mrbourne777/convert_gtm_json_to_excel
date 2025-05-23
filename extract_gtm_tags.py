import argparse
import os
from utils import load_json, load_config_yaml, process_gtm_data, save_to_excel
from datetime import datetime

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract GTM tags, triggers, and variables into Excel.")
    parser.add_argument('--json', required=True, help='GTM container JSON file (inside containers/)')
    args = parser.parse_args()

    json_file = os.path.join('containers', args.json)
    base_filename = os.path.splitext(os.path.basename(json_file))[0]
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    output_excel_file = f'excel/{base_filename}_{timestamp}.xlsx'

    json_data = load_json(json_file)
    config = load_config_yaml('config/mappings.yaml')
    
    tag_df, trigger_df, variable_df = process_gtm_data(json_data, config)
    save_to_excel(tag_df, trigger_df, variable_df, output_excel_file)
    
    print(f"✅ Excel saved to {output_excel_file}")
