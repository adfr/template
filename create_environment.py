#!/usr/bin/env python3
"""
Set up a Python environment with required dependencies using uv.
This is typically the first job in the workflow.
"""
import os
import subprocess
import sys
import shutil

def create_environment():
    print("Creating Python environment using uv...")
    
    # Environment name
    env_name = "project_env"
    
    # Check if uv is installed, install if not
    try:
        subprocess.run(["uv", "--version"], check=True, capture_output=True)
        print("uv is already installed.")
    except (subprocess.SubprocessError, FileNotFoundError):
        print("uv not found. Installing uv...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "uv"])
            print("uv installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing uv: {e}")
            return False
    
    # Get current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to requirements.txt file
    requirements_file = os.path.join(current_dir, "requirements.txt")
    
    # Check if requirements.txt exists
    if not os.path.exists(requirements_file):
        print(f"Error: {requirements_file} not found.")
        return False
    
    # Check if the environment already exists
    env_path = os.path.join(current_dir, env_name)
    if os.path.exists(env_path):
        print(f"Environment {env_name} already exists. Removing it to create a fresh one.")
        try:
            shutil.rmtree(env_path)
        except Exception as e:
            print(f"Error removing existing environment: {e}")
            return False
    
    # Create a new virtual environment
    try:
        print(f"Creating new virtual environment: {env_name}")
        subprocess.check_call(["uv", "venv", env_name])
        print(f"Virtual environment '{env_name}' created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating virtual environment: {e}")
        return False
    
    # Install packages from requirements.txt
    try:
        print("Installing packages from requirements.txt...")
        # Get the pip path from the virtual environment
        if sys.platform == "win32":
            uv_cmd = ["uv", "pip", "install", "-r", requirements_file, "--venv", env_name]
        else:
            uv_cmd = ["uv", "pip", "install", "-r", requirements_file, "--venv", env_name]
        
        subprocess.check_call(uv_cmd)
        print("Packages installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing packages: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = create_environment()
    
    # List all installed packages
    if success:
        print("\nListing all installed packages in project_env:")
        env_python = os.path.join(os.path.dirname(os.path.abspath(__file__)), "project_env", 
                                "bin" if sys.platform != "win32" else "Scripts", "python")
        subprocess.run([env_python, "-m", "pip", "list"])
        print("\nEnvironment setup was successful.")
        sys.exit(0)
    else:
        print("\nEnvironment setup failed.")
        sys.exit(1)