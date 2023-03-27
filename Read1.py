import csv
import datetime
import time

# set the starting timestamp
timestamp = datetime.datetime(2023, 3, 8, 18, 38, 49)

# open the CSV file
with open('your_file_name.csv') as csvfile:
    reader = csv.DictReader(csvfile)

    # loop through each row in the CSV file
    for row in reader:

        # extract the data from the selected columns
        timestamp_data = row['timestamp']
        name_data = row['name']

        # convert the timestamp from the CSV to a datetime object
        csv_timestamp = datetime.datetime.strptime(timestamp_data, '%Y-%m-%d %H:%M:%S')

        # check if the timestamp in the CSV is after the current timestamp
        while csv_timestamp > timestamp:

            # wait for 15 seconds
            time.sleep(15)

            # update the timestamp
            timestamp = timestamp + datetime.timedelta(seconds=15)

        # store the data in separate variables
        timestamp = datetime.datetime.strptime(timestamp_data, '%Y-%m-%d %H:%M:%S')
        name = name_data

        # do something with the variables (e.g. pass them to another module)
