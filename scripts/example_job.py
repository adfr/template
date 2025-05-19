#!/usr/bin/env python3
"""
Example job script that activates a Python environment and runs another script
"""

import subprocess
import os
import sys
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    """
    Main function to activate environment and run hello_world.py
    """
    try:
        # Get the directory of the current script - works in both interactive and file execution modes
        try:
            # When run as a script file
            script_dir = os.path.dirname(os.path.abspath(__file__))
        except NameError:
            # When run in interactive mode
            script_dir = os.path.abspath(os.getcwd())
            logger.info(f"Running in interactive mode. Using current directory: {script_dir}")
        
        # Get the project root directory (parent of script_dir)
        project_root = os.path.dirname(script_dir)
        
        # Path to the hello_world.py script in the expected production location
        hello_world_script = os.path.join(project_root, "template", "scripts", "hello_world.py")
        
        # Check if the script exists
        if not os.path.exists(hello_world_script):
            logger.warning(f"Script not found at expected production location: {hello_world_script}")
            
            # Check possible fallback locations
            possible_paths = [
                os.path.join(script_dir, "hello_world.py"),                    # Same directory as this script
                os.path.join(project_root, "scripts", "hello_world.py"),       # scripts directory in project root
                os.path.join(project_root, "template", "hello_world.py"),      # template directory in project root
                os.path.join(os.path.dirname(project_root), "template", "scripts", "hello_world.py")  # One level up
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    hello_world_script = path
                    logger.info(f"Found script at alternate location: {hello_world_script}")
                    break
            else:
                raise FileNotFoundError(f"Could not find hello_world.py script in any expected location")
        
        # Command to activate environment and run script
        cmd = f"source activate _project_env && python {hello_world_script} --name 'CML User' --repeat 3"
        
        logger.info(f"Running command: {cmd}")
        
        # Execute the command in a shell
        process = subprocess.run(
            cmd,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Print output
        logger.info("Command output:")
        print(process.stdout)
        
        if process.stderr:
            logger.warning("Command stderr:")
            print(process.stderr)
            
        logger.info("Script execution completed successfully")
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Error executing command: {e}")
        logger.error(f"Command stderr: {e.stderr}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
