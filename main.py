import csv
import json
import sys
import os

def detect_file_type(file_path):
    _, extension = os.path.splitext(file_path)
    extension = extension.lower()
    if(extension == ".txt"):
        return 'txt'
    elif(extension == ".csv"):
        return "csv"
    elif(extension == ".json"):
        return "json"
    else:
        return None

def inspect_csv(file_path):
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        records = list(reader)
        lenght = len(records)
        col = reader.fieldnames

        missing_count = {}
        for column in col:
            missing_count[column] = 0
        for record in records:
            for column in col:
                if is_missing(record[column]):
                    missing_count[column] += 1

    
        print("File type: CSV")
        print(f"Rows: {lenght}")
        print(f"Columns: {len(col)}")
        print(f"Column Names: {', '.join(col)}")

        print()
        print("Preview:")
        print_preview(records, col)
        print()
        print("Missing Values:")
        for column in col:
            print(f"{column}: {missing_count[column]}")
        
        
     
    

def inspect_json(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
        
        if not isinstance(data, list):
            print("JSON file does not contain a list of dictionaries.")
            return
        for record in data:
            if not isinstance(record, dict):
                print("JSON file does not contain a list of dictionaries.")
                return
        print("File type: JSON")
        lenght = len(data)
        print(f"Records: {lenght}")
        keys = []
        for record in data:
            for key in record:
                if key not in keys:
                    keys.append(key)
        missing_counts = {}

        for key in keys:
            missing_counts[key] = 0
        for record in data:
            for key in keys:
                if key not in record or is_missing(record[key]):
                    missing_counts[key] += 1
        
        print()
        print("Preview:")
        print_preview(data, keys)

        print()
        print("Missing values:")

        for key in keys:
              print(f"{key}: {missing_counts[key]}")
        
        


def inspect_txt(file_path):
    
    with open(file_path, "r") as f:
        content = f.read()
        lines = content.splitlines()
        words = content.split()

        print("File type: TXT")
        print(f"Lines: {len(lines)}")
        print(f"Words: {len(words)}")
        print(f"Characters: {len(content)}")

    

def is_missing(value):
    if value is None:
        return True
    if isinstance(value, str):
        if value.strip() == "":
            return True
    
    return False

def print_preview(records, keys, limit=3):
    n = 0
    for record in records[:limit]:
        n += 1
        print(f"{n}. ", end ="")
        for i, key in enumerate(keys):
            value = ""
            if key not in record:
                value = "MISSING"
            elif is_missing(record[key]):
                value = "MISSING"
            else:
                value = record[key]
            if i < len(keys) - 1:
                print(f"{key}={value}, ", end="")
            else:
                print(f"{key}={value}", end="")
            
        print("")
            
            

    


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <file_path>")
        return
    
    file_path = sys.argv[1]
    file_type = detect_file_type(file_path)
    if file_type is None:
        print("Error: Unsupported file type.")
        print("Supported file types: .txt, .csv, .json")
        return
    
    
    if not os.path.exists(file_path):
        print("Error: File does not exist.")
        return  
    if os.path.getsize(file_path) == 0:
        print("Error: File is empty.")
        return
    if file_type == "csv":
      inspect_csv(file_path)
    elif file_type == "json":
      inspect_json(file_path)
    elif file_type == "txt":
       inspect_txt(file_path)
    
    
    
    


    
    
    
    
    

main()