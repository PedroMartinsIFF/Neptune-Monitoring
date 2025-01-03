
```markdown
# Zabbix API Metrics Script

This script collects metrics from AWS CloudWatch for Neptune databases and sends them to a Zabbix server.

## Prerequisites

- Python 3.x
- `pyzabbix` library
- `boto3` library
- AWS credentials with access to CloudWatch
- Zabbix server details

## Environment Variables

The script requires the following environment variables to be set:

- `ZABBIX_PASSIVE`: Hostname or IP address of the Zabbix server.
- `ZABBIX_PASSIVE_PORT`: Port number of the Zabbix server.
- `ACCESS_KEY`: AWS access key.
- `SECRET_KEY`: AWS secret key.
- `REGION`: AWS region.
- `METRIC`: Metric type (0 or 1).
- `DATABASE`: Comma-separated list of Neptune databases.
- `ZABBIX_HOST_DST`: Comma-separated list of Zabbix hosts.
- `ITEM_KEY`: Zabbix item key.

## Usage

1. Clone the repository or download the script.
2. Install the required Python libraries:
   ```sh
   pip install pyzabbix boto3
   ```
3. Set the required environment variables.
4. Run the script:
   ```sh
   python3 your_script_name.py
   ```

## Functions

### `convert(string)`

Converts a comma-separated string into a list.

### `cria_string(var)`

Creates a JSON string from the metric data.

### `Average(lst)`

Calculates the average of a list of numbers.

### `neptune(database, i)`

Fetches metrics from AWS CloudWatch and sends them to the Zabbix server.

### `run_lambda(event, lambda_context)`

Main function to run the script.

## Error Handling

The script includes basic error handling to catch and print exceptions.

## License

This project is licensed under the MIT License.
```
