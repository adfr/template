# Cloudera AI Jobs Template

This template provides a comprehensive framework for setting up and managing jobs in Cloudera Machine Learning (CML), including ML workflows, data processing, and scheduled tasks.

## 🚀 Quick Start

1. Clone this repository into your CML project
2. Copy `.env.example` to `.env` and fill in your values
3. Run `python run_jobs.py` to create all jobs in CML

## 📁 Project Structure

```
cloudera-AI-template/
├── config/
│   └── jobs_config.yaml      # Job configurations
├── scripts/
│   ├── hello_world.py        # Basic job example
│   └── example_job.py        # Environment activation example
├── src/                      # Additional source code
├── results/                  # Job outputs (created automatically)
├── create_environment.py     # Environment setup script
├── run_jobs.py              # Main job creation script
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
└── README.md                # This file
```

## ⚙️ Configuration

### Environment Variables (.env)

```bash
# CML API Configuration
CML_API_HOST=https://ml-12345.cloud.example.com
CML_API_KEY=your_api_key_here
CML_PROJECT_ID=project_id_here

# ML Runtime ID (required for ML Runtime projects)
CML_RUNTIME_ID=python3.11

# Default resource settings (optional)
DEFAULT_CPU=1
DEFAULT_MEMORY=2
DEFAULT_TIMEOUT=3600
```

### Job Configuration (jobs_config.yaml)

Each job has the following structure:

```yaml
jobs:
  job_key:
    name: Human-readable job name
    script: path/to/script.py
    kernel: python3
    runtime_id: 91
    cpu: 4
    memory: 8
    timeout: 3600
    environment:
      ENV_VAR: value
    arguments: --param value
    parent_job_id: previous_job  # For dependent jobs
    schedule: "0 8 * * 1"       # For scheduled jobs (cron format)
```

## 📋 Included Jobs

1. **create_env** - Sets up the Python environment with required packages
2. **data_processing** - Example data processing job with argument parsing
3. **scheduled_report** - Weekly scheduled job example

## 🔧 Key Features

- **Automatic path detection** - Works both locally and when cloned in CML
- **Dependency management** - Jobs can depend on other jobs
- **Flexible scheduling** - Support for cron-style scheduling
- **Resource configuration** - CPU, memory, and GPU allocation
- **Environment variables** - Pass configuration to jobs
- **Comprehensive examples** - ML training, data processing, and more

## 📝 Adding New Jobs

1. Create your script in the `scripts/` directory:

```python
#!/usr/bin/env python3
"""Your job description"""

import argparse
import logging

def main():
    # Your job logic here
    pass

if __name__ == "__main__":
    main()
```

2. Add the job configuration to `config/jobs_config.yaml`:

```yaml
jobs:
  my_new_job:
    name: My New Job
    script: scripts/my_new_job.py
    kernel: python3
    runtime_id: 91
    cpu: 2
    memory: 4
    parent_job_id: data_processing
```

3. Run `python run_jobs.py` to create the job in CML

## 🏃 ML Runtimes vs. Engine Runtimes

CML supports two types of runtimes:

1. **ML Runtimes** (newer) - Require a `runtime_id` parameter
2. **Engine Runtimes** (legacy) - Don't require a `runtime_id`

For ML Runtime projects, specify the `runtime_id` either:
- In each job configuration, or
- As `CML_RUNTIME_ID` in the `.env` file (default for all jobs)

## 🔍 Debugging

1. Check job logs in the CML UI
2. Use `--log_level DEBUG` in job arguments for verbose logging
3. Verify environment variables are set correctly
4. Ensure all file paths are correct

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues or questions:
- Check the CML documentation
- Open an issue in this repository
- Contact your CML administrator