job_body = cmlapi.CreateJobRequest()
      
# name and script
job_body.name = "my job name"
job_body.script = "pi.py"
      
# arguments
job_body.arguments = "arg1 arg2 \"all arg 3\""
      
# engine kernel
job_body.kernel = "python3" # or "r", or "scala"
      
# schedule
# manual by default
# for recurring/cron:
job_body.schedule = "* * * * 5" # or some valid cron string
      
# for dependent (don't set both parent_job_id and schedule)
job_body.parent_job_id = "abcd-1234-abcd-1234"
      
# resource profile (cpu and memory can be floating point for partial)
job_body.cpu = 1 # one cpu vcore
job_body.memory = 1 # one GB memory
job_body.nvidia_gpu = 1 # one nvidia gpu, cannot do partial gpus
      
# timeout
job_body.timeout = 300 # this is in seconds
      
# environment
job_body.environment = {"MY_ENV_KEY": "MY_ENV_VAL", "MY_SECOND_ENV_KEY": "MY_SECOND_ENV_VAL"}
      
# attachment
job_body.attachments = ["report/1.txt", "report/2.txt"] # will attach /home/cdsw/report/1.txt and /home/cdsw/report/2.txt to emails
      
# After setting the parameters above, create the job:
client = cmlapi.default_client("host", "api key")
client.create_job(job_body, project_id="id of project to create job in")