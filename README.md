# CML Jobs Template

This template provides a framework for setting up and managing jobs in Cloudera Machine Learning (CML).

## Files Overview

- `config/jobs_config.yaml` - Contains all job configurations and their parameters
- `run_jobs.py` - Main script that reads job configurations and creates them in CML
- `create_environment.py` - First job that sets up the Python environment
- `process_data.py` - Example data processing job 

## How It Works

1. Define all your jobs in `config/jobs_config.yaml` with their parameters, dependencies, and resources
2. The first job is always `create_env` which sets up the Python environment
3. Run the `run_jobs.py` script to create all the jobs in CML

## Usage

```bash
python run_jobs.py <api_host> <api_key> <project_id>
```

Where:
- `api_host` is your CML API host URL (e.g., https://ml-12345.cloud.example.com)
- `api_key` is your CML API key for authentication
- `project_id` is the ID of the project to create jobs in

## Job Configuration

Each job in `config/jobs_config.yaml` has the following structure:

```yaml
jobs:
  job_key:
    name: Human-readable job name
    script: script_to_run.py
    kernel: python3  # or r, scala, etc.
    cpu: 1  # Number of CPU cores
    memory: 2  # Memory in GB
    timeout: 3600  # Timeout in seconds
    environment:
      ENV_VAR: value  # Environment variables
    arguments: --param value  # Command-line arguments
    
    # Either schedule (for cron) or parent_job_id (for dependent jobs)
    schedule: 0 8 * * 1  # Run every Monday at 8 AM
    # OR
    parent_job_id: previous_job_key  # Run after this job completes
    
    # Optional
    nvidia_gpu: 1  # Number of GPUs
    attachments:
      - path/to/file.txt  # Files to attach to emails
```

## Adding New Jobs

1. Define the job in `config/jobs_config.yaml`
2. Create the script file referenced in the job configuration
3. Re-run `run_jobs.py` to create the new job

## Example Workflow

The template includes an example workflow:

1. `create_env` - Sets up the Python environment
2. `data_processing` - Processes data (depends on create_env)
3. `model_training` - Trains a model (depends on data_processing)
4. `scheduled_report` - Generates a weekly report (scheduled job)

You can modify or extend this workflow based on your specific needs. 