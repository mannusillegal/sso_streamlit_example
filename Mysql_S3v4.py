import csv
import boto3
from sqlalchemy import create_engine, desc

# Set up database connection
DB_USERNAME = 'your_db_username'
DB_PASSWORD = 'your_db_password'
DB_HOST = 'your_db_host'
DB_PORT = 'your_db_port'
DB_NAME = 'your_db_name'

DATABASE_URL = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_engine(DATABASE_URL)

# Set up S3 client
S3_BUCKET = 'your_s3_bucket_name'
s3_prefix = '/MySQL/data/'
s3 = boto3.resource('s3')

# Set up file paths and names
LOCAL_FILE_NAME = 'data.csv'
LOCAL_FILE_PATH = '/app/tmp/sqldata'
S3_FILE_NAME = f"{s3_prefix}{{table_name}}/{LOCAL_FILE_NAME}"

def copy_to_s3(table_name):
    # Query the latest data from the database
    query = f"SELECT * FROM {table_name} ORDER BY your_timestamp_column DESC LIMIT 1;"
    result_proxy = engine.execute(query)
    latest_data = result_proxy.fetchone()

    # Get the column names from the database
    columns_query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='{table_name}';"
    columns_result_proxy = engine.execute(columns_query)
    columns = [row[0] for row in columns_result_proxy.fetchall()]

    # Append latest data to existing file or create new file in local
    local_path = f"{LOCAL_FILE_PATH}/{LOCAL_FILE_NAME}"
    with open(local_path, 'a+', newline='') as f:
        csvwriter = csv.writer(f)
        if f.tell() == 0:
            # If the file is empty, write the column names
            csvwriter.writerow(columns)
        csvwriter.writerow(latest_data)

    # Upload the local file to S3
    s3_path = S3_FILE_NAME.format(table_name=table_name)
    s3.meta.client.upload_file(local_path, S3_BUCKET, s3_path)

# Example usage:
copy_to_s3('your_table_name')
