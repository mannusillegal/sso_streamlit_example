from influxdb import InfluxDBClient

def write_to_influxdb(data, database, measurement):
    try:
        # Configure the InfluxDB client
        client = InfluxDBClient(host='localhost', port=8086)

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

        # Close the connection
        client.close()
    except Exception as e:
        print(f"Error occurred while writing to InfluxDB: {str(e)}")

def read_from_influxdb(database, measurement):
    try:
        # Configure the InfluxDB client
        client = InfluxDBClient(host='localhost', port=8086)

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

        # Close the connection
        client.close()

        # Return the dictionary containing the retrieved data
        return data_dict
    except Exception as e:
        print(f"Error occurred while reading from InfluxDB: {str(e)}")
        
        
  ### Example usage

# Step 1: Prepare the data to be written to InfluxDB
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

# Step 2: Write the data to InfluxDB
database = "my_database"
measurement = "my_measurement"
write_to_influxdb(my_dict, database, measurement)

# Step 3: Read the data from InfluxDB
retrieved_data = read_from_influxdb(database, measurement)

# Step 4: Print the retrieved data
print(retrieved_data)
      
