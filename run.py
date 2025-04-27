#!/usr/bin/env python3

import os
import sys
from pathlib import Path
from helper import (
    ensure_directory_exists,
    get_raw_data_files,
    get_pdf_files,
    print_file_list
)

def main():
    """
    Main function to run the application.
    """
    # Get the project root directory
    project_root = Path(__file__).parent
    
    # Ensure data and config directories exist
    data_dir = project_root / "data"
    config_dir = project_root / "config"
    
    ensure_directory_exists(data_dir)
    ensure_directory_exists(config_dir)
    
    # Get and print all files in rawData
    all_files = get_raw_data_files()
    print_file_list(all_files, "All files in rawData directory")
    
    # Get and print all PDF files
    pdf_files = get_pdf_files()
    print_file_list(pdf_files, "PDF files in rawData directory")
    
    print("\nApplication started successfully!")

if __name__ == "__main__":
    main() 