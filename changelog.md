# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2025-05-23
### Major release
- **Modularized Script Logic**
  - Extracted all reusable logic into `utils.py`
  - Main script (`extract_gtm_tags.py`) now serves as a clean CLI entry point

- **YAML-Based Configuration**
  - Moved `variable_type_dict` and built-in triggers to `config/mappings.yaml`
  - Allows easier customization and reuse across projects

- **Improved Custom Template Support**
  - Custom tag types prefixed with `cvt_` now resolve to their actual template names
  - Uses regex-based parsing of `templateData` for reliable ID matching

## [0.1.1] - 2025-04-28
### Added
- Added variable types descriptions
  


## [0.1.0] - 2025-04-25
### Added
- Initial commit: Created the script to parse GTM exported container JSON and export it to Excel.
  
