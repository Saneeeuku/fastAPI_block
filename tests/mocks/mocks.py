from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

mock_router = mock.AsyncMock()
mock_router.subscriber.return_value = lambda f: f
mock_router.publisher.return_value = lambda f: f
mock_router.include_router.return_value = None
mock_router.start = mock.AsyncMock()
mock_router.close = mock.AsyncMock()

possible_paths = ["src.init.router", "app.init.router"]

for path in possible_paths:
    try:
        mock.patch(path, mock_router).start()
        break
    except Exception:
        continue
