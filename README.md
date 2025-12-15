# TwinCAT Merging JSON

This repository contains a utility for **merging and translating JSON outputs generated from TwinCAT projects**.  
The tool is designed to support automation workflows where multiple TwinCAT JSON exports must be consolidated into a single, structured representation suitable for further processing, configuration management, or analysis.

The project emphasizes **clarity, reproducibility, and practical usability** in industrial automation contexts.

---

## 1. Project Overview

Beckhoff TwinCAT projects often generate structured JSON data that represents configuration parameters, tag definitions, or exported metadata. In real-world workflows, this data may be distributed across multiple files and must be merged or translated before it can be consumed by external tools.

This repository provides:
- A Python-based script for merging TwinCAT JSON files
- Support for command-line execution
- Build artifacts for creating standalone executables

The tool is intended to simplify downstream integration and reduce manual JSON manipulation.

---

## 2. Key Features

- Parsing and validation of TwinCAT-generated JSON files
- Merging of multiple JSON inputs into a single output structure
- Deterministic and repeatable output generation
- Command-line driven execution
- Optional standalone executable generation using PyInstaller

---

## 3. Repository Structure

```text
TwinCAT-Merging-JSON/
├── build/                            # Intermediate build artifacts
├── dist/                             # Standalone executable output
├── TwinCAT_JSON_Merge_Translate.py   # Main JSON merge and translation script
├── TwinCAT_JSON_Merge_Translate.spec # PyInstaller specification file
└── README.md                         # Project documentation
```

---

## 4. Requirements

The following software is required to use this project:

- Python 3.7 or newer
- Standard Python libraries (`json`, `os`, `sys`)
- Optional: PyInstaller (for building standalone executables)

No external third-party dependencies are required for basic operation.

---

## 5. Installation

Clone the repository:

```bash
git clone https://github.com/Vinit-Pimpale/TwinCAT-Merging-JSON.git
cd TwinCAT-Merging-JSON
```

It is recommended to use a Python virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate    # Windows
```

---

## 6. Usage

The main entry point is:

```bash
python TwinCAT_JSON_Merge_Translate.py <input_file_1.json> <input_file_2.json> ...
```

The script reads the provided JSON files, applies the merge logic, and produces a consolidated JSON output.

### Example

```bash
python TwinCAT_JSON_Merge_Translate.py tc_export_1.json tc_export_2.json > merged_output.json
```

This command merges multiple TwinCAT JSON exports into a single JSON document.

---

## 7. Building a Standalone Executable

A PyInstaller specification file is provided to build a standalone executable.

To build the executable:

```bash
pip install pyinstaller
pyinstaller TwinCAT_JSON_Merge_Translate.spec
```

The resulting executable will be located in the `dist/` directory and can be executed without a Python installation.

---

## 8. Design and Implementation Notes

- Input JSON files are validated before merging
- The merge logic is deterministic to ensure reproducibility
- The script is structured to allow easy extension for additional TwinCAT JSON formats
- Console output is suitable for redirection and pipeline usage

---

## 9. Limitations

- No schema enforcement beyond basic JSON validation
- No graphical user interface
- Merge strategy is fixed unless modified in code

These limitations are acceptable for a lightweight utility tool.

---

## 10. Future Improvements

Possible future extensions include:
- Configurable merge strategies
- JSON schema validation against TwinCAT definitions
- Logging and verbosity control
- Integration with TwinCAT ADS or PLC data export pipelines

---

## 11. Author

**Vinit Pimpale**

This tool was developed to support JSON handling and automation data integration in TwinCAT-based industrial environments.
