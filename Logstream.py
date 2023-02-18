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
