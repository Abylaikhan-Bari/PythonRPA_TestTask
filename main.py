import os
import logging
from collections import defaultdict
from datetime import datetime
from logging.handlers import RotatingFileHandler

# Setup logging
log_file = 'file_categorization.log'
log_handler = RotatingFileHandler(log_file, maxBytes=5000000, backupCount=5)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[log_handler])

def categorize_files_by_type(folder_path):
    # Check if folder_path exists and is a directory
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"'{folder_path}' does not exist.")
    if not os.path.isdir(folder_path):
        raise NotADirectoryError(f"'{folder_path}' is not a directory.")

    # Dictionary to store files by extension
    file_dict = defaultdict(list)

    # Walk through all files and folders in folder_path
    for root, _, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[1] or ''
            file_dict[file_ext].append(full_path)
            logging.info(f"Categorized file: {file}")

    return dict(file_dict)

def main():
    folder_path = input("Enter the folder path: ").strip()

    try:
        # Call categorize_files_by_type and display the result
        result = categorize_files_by_type(folder_path)
        for ext, files in result.items():
            print(f"\nFiles with extension '{ext}':")
            for file in files:
                print(file)
    except (FileNotFoundError, NotADirectoryError) as e:
        print(e)

if __name__ == "__main__":
    main()
