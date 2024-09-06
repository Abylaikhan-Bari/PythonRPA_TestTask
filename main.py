import os
import logging
from datetime import datetime
from collections import defaultdict
from logging.handlers import RotatingFileHandler

# Set up logging configuration
log_file = 'file_categorization.log'
log_handler = RotatingFileHandler(log_file, maxBytes=5000000, backupCount=5)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[log_handler])

# Global variables to hold filter criteria
MIN_SIZE = None
MODIFIED_AFTER = None
FILTER_EXTENSION = None

def categorize_files_by_type(folder_path):
    logging.info(f"Starting to categorize files in the folder: {folder_path}")

    # Check if the provided folder path exists and is a directory
    if not os.path.exists(folder_path):
        logging.error(f"Folder '{folder_path}' does not exist.")
        raise FileNotFoundError(f"Folder '{folder_path}' does not exist.")
    if not os.path.isdir(folder_path):
        logging.error(f"'{folder_path}' is not a directory.")
        raise NotADirectoryError(f"'{folder_path}' is not a directory.")

    # Dictionary to keep track of files, organized by their extension
    file_dict = defaultdict(list)

    # Walk through the directory tree
    for root, _, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)

            # Get the last modified time of each file
            modified_time = datetime.fromtimestamp(os.path.getmtime(full_path))
            logging.debug(f"Processing file: {full_path}, Last modified: {modified_time}")

            # Apply size filter if specified
            if MIN_SIZE:
                file_size = os.path.getsize(full_path)
                if file_size < MIN_SIZE:
                    logging.debug(f"Skipping file: {full_path}, as its size is less than {MIN_SIZE} bytes")
                    continue

            # Apply modification date filter if specified
            if MODIFIED_AFTER:
                if modified_time < MODIFIED_AFTER:
                    logging.debug(f"Skipping file: {full_path}, as it was modified before {MODIFIED_AFTER}")
                    continue

            # Apply file extension filter if specified
            if FILTER_EXTENSION:
                file_ext = os.path.splitext(file)[1] or ''
                if file_ext != FILTER_EXTENSION:
                    logging.debug(f"Skipping file: {full_path}, as its extension does not match {FILTER_EXTENSION}")
                    continue

            # Extract file extension (use empty string for files without an extension)
            file_ext = os.path.splitext(file)[1] or ''

            # Add the file to our dictionary, grouped by its extension
            file_dict[file_ext].append((full_path, modified_time.strftime('%d.%m.%Y')))

    logging.info(f"File categorization complete. Found {len(file_dict)} different file types.")
    return file_dict

def main():
    global MIN_SIZE, MODIFIED_AFTER, FILTER_EXTENSION

    # Get folder path from the user
    folder_path = input("Please enter the folder path: ").strip()

    # Get filtering criteria from the user
    min_size_input = input("Enter minimum file size in bytes (or leave blank to skip size filter): ").strip()
    MIN_SIZE = int(min_size_input) if min_size_input else None

    modified_after_input = input("Enter last modified date (DD.MM.YYYY) or leave blank to skip date filter: ").strip()
    if modified_after_input:
        try:
            # Parse the date from user input
            MODIFIED_AFTER = datetime.strptime(modified_after_input, '%d.%m.%Y')
        except ValueError:
            print("Invalid date format. Ignoring the last modified filter.")
            MODIFIED_AFTER = None

    filter_extension_input = input("Enter file extension to filter (e.g., .txt) or leave blank to skip extension filter: ").strip()
    FILTER_EXTENSION = filter_extension_input if filter_extension_input else None

    try:
        # Categorize files based on the criteria
        categorized_files = categorize_files_by_type(folder_path)

        # Format the categorized files for output
        output = {}
        for ext, files in categorized_files.items():
            output[ext] = [f"{file} (Last modified: {modified_time})" for file, modified_time in files]

        # Print the categorized files in a readable format
        print("{")
        for ext, file_list in output.items():
            print(f"  '{ext}': {file_list},")
        print("}")
    except (FileNotFoundError, NotADirectoryError) as e:
        print(e)

if __name__ == "__main__":
    main()
