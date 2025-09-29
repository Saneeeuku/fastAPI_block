import json
from typing import Callable
from functools import wraps
import inspect

from redis import RedisError
from pydantic import BaseModel

from src.init import redis_manager


def my_cache(
    expire: int = None,
    include_query: bool = True
):
    def my_cache_outer(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            sig = inspect.signature(func)
            param_names = list(sig.parameters.keys())[:1]
            cache_key_parts = [func.__name__, f"{args}"]
            if include_query:
                request = None
                for arg in args:
                    if hasattr(arg, 'query_params'):
                        request = arg
                        break
                if not request and 'request' in kwargs:
                    request = kwargs['request']

                if request and hasattr(request, 'query_params') and request.query_params:
                    query_str = "&".join([f"{k}={v}" for k, v in sorted(request.query_params.items())])
                    cache_key_parts.append(f"query_{hash(query_str)}")
            for k, v in kwargs.items():
                if k not in param_names:
                    cache_key_parts.append(f"{k}={v}")
            cache_key = ":".join(cache_key_parts)
            try:
                data_from_rds = await redis_manager.get(cache_key)
                if data_from_rds:
                    return json.loads(data_from_rds)
            except RedisError:
                print("No data in cache... passing")
                pass
            res = await func(*args, **kwargs)
            if isinstance(res, dict):
                for k, v in res.items():
                    if isinstance(v, BaseModel):
                        res[k] = v.model_dump()
            else:
                try:
                    res = res.model_dump()
                except Exception:
                    res = [f.model_dump() for f in res]
            try:
                if expire:
                    await redis_manager.set(cache_key, json.dumps(res), expire=expire)
                else:
                    await redis_manager.set(cache_key, json.dumps(res))
                print(F"Added to Redis:\n{cache_key}")
            except RedisError:
                print("Error in adding cache... passing")
                pass
            return res
        return wrapper
    return my_cache_outer
