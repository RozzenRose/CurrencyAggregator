import httpx


async def get_rates(cur, count_cur):
    if cur == count_cur:
        return 1
    if not count_cur:
        return 0
    url = f'https://open.er-api.com/v6/latest/{cur}'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()['rates'][f'{count_cur}']
