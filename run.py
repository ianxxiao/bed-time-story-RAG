#!/usr/bin/env python3

import os
import sys
from pathlib import Path
from helper import (
    ensure_directory_exists,
    get_pdf_files,
    print_file_list
)

from OCR import perform_ocr_file

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

    # Get and print all PDF files
    pdf_files = get_pdf_files()
    print_file_list(pdf_files, "PDF files in rawData directory")

    # Process each PDF through OCR
    print("\nProcessing PDFs through OCR...")

    for pdf_file in pdf_files:

        print(f"\nProcessing {pdf_file.name}...")

        success, error = perform_ocr_file(pdf_file)
        
        if success:
            print(f"Successfully processed {pdf_file.name}")
        else:
            print(f"Failed to process: {pdf_file.name} - {error}")
    
    print("\nApplication ran successfully!")

if __name__ == "__main__":
    main() 