import asyncclick
import re
import aiohttp
import asyncio
import json


EXPRESSION = (
    r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\."
    r"[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|"
    r"https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\."
    r"[a-zA-Z0-9]+\.[^\s]{2,})"
)
STRINGS = ['http://www.foufos.gr', 'https://google.com', 'google.com']


def validate_url(number: int, url: str) -> bool:
    if re.match(EXPRESSION, url) is None:
        print(f"the string {number} is not a valid URL")
        return False
    else:
        return True


async def check_methods(session, url: str,):
    result = {}
    async with session.get(url) as resp:
        if resp.status != 405:
            result['GET'] = resp.status
    async with session.head(url) as resp:
        if resp.status != 405:
            result['HEAD'] = resp.status
    async with session.options(url) as resp:
        if resp.status != 405:
            result['OPTIONS'] = resp.status
    async with session.post(url) as resp:
        if resp.status != 405:
            result['POST'] = resp.status
    async with session.put(url) as resp:
        if resp.status != 405:
            result['PUT'] = resp.status
    async with session.patch(url) as resp:
        if resp.status != 405:
            result['PATCH'] = resp.status
    async with session.delete(url) as resp:
        if resp.status != 405:
            result['DELETE'] = resp.status
    return result


async def check_all_urls(session, urls: dict):
    tasks = []
    for url in urls:
        task = asyncio.create_task(check_methods(session, url))
        tasks.append(task)
    result = await asyncio.gather(*tasks)
    counter = 0
    for url in urls:
        urls[url] = result[counter]
        counter += 1
    return urls


@asyncclick.command()
@asyncclick.argument('strings', nargs=-1)
async def main(strings) -> None:
    result = {}
    for number, string in enumerate(strings):
        if validate_url(number, string) is True:
            result[string] = None
    async with aiohttp.ClientSession() as session:
        await check_all_urls(session, result)
    if result != {}:
        print(json.dumps(result, indent=4))


if __name__ == '__main__':
    asyncio.run(main())
