import subprocess
import os
import boto3

# AWS CloudWatch log group name
LOG_GROUP_NAME = 'my-log-group'

# Docker container names and log categories
CONTAINERS = {
    'my-app': 'app-logs',
    'my-database': 'db-logs'
}

# Temp log file directory
TEMP_LOG_DIR = '/app/tmp'

# AWS CloudWatch client
cloudwatch = boto3.client('logs')

def create_log_group_if_not_exists(log_group_name):
    # Check if the log group exists, create it if it does not exist
    response = cloudwatch.describe_log_groups(logGroupNamePrefix=log_group_name)
    if len(response['logGroups']) == 0:
        # Log group does not exist, create it
        cloudwatch.create_log_group(logGroupName=log_group_name)
        print(f'Log group "{log_group_name}" created successfully.')
    else:
        # Log group already exists
        print(f'Log group "{log_group_name}" already exists.')

def upload_logs_to_cloudwatch(log_group_name, container_name, log_category):
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
            logStreamName=container_name,
            logEvents=[
                {
                    'timestamp': int(round(time.time() * 1000)),
                    'message': log_data
                }
            ]
        )

        # Delete log file
        os.remove(log_file)

def pull_container_logs(container_name, log_category):
    # Set log file path
    log_file = f'{TEMP_LOG_DIR}/{container_name}.log'

    # Pull logs from Docker container
    subprocess.run(['docker', 'logs', container_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Write logs to file
    with open(log_file, 'w') as f:
        f.write(log_data)

def main():
    # Check if log group exists, create it if it does not exist
    create_log_group_if_not_exists(LOG_GROUP_NAME)

    # Pull logs from each container and upload to CloudWatch
    for container_name, log_category in CONTAINERS.items():
        pull_container_logs(container_name, log_category)
        upload_logs_to_cloudwatch(LOG_GROUP_NAME, container_name, log_category)

if __name__ == '__main__':
    main()
