import os
import subprocess
import boto3
import time

# AWS region and credentials
region_name = 'us-east-1'
aws_access_key_id = 'your_access_key_id'
aws_secret_access_key = 'your_secret_access_key'

# AWS CloudWatch client
cloudwatch = boto3.client('logs', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# Name of the CloudWatch log group
log_group_name = 'my-log-group'

def create_log_group_if_not_exists(log_group_name):
    try:
        response = cloudwatch.describe_log_groups(logGroupNamePrefix=log_group_name)
        if len(response['logGroups']) > 0:
            print(f'Log group "{log_group_name}" already exists')
            return
    except cloudwatch.exceptions.ResourceNotFoundException:
        pass

    print(f'Log group "{log_group_name}" does not exist, creating log group')
    cloudwatch.create_log_group(logGroupName=log_group_name)

def create_log_stream_if_not_exists(log_group_name, log_stream_name):
    try:
        response = cloudwatch.describe_log_streams(logGroupName=log_group_name, logStreamNamePrefix=log_stream_name)
        if len(response['logStreams']) > 0:
            print(f'Log stream "{log_stream_name}" already exists')
            return
    except cloudwatch.exceptions.ResourceNotFoundException:
        pass

    print(f'Log stream "{log_stream_name}" does not exist, creating log stream')
    cloudwatch.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)

def upload_logs_to_cloudwatch(log_group_name):
    # Get a list of Docker container IDs and names
    containers = subprocess.check_output('docker ps -aq --format "{{.ID}}:{{.Names}}"', shell=True).decode().strip().split('\n')

    # Iterate over the containers, extract and upload the logs to CloudWatch
    for container in containers:
        container_id, container_name = container.split(':')
        log_stream_name = container_name
        category = 'my-log-group/' + log_stream_name

        # Check if the log stream exists, create it if it does not exist
        create_log_stream_if_not_exists(log_group_name, log_stream_name)

        # Get the logs from the container and save them to the temp directory
        subprocess.call(f'docker logs {container_id} > /app/tmp/{container_name}.log', shell=True)

        # Upload the logs to CloudWatch in 1 MB chunks
        with open(f'/app/tmp/{container_name}.log', 'r') as log_file:
            lines = log_file.readlines()
            num_chunks = len(lines) // 10000 + 1
            for i in range(num_chunks):
                start = i * 10000
                end = (i + 1) * 10000
                log_events = [{'timestamp': int(os.path.getctime(log_file.name)) * 1000, 'message': line} for line in lines[start:end]]
                cloudwatch.put_log_events(logGroupName=log_group_name, logStreamName=log_stream_name, logEvents=log_events)

        # Delete the temp log file
        os.remove(f'/app/tmp/{container_name}.log')

# Create the log group if it does not exist
create_log_group_if_not_exists(log_group_name)

# Run the script every 10 minutes
while True:
    upload_logs_to_cloudwatch(log_group_name)
    time.sleep(600)
