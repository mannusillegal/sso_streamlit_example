import subprocess
import boto3
import tempfile
import os
import time

# Initialize the CloudWatch client with region parameter
cloudwatch = boto3.client('logs', region_name='us-west-2')

# Define the name of the CloudWatch log group
log_group_name = 'your-log-group-name'

# Define the time interval between log pulls in seconds
n_minutes = 1
n_seconds = n_minutes * 60

# Define the directory to store temporary logs
temp_dir = '/app/temp'

# Check if the log group already exists
try:
    cloudwatch.describe_log_groups(logGroupNamePrefix=log_group_name)
    print(f"The log group '{log_group_name}' already exists.")
except cloudwatch.exceptions.ResourceNotFoundException:
    print(f"The log group '{log_group_name}' does not exist. Creating log group...")
    cloudwatch.create_log_group(logGroupName=log_group_name)

while True:
    # Get a list of all the running containers
    output = subprocess.check_output(['docker', 'ps', '-q']).decode('utf-8').strip().split('\n')
    containers = [x.strip() for x in output if x.strip()]

    # Loop through each container and pull the logs
    for container in containers:
        # Get the container name
        name = subprocess.check_output(['docker', 'inspect', '-f', '{{.Name}}', container]).decode('utf-8').strip()
        print(name)

        # Pull the logs
        logs = subprocess.check_output(['docker', 'logs', container]).decode('utf-8')
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
                logStreamName=name,
                logEvents=log_events
            )

        # Delete the temporary file
        os.unlink(temp_file.name)

    # Wait for the specified time interval before pulling logs again
    time.sleep(n_seconds)
