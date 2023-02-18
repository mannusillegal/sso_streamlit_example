import boto3
import os
import subprocess
import time

# Constants
LOG_GROUP_NAME = 'my-log-group'
LOG_CATEGORY = 'my-log-category'
TEMP_LOG_DIR = '/app/tmp'

# AWS CloudWatch client
cloudwatch = boto3.client('logs')

def create_log_group(log_group_name):
    # Check if log group exists
    response = cloudwatch.describe_log_groups(
        logGroupNamePrefix=log_group_name
    )

    if len(response['logGroups']) == 0:
        # Log group does not exist, create it
        cloudwatch.create_log_group(
            logGroupName=log_group_name
        )
        print(f'Log group {log_group_name} created.')
    else:
        # Log group already exists
        print(f'Log group {log_group_name} exists.')

def upload_logs_to_cloudwatch(log_group_name, container_name, log_category):
    # Get log stream name
    log_stream_name = container_name

    # Check if log stream exists, create it if it does not exist
    response = cloudwatch.describe_log_streams(
        logGroupName=log_group_name,
        logStreamNamePrefix=log_stream_name
    )
    if len(response['logStreams']) == 0:
        # Log stream does not exist, create it
        cloudwatch.create_log_stream(
            logGroupName=log_group_name,
            logStreamName=log_stream_name
        )

    # Get log file path
    log_file = f'{TEMP_LOG_DIR}/{container_name}.log'

    # Check if log file exists, upload logs if it exists
    if os.path.exists(log_file):
        # Read logs from log file
        with open(log_file, 'r') as f:
            log_data = f.read()

        # Upload logs to CloudWatch
        cloudwatch.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=[
                {
                    'timestamp': int(round(time.time() * 1000)),
                    'message': log_data
                }
            ]
        )

        # Delete log file
        os.remove(log_file)

def get_container_names():
    # Get container names
    cmd = "docker ps --format '{{.Names}}'"
    output = subprocess.check_output(cmd, shell=True)
    container_names = output.decode().strip().split('\n')
    return container_names

def pull_docker_logs(container_names):
    # Pull logs from each container
    for container_name in container_names:
        cmd = f'docker logs {container_name} > {TEMP_LOG_DIR}/{container_name}.log'
        os.system(cmd)

def main():
    # Create log group if it does not exist
    create_log_group(LOG_GROUP_NAME)

    # Get container names
    container_names = get_container_names()

    # Pull logs from containers and upload to AWS CloudWatch
    for container_name in container_names:
        pull_docker_logs([container_name])
        upload_logs_to_cloudwatch(LOG_GROUP_NAME, container_name, LOG_CATEGORY)

if __name__ == '__main__':
    main()
