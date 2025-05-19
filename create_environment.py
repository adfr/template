#!/usr/bin/env python3
"""
Set up a Python environment with required dependencies.
This is typically the first job in the workflow.
"""
import os
import subprocess
import sys

def create_environment():
    print("Creating Python environment...")
    
    # Define packages to install
    packages = [
        "numpy",
        "pandas",
        "scikit-learn",
        "matplotlib",
        "cmlapi"
    ]
    
    try:
        # Install packages using pip
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade"] + packages)
        print(f"Successfully installed packages: {', '.join(packages)}")
        
        return True
    except Exception as e:
        print(f"Error creating environment: {str(e)}")
        return False

if __name__ == "__main__":
    success = create_environment()
    sys.exit(0 if success else 1) 