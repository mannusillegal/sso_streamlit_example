import pandas as pd
import time

# define the file path and column names to read from
file_path = 'data.csv'
timestamp_col = 'timestamp'
tags_col = 'tags'

# read the CSV file
data = pd.read_csv(file_path)

# convert the timestamp column to datetime format
data[timestamp_col] = pd.to_datetime(data[timestamp_col])

# set the initial time
start_time = pd.Timestamp('2023-03-08 18:38:49')

# loop through the data
while True:
    # select the rows that come after start_time
    selected_data = data[data[timestamp_col] >= start_time][[timestamp_col, tags_col]]
    
    # check if there's any data to process
    if not selected_data.empty:
        # do something with the selected data
        # for example, print the data to the console
        print(selected_data)
        
        # update the start_time to be 15 seconds after the last timestamp
        last_timestamp = selected_data[timestamp_col].max()
        start_time = last_timestamp + pd.Timedelta(seconds=15)
        
    # wait for 15 seconds before reading the next set of data
    time.sleep(15)
