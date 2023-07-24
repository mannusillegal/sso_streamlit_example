import redis
import json
import configparser


class RedisCacheReader:
    def __init__(self, host, port, password=None, db=0):
        """
        Redis Cache Reader.

        Args:
            host (str): The Redis server hostname.
            port (int): The Redis server port.
            password (str, optional): The Redis server password, if any.
            db (int, optional): The Redis database number.
        """
        self.redis_client = redis.Redis(host=host, port=port, password=password, db=db)

    def read_json_data(self, key):
        """
        Read JSON data from Redis cache.

        Args:
            key (str): The key to retrieve the JSON data from Redis.

        Returns:
            dict: The JSON data associated with the provided key, or None if the key does not exist.
        """
        try:
            data = self.redis_client.get(key)
            if data is not None:
                return json.loads(data.decode())
            else:
                return None
        except (redis.exceptions.RedisError, json.JSONDecodeError) as e:
            print(f"An error occurred while reading JSON data from Redis cache: {e}")
            return None


def read_redis_config_from_secret_manager(file_path):
    """
    Read Redis configuration from the secret manager.

    Args:
        file_path (str): Path to the configuration file.

    Returns:
        tuple: Redis host, port, and password as a tuple.
    """
    config = configparser.ConfigParser()
    config.read(file_path)

    redis_host = config.get('redis', 'host')
    redis_port = config.getint('redis', 'port')
    redis_password = config.get('redis', 'password', fallback=None)

    return redis_host, redis_port, redis_password


def main():
    try:
        # Read Redis configuration from the secret manager
        redis_host, redis_port, redis_password = read_redis_config_from_secret_manager('config.ini')

        cache_reader = RedisCacheReader(host=redis_host, port=redis_port, password=redis_password)

        # Replace 'my_key' with the desired key to retrieve the JSON document from the cache
        json_data = cache_reader.read_json_data('my_key')

        if json_data:
            # Process the JSON data as needed
            print(json_data)
        else:
            print("JSON data not found in the cache.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
  
