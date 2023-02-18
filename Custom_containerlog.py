import boto3
import docker
import os
import shutil
import time

# Define the log group name
LOG_GROUP_NAME = '/aws/lambda/my-function'

# Define the temporary directory to store logs
TMP_DIR = '/app/tmp'

# Initialize the AWS CloudWatch Logs client
logs_client = boto3.client('logs')

# Initialize the Docker client
docker_client = docker.from_env()

# Function to check if a log group exists
def log_group_exists(log_group_name):
    try:
        response = logs_client.describe_log_groups(
            logGroupNamePrefix=log_group_name
        )
        if len(response['logGroups']) > 0:
            return True
        else:
            return False
    except:
        return False

# Function to create a log group
def create_log_group(log_group_name):
    response = logs_client.create_log_group(
        logGroupName=log_group_name
    )
    print('Created log group:', log_group_name)

# Function to fetch the logs for a container
def fetch_container_logs(container, log_file):
    logs = container.logs(tail=1000).decode('utf-8')
    with open(log_file, 'w') as f:
        f.write(logs)

# Function to upload logs to CloudWatch Logs
def upload_logs(log_group_name, log_stream_name, log_file):
    with open(log_file, 'r') as f:
        logs = f.read()
    logs_client.put_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        logEvents=[
            {
                'timestamp': int(round(time.time() * 1000)),
                'message': logs
            }
        ]
    )

# Function to delete logs from the host
def delete_logs(log_file):
    os.remove(log_file)

# Check if the log group exists, create if not
if not log_group_exists(LOG_GROUP_NAME):
    create_log_group(LOG_GROUP_NAME)

# Get the list of containers and their names
containers = docker_client.containers.list()

# Fetch logs for each container and upload to CloudWatch Logs
for container in containers:
    container_name = container.name
    log_file = os.path.join(TMP_DIR, container_name + '.log')
    fetch_container_logs(container, log_file)
    upload_logs(LOG_GROUP_NAME, container_name, log_file)
    delete_logs(log_file)

# Schedule the entire process to run every 30 minutes
while True:
    time.sleep(1800)
    containers = docker_client.containers.list()
    for container in containers:
        container_name = container.name
        log_file = os.path.join(TMP_DIR, container_name + '.log')
        fetch_container_logs(container, log_file)
        upload_logs(LOG_GROUP_NAME, container_name, log_file)
        delete_logs(log_file)
