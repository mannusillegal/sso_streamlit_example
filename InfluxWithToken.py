from influxdb_client import InfluxDBClient, Point, WritePrecision

def connect_to_influxdb(url, token, org):
    try:
        # Configure the InfluxDB client
        client = InfluxDBClient(url=url, token=token, org=org)
        return client
    except Exception as e:
        print(f"Error occurred while connecting to InfluxDB: {str(e)}")

def write_to_influxdb(client, data, bucket, measurement):
    try:
        write_api = client.write_api()

        for key, values in data.items():
            for subkey, value in values.items():
                point = Point(measurement).tag("key", key).tag("subkey", subkey).field("value", value)
                write_api.write(bucket=bucket, record=point)

        write_api.close()
    except Exception as e:
        print(f"Error occurred while writing to InfluxDB: {str(e)}")

def read_from_influxdb(client, bucket, measurement):
    try:
        query_api = client.query_api()

        query = f'from(bucket: "{bucket}") |> range(start: 0) |> filter(fn: (r) => r._measurement == "{measurement}")'
        result = query_api.query(org=client.org, query=query)

        data_dict = {}

        for table in result:
            for record in table.records:
                key = record.get_tag("key")
                subkey = record.get_tag("subkey")
                value = record.get_field("value")
                
                if key not in data_dict:
                    data_dict[key] = {}
                
                data_dict[key][subkey] = value

        return data_dict
    except Exception as e:
        print(f"Error occurred while reading from InfluxDB: {str(e)}")

# Example usage

# Step 1: Establish connection to InfluxDB
url = "http://localhost:8086"
token = "your_influxdb_token"
org = "your_organization"
bucket = "my_bucket"
measurement = "my_measurement"

try:
    client = connect_to_influxdb(url, token, org)
    print("Connected to InfluxDB successfully.")
except Exception as e:
    print(f"Error occurred while connecting to InfluxDB: {str(e)}")
    exit(1)

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
try:
    write_to_influxdb(client, my_dict, bucket, measurement)
    print("Data has been written to InfluxDB successfully.")
except Exception as e:
    print(f"Error occurred while writing to InfluxDB: {str(e)}")
    exit(1)

# Step 4: Read the data from InfluxDB
try:
    retrieved_data = read_from_influxdb(client, bucket, measurement)
    print("Retrieved data from InfluxDB:")
    print(retrieved_data)
except Exception as e:
    print(f"Error occurred while reading from InfluxDB: {str(e)}")
    exit(1)

# Step 5: Close the connection
client.close()
print("InfluxDB connection has been closed.")
