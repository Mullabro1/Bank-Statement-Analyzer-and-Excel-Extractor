import os
import json
import csv

def get_script_directory():
    return os.path.dirname(os.path.realpath(__file__))

def clean_text(text):
    """
    Clean the text block:
      - Remove semicolons.
      - Replace newline characters with a single space.
      - Extra spaces are reduced.
    """
    if not text:
        return ""
    # Remove semicolons, replace newlines with space, and clean extra spaces.
    return " ".join(text.replace(";", "").split())

def clean_value(value):
    """
    Convert a cell to string, remove newline characters, remove commas.
    e.g. "10,000.00" becomes "10000.00"
    """
    if value is None:
        return ""
    # Convert to string, remove newline and commas, and strip extra spaces.
    return " ".join(str(value).replace("\n", " ").replace(",", "").split())

def process_json_to_csv(json_path, csv_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Open the CSV file for writing with semicolon delimiter.
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=';')
        
        # Iterate through each page in the JSON.
        for page, page_data in data.items():
            # Write the page number (e.g. "Page_1" becomes "Page 1")
            page_label = page.replace("_", " ")
            csv_writer.writerow([page_label])
            
            # Process and write the text block.
            text_block = page_data.get("text", "")
            cleaned_text_block = clean_text(text_block)
            csv_writer.writerow([cleaned_text_block])
            
            # Process table data if available.
            tables = page_data.get("tables", None)
            if tables and isinstance(tables, list):
                for table in tables:
                    # Ensure table is a non-empty list.
                    if table and isinstance(table, list) and len(table) > 0:
                        # Use the first row as header.
                        header = table[0]
                        csv_writer.writerow([clean_value(cell) for cell in header])
                        
                        # Process remaining rows.
                        for row in table[1:]:
                            csv_writer.writerow([clean_value(cell) for cell in row])
                    # Write an empty row for spacing after each table.
                    csv_writer.writerow([])
            else:
                # If table is null or not present, note it.
                csv_writer.writerow(["No table data available"])
            # Write an empty row after each page.
            csv_writer.writerow([])

# Get script directory and set folder paths.
directory = get_script_directory()
json_folder = os.path.join(directory, "json2")
csv_folder = os.path.join(directory, "csv2")
os.makedirs(csv_folder, exist_ok=True)

# Process each JSON file in the json2 folder.
for filename in os.listdir(json_folder):
    if filename.lower().endswith(".json"):
        json_path = os.path.join(json_folder, filename)
        csv_path = os.path.join(csv_folder, f"{os.path.splitext(filename)[0]}.csv")
        process_json_to_csv(json_path, csv_path)
        print(f"CSV file successfully created at: {csv_path}")
