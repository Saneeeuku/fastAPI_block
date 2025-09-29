from src.connectors.redis_manager import RedisManager
from src.config import settings as s


redis_manager = RedisManager(host=s.REDIS_HOST, port=s.REDIS_PORT)
