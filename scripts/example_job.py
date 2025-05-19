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
        # Hard-coded path to the hello_world.py script
        hello_world_script = "template/scripts/hello_world.py"
        
        # Check if the script exists
        if not os.path.exists(hello_world_script):
            raise FileNotFoundError(f"Could not find hello_world.py at {hello_world_script}")
        
        # Command to activate environment and run script
        cmd = f"python {hello_world_script} "
        
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
