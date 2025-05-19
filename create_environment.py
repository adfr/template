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
    
    # Install packages using pip
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade"] + packages)
        print("Environment setup completed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing packages: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = create_environment()
    # Exit with appropriate code
    if success:
        print("Environment setup was successful.")
        sys.exit(0)
    else:
        print("Environment setup failed.")
        sys.exit(1) 