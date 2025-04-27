#!/usr/bin/env python3

from pathlib import Path

def ensure_directory_exists(directory_path):
    """
    Ensure that a directory exists, create it if it doesn't.
    
    Args:
        directory_path (Path): Path object for the directory
        
    Returns:
        bool: True if directory exists or was created, False otherwise
    """
    try:
        if not directory_path.exists():
            directory_path.mkdir(parents=True)
            print(f"Created directory: {directory_path}")
        return True
    except Exception as e:
        print(f"Error creating directory {directory_path}: {e}")
        return False

def get_raw_data_files():
    """
    Get all files from the /data/rawData directory.
    
    Returns:
        list: List of file paths
    """
    raw_data_dir = Path(__file__).parent / "data" / "rawData"
    if ensure_directory_exists(raw_data_dir):
        return list(raw_data_dir.glob("*"))
    return []

def get_pdf_files():
    """
    Get all PDF files from the /data/rawData directory.
    
    Returns:
        list: List of PDF file paths
    """
    raw_data_dir = Path(__file__).parent / "data" / "rawData"
    if ensure_directory_exists(raw_data_dir):
        return list(raw_data_dir.glob("*.pdf"))
    return []

def print_file_list(files, title):
    """
    Print a list of files with a title.
    
    Args:
        files (list): List of file paths
        title (str): Title to print before the list
    """
    print(f"\n{title}:")
    for file in files:
        print(f"- {file.name}") 