from fastapi import FastAPI
from app.users.routers import router as user_router
from app.main.routers import router as main_router
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis


app = FastAPI()


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


app.include_router(user_router)
app.include_router(main_router)
