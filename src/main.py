import uvicorn
from fastapi import FastAPI

from src.api.hotels import router as router_hotels
from src.config import settings

app = FastAPI()
app.include_router(router_hotels)


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
