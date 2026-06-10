# Python Data Inspector CLI

A command-line Python program that inspects CSV, JSON, and TXT files using only the Python standard library.

## Features

- Detects file type by extension
- Supports `.csv`, `.json`, and `.txt`
- Handles missing files
- Handles empty files
- Handles invalid JSON
- Rejects unsupported file types
- Counts CSV rows and columns
- Detects missing CSV values
- Validates JSON as a list of dictionaries
- Detects missing JSON keys and values
- Counts TXT lines, words, and characters

## Usage

```bash
python data_inspector.py people.csv
python data_inspector.py people.json
python data_inspector.py notes.txt


File type: CSV
Rows: 4
Columns: 3
Column names: name, age, city

Preview:
1. name=Ali, age=22, city=Toronto
2. name=Sara, age=29, city=Vancouver
3. name=John, age=35, city=Calgary

Missing values:
name: 0
age: 0
city: 0