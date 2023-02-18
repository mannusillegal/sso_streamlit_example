#This code defines two functions, create_log_group_if_not_exists()
#and upload_logs_to_cloudwatch(). The create_log_group_if_not_exists() 
#function checks if the log group exists,
#and creates it if it does not. The upload_logs_to_cloudwatch()
#function uploads the logs to CloudWatch for each Docker container.
#The main code block checks if the log group
#exists, creates it if it does not, and then 
#enters a loop that uploads the logs to CloudWatch every 30 minutes using the time.sleep() function.


import os
import subprocess
import boto3
import time

def create_log_group_if_not_exists(log_group_name):
    # AWS CloudWatch client
    cloudwatch = boto3.client('logs')

    # Check if the log group exists, create it if it does not exist
    try:
        response = cloudwatch.describe_log_groups(logGroupNamePrefix=log_group_name)
    except Exception as e:
        cloudwatch.create_log_group(logGroupName=log_group_name)

def upload_logs_to_cloudwatch(log_group_name):
    # AWS CloudWatch client
    cloudwatch = boto3.client('logs')

    # Get a list of Docker container IDs and names
    containers = subprocess.check_output('docker ps -aq --format "{{.ID}}:{{.Names}}"', shell=True).decode().strip().split('\n')

    # Iterate over the containers, extract and upload the logs to CloudWatch
    for container in containers:
        container_id, container_name = container.split(':')
        category = 'my-log-group/' + container_name

        # Get the logs from the container and save them to the temp directory
        subprocess.call(f'docker logs {container_id} > /app/tmp/{container_name}.log', shell=True)

        # Upload the logs to CloudWatch
        with open(f'/app/tmp/{container_name}.log', 'r') as log_file:
            log_events = [{'timestamp': int(os.path.getctime(log_file.name)) * 1000, 'message': line} for line in log_file.readlines()]
            cloudwatch.put_log_events(logGroupName=log_group_name, logStreamName=category, logEvents=log_events)

        # Delete the temp log file
        os.remove(f'/app/tmp/{container_name}.log')

# CloudWatch log group name
log_group_name = '/aws/ecs/my-log-group'

# Check if the log group exists, create it if it does not exist
create_log_group_if_not_exists(log_group_name)

# Upload the logs to CloudWatch
while True:
    upload_logs_to_cloudwatch(log_group_name)
    time.sleep(1800) # wait 30 minutes
