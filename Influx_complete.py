from influxdb import InfluxDBClient

def connect_to_influxdb(host, port, username, password):
    try:
        # Configure the InfluxDB client
        client = InfluxDBClient(host=host, port=port, username=username, password=password)
        return client
    except Exception as e:
        print(f"Error occurred while connecting to InfluxDB: {str(e)}")

def write_to_influxdb(client, data, database, measurement):
    try:
        # Create the database if it doesn't exist
        client.create_database(database)
        client.switch_database(database)

        # Prepare the data for writing to InfluxDB
        influx_data = []

        for key, values in data.items():
            for subkey, value in values.items():
                point = {
                    "measurement": measurement,
                    "tags": {
                        "key": key,
                        "subkey": subkey
                    },
                    "fields": {
                        "value": value
                    }
                }
                influx_data.append(point)

        # Write the data to InfluxDB
        client.write_points(influx_data)
    except Exception as e:
        print(f"Error occurred while writing to InfluxDB: {str(e)}")

def read_from_influxdb(client, database, measurement):
    try:
        # Switch to the specified database
        client.switch_database(database)

        # Query the data from InfluxDB
        query = f'SELECT * FROM "{measurement}"'
        result = client.query(query)

        # Create an empty dictionary to store the retrieved data
        data_dict = {}

        # Iterate over the query result and populate the dictionary
        for point in result.get_points():
            key = point['tags']['key']
            subkey = point['tags']['subkey']
            value = point['fields']['value']

            if key not in data_dict:
                data_dict[key] = {}

            data_dict[key][subkey] = value

        # Return the dictionary containing the retrieved data
        return data_dict
    except Exception as e:
        print(f"Error occurred while reading from InfluxDB: {str(e)}")

# Step 1: Establish connection to InfluxDB
host = "localhost"
port = 8086
username = "your_username"
password = "your_password"
database = "my_database"
measurement = "my_measurement"

client = connect_to_influxdb(host, port, username, password)

# Step 2: Prepare the data to be written to InfluxDB
my_dict = {
    "key1": {
        "subkey1": 10,
        "subkey2": 20
    },
    "key2": {
        "subkey3": 30,
        "subkey4": 40
    }
}

# Step 3: Write the data to InfluxDB
write_to_influxdb(client, my_dict, database, measurement)
print("Data has been written to InfluxDB successfully.")

# Step 4: Read the data from InfluxDB
retrieved_data = read_from_influxdb(client, database, measurement)

# Step 5: Print the retrieved data
print("Retrieved data from InfluxDB:")
print(retrieved_data)

# Step 6: Close the connection
client.close()
print("InfluxDB connection has been closed.")
