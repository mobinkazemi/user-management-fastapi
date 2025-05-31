import redis
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

redis_host = config.get("redis", "REDIS_HOST")
redis_port = config.get("redis", "REDIS_PORT")
redis_password = config.get("redis", "REDIS_PASSWORD")


redis_client = redis.Redis(
    host=redis_host, password=redis_password, port=redis_port, decode_responses=True
)
