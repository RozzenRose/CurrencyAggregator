import httpx, json
from config import settings
from local_redis import Redis


async def get_rates(cur):
    redis = await Redis.get_redis()
    cache_key = f'rates:{cur}'
    cache = await redis.get(cache_key)
    if cache:
        return json.loads(cache)
    url = (f'{settings.url_rate_api}{cur}')
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        await redis.set(cache_key, json.dumps(response.json()['rates']), ex=60*60)
        return response.json()['rates']
