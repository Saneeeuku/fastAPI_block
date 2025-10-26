import logging

import redis.asyncio as redis
from redis import RedisError


class RedisManager:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.redis: redis.Redis | None = None

    async def connect(self):
        try:
            self.redis = await redis.Redis(host=self.host, port=self.port)
        except RedisError:
            logging.error(f"Не удалось подключиться Redis host={self.host}, port={self.port}")
        logging.info(f"Подключено к Redis host={self.host}, port={self.port}")

    async def set(self, key: str, val: str, expire: int = None):
        if expire:
            await self.redis.set(key, val, ex=expire)
        else:
            await self.redis.set(key, val)

    async def get(self, key: str):
        return await self.redis.get(key)

    async def delete(self, key: str):
        await self.redis.delete(key)

    async def close(self):
        if self.redis:
            try:
                await self.redis.close()
            except RedisError:
                logging.error(f"Не удалось подключиться Redis host={self.host}, port={self.port}")
            logging.info(f"Подключение Redis закрыто host={self.host}, port={self.port}")
