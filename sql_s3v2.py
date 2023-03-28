#In thisscript, we first read the existing data from the S3 file and store it in the existing_data variable. 
#We then create a StringIO buffer from the existing data and use the csv.reader to skip the header row. 
#We then use the csv.writer to write the existing data from the buffer to the csv_buffer variable, 
#followed by the latest data. Finally, we use the s3.Object


import io
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

    # Write latest data to StringIO buffer
    csv_buffer = io.StringIO()
    csvwriter = csv.writer(csv_buffer)
    if s3.Object(S3_BUCKET, S3_FILE_NAME.format(table_name=table_name)).content_length == 0:
        # If the file is empty, write the column names
        csvwriter.writerow(columns)
    csvwriter.writerow(latest_data)

    # Append latest data to existing file in S3 bucket
    s3_path = S3_FILE_NAME.format(table_name=table_name)
    if s3.Object(S3_BUCKET, s3_path).content_length == 0:
        # If the file is empty, upload the buffer as a new file
        s3.Object(S3_BUCKET, s3_path).put(Body=csv_buffer.getvalue())
    else:
        # Otherwise, read the existing file and append the buffer to the contents
        existing_data = s3.Object(S3_BUCKET, s3_path).get()['Body'].read().decode('utf-8')
        existing_data_buffer = io.StringIO(existing_data)
        existing_csvreader = csv.reader(existing_data_buffer)
        next(existing_csvreader) # skip the header row
        csvwriter = csv.writer(csv_buffer)
        for row in existing_csvreader:
            csvwriter.writerow(row)
        s3.Object(S3_BUCKET, s3_path).put(Body=csv_buffer.getvalue())

# Example usage:
copy_to_s3('your_table_name')
