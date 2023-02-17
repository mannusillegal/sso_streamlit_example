import docker
import boto3
import tempfile
import os
import time

# Initialize the Docker client
client = docker.from_env()

# Initialize the CloudWatch client
cloudwatch = boto3.client('logs')

# Define the name of the CloudWatch log group
log_group_name = 'docker-logs'

# Define the time interval between log pulls in seconds
n_minutes = 1
n_seconds = n_minutes * 60

# Define the directory to store temporary logs
temp_dir = '/app/temp'

while True:
    # Get a list of all the running containers
    containers = client.containers.list()

    # Loop through each container and pull the logs
    for container in containers:
        print(container.name)
        logs = container.logs().decode('utf-8')
        print(logs)

        # Write the logs to a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, dir=temp_dir) as temp_file:
            temp_file.write(logs)

        # Send the logs to CloudWatch
        with open(temp_file.name, 'r') as file:
            log_events = [{
                'timestamp': int(time.time() * 1000),
                'message': line
            } for line in file.readlines()]

            cloudwatch.put_log_events(
                logGroupName=log_group_name,
                logStreamName=container.name,
                logEvents=log_events
            )

        # Delete the temporary file
        os.unlink(temp_file.name)

    # Wait for the specified time interval before pulling logs again
    time.sleep(n_seconds)
