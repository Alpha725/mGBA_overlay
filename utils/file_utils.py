import json
import os
import csv

def load_json_to_dict(filepath):
    if not os.path.exists(filepath):
        print(f"Error: The file '{filepath}' was not found.")
        return None
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON. {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def load_csv_to_dict(path):
    data = {}
    try:
        with open(path, mode='r', encoding='utf-8') as f:
            for row in csv.reader(f):
                if len(row) >= 2: data[row[0]] = row[1]
    except FileNotFoundError:
        pass
    return data 
