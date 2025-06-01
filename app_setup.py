#!/usr/bin/env python3
"""
Generic App Setup and Launcher
Automatically installs dependencies and starts the application
Supports both UV and pip package managers
"""

import subprocess
import sys
import os
from pathlib import Path

# Configuration
APP_FILE = "app.py"  # Main application file to run
DEFAULT_PORT = 5000  # Default port for web applications
USE_UV = True  # Set to False to use pip instead

def run_command(command, description):
    """Run a command and print status"""
    print(f"🔧 {description}...")
    result = subprocess.run(command, shell=True)
    if result.returncode == 0:
        print(f"✅ {description} completed")
        return True
    else:
        print(f"❌ {description} failed")
        return False

def check_uv_available():
    """Check if UV package manager is available"""
    return subprocess.run(["uv", "--version"], capture_output=True).returncode == 0

def install_uv():
    """Install UV package manager if not present"""
    if check_uv_available():
        print("✅ UV is already installed")
        return True

    print("📦 Installing UV package manager...")
    return run_command("curl -LsSf https://astral.sh/uv/install.sh | sh", "Installing UV")

def setup_environment_uv():
    """Create virtual environment and install requirements using UV"""
    # Create virtual environment if it doesn't exist
    if not Path(".venv").exists():
        if not run_command("uv venv", "Creating virtual environment with UV"):
            return False
    else:
        print("✅ Virtual environment already exists")

    # Install requirements
    if not Path("requirements.txt").exists():
        print("❌ requirements.txt not found!")
        return False

    return run_command("uv pip install -r requirements.txt", "Installing requirements with UV")

def setup_environment_pip():
    """Create virtual environment and install requirements using pip"""
    # Create virtual environment if it doesn't exist
    if not Path(".venv").exists():
        if not run_command("python -m venv .venv", "Creating virtual environment with venv"):
            return False
    else:
        print("✅ Virtual environment already exists")

    # Install requirements
    if not Path("requirements.txt").exists():
        print("❌ requirements.txt not found!")
        return False

    # Activate environment and install requirements
    if sys.platform == "win32":
        activate_cmd = ".venv\\Scripts\\activate"
        pip_cmd = f"{activate_cmd} && pip install -r requirements.txt"
    else:
        activate_cmd = "source .venv/bin/activate"
        pip_cmd = f"{activate_cmd} && pip install -r requirements.txt"

    return run_command(pip_cmd, "Installing requirements with pip")

def get_python_executable():
    """Get the path to the Python executable in the virtual environment"""
    if sys.platform == "win32":
        venv_python = Path(".venv/Scripts/python.exe")
    else:
        venv_python = Path(".venv/bin/python")
    
    if venv_python.exists():
        return str(venv_python)
    else:
        return "python"

def start_app():
    """Start the application"""
    print(f"🚀 Starting application...")
    print(f"📱 If this is a web app, it may be available at: http://localhost:{DEFAULT_PORT}")
    print("🛑 Press Ctrl+C to stop")
    print("-" * 40)

    python_exec = get_python_executable()
    subprocess.run([python_exec, APP_FILE])

def main():
    """Main setup and launch process"""
    print("🚀 Generic App Setup and Launcher")
    print("=" * 40)

    # Check if we're in the right directory
    if not Path(APP_FILE).exists():
        print(f"❌ {APP_FILE} not found! Run this from the application directory.")
        sys.exit(1)

    # Determine which package manager to use
    package_manager = "UV" if USE_UV else "pip"
    print(f"📦 Using package manager: {package_manager}")

    if USE_UV:
        # Install UV if needed
        if not install_uv():
            print("❌ Failed to install UV, falling back to pip")
            USE_UV = False

    # Setup environment and install requirements
    if USE_UV and check_uv_available():
        success = setup_environment_uv()
    else:
        success = setup_environment_pip()

    if not success:
        print("❌ Failed to setup environment")
        sys.exit(1)

    print("✅ Setup completed!")
    print("-" * 40)

    # Start the application
    start_app()

if __name__ == "__main__":
    main()



''' for flask the app will be 
if __name__ == '__main__':


    # Create templates directory if it doesn't exist
    PORT = os.getenv('CDSW_READONLY_PORT', '8090')
    app.run(host="127.0.0.1", port=int(PORT))
    #app.run(debug=True, host='0.0.0.0', port=5000)
'''