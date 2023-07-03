import csv
import pandas as pd
from influxdb_client import InfluxDBClient

INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "your_influxdb_token"
INFLUXDB_ORG = "your_influxdb_org"
INFLUXDB_BUCKET = "your_influxdb_bucket"

def convert_csv_to_line_protocol(file_path):
    data = pd.read_csv(file_path)

    lines = []
    for _, row in data.iterrows():
        measurement = "your_measurement_name"
        equipment = row["EQUIPMENT"]
        timestamp = row["TIMESTAMP"]
        tagname = row["TAGNAME"]
        tagvalue = row["TAGVALUE"]
        tagchangedtimestamp = row["TAGCHANGEDTIMESTAMP"]
        historical_data_flag = row["HISTORICAL DATA FLAG"]

        line = f'{measurement},equipment={equipment},tagname={tagname} tagvalue={tagvalue},' \
               f'tagchangedtimestamp={tagchangedtimestamp},' \
               f'historical_data_flag={historical_data_flag} {timestamp}'

        lines.append(line)

    return "\n".join(lines)

def load_data_to_influxdb(line_protocol_data):
    client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
    write_api = client.write_api()

    write_api.write(bucket=INFLUXDB_BUCKET, record=line_protocol_data)

def read_data_from_influxdb():
    client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
    query_api = client.query_api()

    query = f'from(bucket:"{INFLUXDB_BUCKET}") |> range(start: 0)'

    result = query_api.query(query=query)
    return result

def delete_data_from_influxdb():
    client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
    delete_api = client.delete_api()

    predicate = f'_measurement=="your_measurement_name"'

    delete_api.delete(predicate=predicate, bucket=INFLUXDB_BUCKET)

# Example usage:
csv_file_path = "path/to/your/file.csv"
line_protocol_data = convert_csv_to_line_protocol(csv_file_path)
load_data_to_influxdb(line_protocol_data)

# Read data from InfluxDB
result = read_data_from_influxdb()
for table in result:
    for record in table.records:
        print(record.values)

# Delete data from InfluxDB
delete_data_from_influxdb()
