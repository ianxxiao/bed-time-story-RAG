#!/usr/bin/env python3

import os
import sys
from pathlib import Path

def main():
    """
    Main function to run the application.
    """
    # Get the project root directory
    project_root = Path(__file__).parent
    
    # Ensure data and config directories exist
    data_dir = project_root / "data"
    config_dir = project_root / "config"
    
    if not data_dir.exists():
        data_dir.mkdir(parents=True)
    if not config_dir.exists():
        config_dir.mkdir(parents=True)
    
    print("Application started successfully!")

if __name__ == "__main__":
    main() 