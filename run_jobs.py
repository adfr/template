#!/usr/bin/env python3
"""
Main script to set up and run CML jobs based on configuration.
This script reads job definitions from config/jobs_config.yaml and creates them in CML.
"""
import os
import sys
import yaml
import cmlapi
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def load_config():
    """
    Load the job configuration from the YAML file
    
    Returns:
        dict: The job configuration dictionary
    """
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                              "config", "jobs_config.yaml")
    
    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
    
    return config['jobs']

def setup_jobs():
    """
    Set up and create CML jobs based on configurations in config/jobs_config.yaml
    using environment variables from .env file
    
    Returns:
        dict: Mapping of job names to their created job IDs
    """
    # Get parameters from environment variables
    api_host = os.environ.get("CML_API_HOST")
    api_key = os.environ.get("CML_API_KEY")
    project_id = os.environ.get("CML_PROJECT_ID")
    
    # Check if required parameters are available
    if not all([api_host, api_key, project_id]):
        missing = []
        if not api_host:
            missing.append("CML_API_HOST")
        if not api_key:
            missing.append("CML_API_KEY")
        if not project_id:
            missing.append("CML_PROJECT_ID")
            
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
    
    print(f"Setting up jobs for project: {project_id}")
    
    # Load the job configuration
    JOBS_CONFIG = load_config()
    
    # Initialize CML API client
    client = cmlapi.default_client(api_host, api_key)
    
    # Dictionary to map job names to their IDs
    job_id_map = {}
    
    # Process jobs in order (create_env first, then others)
    job_order = ["create_env"] + [job for job in JOBS_CONFIG if job != "create_env"]
    
    for job_key in job_order:
        job_config = JOBS_CONFIG[job_key]
        
        print(f"Creating job: {job_config['name']}")
        
        # Create job request
        job_body = cmlapi.CreateJobRequest()
        
        # Set basic job parameters
        job_body.name = job_config["name"]
        job_body.script = job_config["script"]
        job_body.kernel = job_config.get("kernel", "python3")
        
        # Set resource requirements
        job_body.cpu = job_config.get("cpu", float(os.environ.get("DEFAULT_CPU", 1)))
        job_body.memory = job_config.get("memory", float(os.environ.get("DEFAULT_MEMORY", 1)))
        if "nvidia_gpu" in job_config:
            job_body.nvidia_gpu = job_config["nvidia_gpu"]
        
        # Set timeout
        job_body.timeout = job_config.get("timeout", int(os.environ.get("DEFAULT_TIMEOUT", 3600)))
        
        # Set arguments if provided
        if "arguments" in job_config:
            job_body.arguments = job_config["arguments"]
        
        # Set environment variables if provided
        if "environment" in job_config:
            job_body.environment = job_config["environment"]
        
        # Set attachments if provided
        if "attachments" in job_config:
            job_body.attachments = job_config["attachments"]
        
        # Set scheduling parameters
        if "schedule" in job_config:
            job_body.schedule = job_config["schedule"]
        elif "parent_job_id" in job_config:
            # If this is a dependent job, use the ID from our map
            parent_key = job_config["parent_job_id"]
            if parent_key in job_id_map:
                job_body.parent_job_id = job_id_map[parent_key]
            else:
                print(f"Warning: Parent job '{parent_key}' not found. Job will not be dependent.")
        
        # Create the job
        try:
            job_response = client.create_job(job_body, project_id=project_id)
            job_id = job_response.id
            job_id_map[job_key] = job_id
            print(f"Successfully created job '{job_config['name']}' with ID: {job_id}")
        except Exception as e:
            print(f"Error creating job '{job_config['name']}': {str(e)}")
    
    return job_id_map

if __name__ == "__main__":
    try:
        job_ids = setup_jobs()
        
        print("\nJob setup complete. Created jobs:")
        for job_name, job_id in job_ids.items():
            print(f"- {job_name}: {job_id}")
            
    except ValueError as e:
        print(f"Error: {str(e)}")
        print("\nPlease set the required environment variables in the .env file:")
        print("CML_API_HOST, CML_API_KEY, and CML_PROJECT_ID")
        sys.exit(1)