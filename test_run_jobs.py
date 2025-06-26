#!/usr/bin/env python3
"""
Local test runner for jobs without CML integration.
Executes jobs locally by running their scripts directly with the configured environment.
"""
import os
import sys
import yaml
import subprocess
import time
from datetime import datetime

def load_config():
    """
    Load the job configuration from the YAML file
    
    Returns:
        dict: The job configuration dictionary
    """
    script_dir = os.getcwd()
    
    possible_paths = [
        os.path.join(script_dir, "config", "jobs_config.yaml"),
        os.path.join(os.path.dirname(script_dir), "config", "jobs_config.yaml"),
    ]
    
    config_path = None
    for path in possible_paths:
        if os.path.exists(path):
            config_path = path
            break
    
    if not config_path:
        raise FileNotFoundError(f"Could not find jobs_config.yaml in any of these locations: {possible_paths}")
    
    print(f"Loading config from: {config_path}")
    
    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
    
    return config['jobs']

def run_script_locally(script_path, arguments="", environment=None, timeout=3600):
    """
    Run a script locally with the specified parameters
    
    Args:
        script_path (str): Path to the script to run
        arguments (str): Command line arguments for the script
        environment (dict): Environment variables to set
        timeout (int): Timeout in seconds
    
    Returns:
        tuple: (success, output, error)
    """
    if not os.path.exists(script_path):
        return False, "", f"Script not found: {script_path}"
    
    # Prepare the command
    cmd = [sys.executable, script_path]
    if arguments:
        # Split arguments properly
        cmd.extend(arguments.split())
    
    # Prepare environment
    env = os.environ.copy()
    if environment:
        env.update(environment)
    
    print(f"Running: {' '.join(cmd)}")
    print(f"Working directory: {os.getcwd()}")
    
    try:
        # Run the script
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
            cwd=os.getcwd()
        )
        
        success = result.returncode == 0
        return success, result.stdout, result.stderr
        
    except subprocess.TimeoutExpired:
        return False, "", f"Script timed out after {timeout} seconds"
    except Exception as e:
        return False, "", f"Error running script: {str(e)}"

def test_run_jobs():
    """
    Test run all jobs locally without CML integration
    """
    print("=== Local Job Test Runner ===")
    print(f"Started at: {datetime.now()}")
    print()
    
    try:
        # Load job configuration
        jobs_config = load_config()
        
        # Track job results
        job_results = {}
        
        # Process jobs in dependency order (create_env first)
        job_order = []
        if "create_env" in jobs_config:
            job_order.append("create_env")
        
        # Add other jobs
        for job_key in jobs_config:
            if job_key != "create_env":
                job_order.append(job_key)
        
        print(f"Found {len(jobs_config)} jobs to test: {', '.join(job_order)}")
        print()
        
        # Run each job
        for job_key in job_order:
            job_config = jobs_config[job_key]
            
            print(f"--- Testing Job: {job_config['name']} ---")
            print(f"Script: {job_config['script']}")
            print(f"Kernel: {job_config.get('kernel', 'python3')}")
            print(f"CPU: {job_config.get('cpu', '1')}")
            print(f"Memory: {job_config.get('memory', '2')} GB")
            print(f"Timeout: {job_config.get('timeout', 3600)} seconds")
            
            if 'arguments' in job_config:
                print(f"Arguments: {job_config['arguments']}")
            if 'environment' in job_config:
                print(f"Environment: {job_config['environment']}")
            if 'schedule' in job_config:
                print(f"Schedule: {job_config['schedule']}")
            
            print()
            
            # Run the job
            start_time = time.time()
            success, stdout, stderr = run_script_locally(
                script_path=job_config['script'],
                arguments=job_config.get('arguments', ''),
                environment=job_config.get('environment', {}),
                timeout=job_config.get('timeout', 3600)
            )
            end_time = time.time()
            duration = end_time - start_time
            
            # Store results
            job_results[job_key] = {
                'success': success,
                'duration': duration,
                'stdout': stdout,
                'stderr': stderr
            }
            
            # Print results
            status = "SUCCESS" if success else "FAILED"
            print(f"Result: {status} (took {duration:.2f} seconds)")
            
            if stdout:
                print("STDOUT:")
                print(stdout)
            
            if stderr:
                print("STDERR:")
                print(stderr)
            
            print("-" * 50)
            print()
            
            # If a job fails, decide whether to continue or stop
            if not success:
                print(f"Job '{job_config['name']}' failed!")
                if job_key == "create_env":
                    print("Environment setup failed - stopping execution")
                    break
                else:
                    print("Continuing with next job...")
        
        # Print summary
        print("=== Test Results Summary ===")
        successful_jobs = [k for k, v in job_results.items() if v['success']]
        failed_jobs = [k for k, v in job_results.items() if not v['success']]
        
        print(f"Total jobs tested: {len(job_results)}")
        print(f"Successful: {len(successful_jobs)}")
        print(f"Failed: {len(failed_jobs)}")
        
        if successful_jobs:
            print(f"Successful jobs: {', '.join(successful_jobs)}")
        
        if failed_jobs:
            print(f"Failed jobs: {', '.join(failed_jobs)}")
        
        total_duration = sum(result['duration'] for result in job_results.values())
        print(f"Total execution time: {total_duration:.2f} seconds")
        
        print(f"Completed at: {datetime.now()}")
        
        # Return success status
        return len(failed_jobs) == 0
        
    except Exception as e:
        print(f"Error during job testing: {str(e)}")
        return False

if __name__ == "__main__":
    try:
        success = test_run_jobs()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nTest execution interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)