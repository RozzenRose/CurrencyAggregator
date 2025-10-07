import httpx


async def get_rates(cur):
    url = f'https://open.er-api.com/v6/latest/{cur}'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()['rates']
