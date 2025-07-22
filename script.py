#!/usr/bin/env python3
"""
EHB-5 Project Script
This is a sample Python script for the EHB-5 project.
"""

import json


def load_config():
    """Load configuration from config.json"""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"error": "Config file not found"}


def process_data():
    """Process data from data.txt"""
    try:
        with open('data.txt', 'r') as f:
            data = f.read()
        return data
    except FileNotFoundError:
        return "Data file not found"


def main():
    """Main function"""
    print("EHB-5 Project Script")
    print("=" * 20)

    # Load configuration
    config = load_config()
    print(f"Project: {config.get('project', 'Unknown')}")
    print(f"Version: {config.get('version', 'Unknown')}")

    # Process data
    data = process_data()
    print(f"Data loaded: {len(data)} characters")

    print("Script completed successfully!")


if __name__ == "__main__":
    main()