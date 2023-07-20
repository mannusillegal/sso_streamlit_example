import redis


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

    def read_data(self, key):
        """
        Read data from Redis cache.

        Args:
            key (str): The key to retrieve the data from Redis.

        Returns:
            The value associated with the provided key, or None if the key does not exist.
        """
        try:
            data = self.redis_client.get(key)
            return data.decode() if data is not None else None
        except redis.exceptions.RedisError as e:
            print(f"An error occurred while reading data from Redis cache: {e}")
            return None


# Usage example
cache_reader = RedisCacheReader(host='localhost', port=6379)
value = cache_reader.read_data('my_key')
print(value)
