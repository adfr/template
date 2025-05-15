# CML Jobs Template

This template provides a framework for setting up and managing jobs in Cloudera Machine Learning (CML).

## Files Overview

- `config/jobs_config.yaml` - Contains all job configurations and their parameters
- `run_jobs.py` - Main script that reads job configurations and creates them in CML
- `create_environment.py` - First job that sets up the Python environment
- `process_data.py` - Example data processing job
- `.env` - Environment variables (not in version control)
- `.env.example` - Example environment variables template

## How It Works

1. Define all your jobs in `config/jobs_config.yaml` with their parameters, dependencies, and resources
2. Configure your environment variables in `.env` (copy from `.env.example`)
3. The first job is always `create_env` which sets up the Python environment
4. Run the `run_jobs.py` script to create all the jobs in CML

## Usage

Set environment variables in a `.env` file:

```
CML_API_HOST=https://ml-12345.cloud.example.com
CML_API_KEY=your_api_key_here
CML_PROJECT_ID=project_id_here
CML_RUNTIME_ID=your_ml_runtime_id  # Required for ML Runtime projects
```

Then run the script:

```bash
python run_jobs.py
```

Additional environment variables that can be set:
- `DEFAULT_CPU` - Default CPU cores for jobs (if not specified in config)
- `DEFAULT_MEMORY` - Default memory in GB for jobs (if not specified in config)
- `DEFAULT_TIMEOUT` - Default timeout in seconds for jobs (if not specified in config)

## Job Configuration

Each job in `config/jobs_config.yaml` has the following structure:

```yaml
jobs:
  job_key:
    name: Human-readable job name
    script: script_to_run.py
    kernel: python3  # or r, scala, etc.
    runtime_id: runtime_id_here  # Required for ML Runtime projects 
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

## ML Runtimes vs. Engine Runtimes

CML supports two types of runtimes:

1. **ML Runtimes** (newer) - Require a `runtime_id` parameter in job configurations
2. **Engine Runtimes** (legacy) - Do not require a `runtime_id` parameter

For ML Runtime projects, you must specify the `runtime_id` either in:
1. Each job configuration in `config/jobs_config.yaml`, or
2. The `.env` file as `CML_RUNTIME_ID` (used as a default for all jobs)

The runtime ID can be:
- A short name (e.g., `python3.11`)
- A full image URL (e.g., `docker.repository.cloudera.com/cloudera/cdsw/ml-runtime-pbj-jupyterlab-python3.11-standard:2025.01.3-b8`)

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