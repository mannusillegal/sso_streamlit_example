from influxdb_client import InfluxDBClient, Point, WritePrecision
import csv

def convert_csv_to_line_protocol(csv_file):
    lines = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            line = f"{row['TAGNAME']},EQUIPMENT={row['EQUIPMENT']} "
            line += f"TAGVALUE={row['TAGVALUE']} "
            line += f"{int(row['TIMESTAMP']) * 1000000000}"
            lines.append(line)
    return lines

def load_data_into_influxdb(lines, token, org, bucket):
    client = InfluxDBClient(url="http://localhost:8086", token=token)
    write_api = client.write_api()
    write_api.write(bucket=bucket, record=lines, org=org, write_precision=WritePrecision.NS)
    write_api.close()

def delete_data_from_influxdb(query, token):
    client = InfluxDBClient(url="http://localhost:8086", token=token)
    query_api = client.query_api()
    query_api.query(query)
    query_api.close()

def handle_error_and_status(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
            print("Data successfully loaded into InfluxDB.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
    return wrapper

@handle_error_and_status
def main(csv_file, token, org, bucket):
    lines = convert_csv_to_line_protocol(csv_file)
    load_data_into_influxdb(lines, token, org, bucket)
    # Optionally, you can delete the loaded data using the following line:
    # delete_data_from_influxdb("DELETE FROM <measurement>", token)

if __name__ == '__main__':
    csv_file = "data.csv"
    token = "your_influxdb_token"
    org = "your_organization"
    bucket = "your_bucket"
    main(csv_file, token, org, bucket)
            
