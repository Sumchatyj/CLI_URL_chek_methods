import asyncio
import json
import re
from http import HTTPStatus

import aiohttp
import asyncclick

EXPRESSION = (
    r"^https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]"
    r"{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)$"
)


def validate_url(number: int, url: str) -> bool:
    if re.match(EXPRESSION, url) is None:
        print(f"the string {number} is not a valid URL")
        return False
    else:
        return True


async def check_methods(
    session,
    url: str,
) -> dict:
    result = {}
    try:
        async with session.get(url) as resp:
            if resp.status != HTTPStatus.METHOD_NOT_ALLOWED:
                result["GET"] = resp.status
    except Exception:
        return "try another url"
    async with session.head(url) as resp:
        if resp.status != HTTPStatus.METHOD_NOT_ALLOWED:
            result["HEAD"] = resp.status
    async with session.options(url) as resp:
        if resp.status != HTTPStatus.METHOD_NOT_ALLOWED:
            result["OPTIONS"] = resp.status
    async with session.post(url) as resp:
        if resp.status != HTTPStatus.METHOD_NOT_ALLOWED:
            result["POST"] = resp.status
    async with session.put(url) as resp:
        if resp.status != HTTPStatus.METHOD_NOT_ALLOWED:
            result["PUT"] = resp.status
    async with session.patch(url) as resp:
        if resp.status != HTTPStatus.METHOD_NOT_ALLOWED:
            result["PATCH"] = resp.status
    async with session.delete(url) as resp:
        if resp.status != HTTPStatus.METHOD_NOT_ALLOWED:
            result["DELETE"] = resp.status
    return result


async def check_all_urls(session, urls: dict):
    tasks = []
    for url in urls:
        task = asyncio.create_task(check_methods(session, url))
        tasks.append(task)
    result = await asyncio.gather(*tasks)
    for number, url in enumerate(urls):
        urls[url] = result[number]
    return urls


@asyncclick.command()
@asyncclick.argument("strings", nargs=-1)
async def main(strings) -> None:
    result = {}
    for number, string in enumerate(strings):
        if validate_url(number, string):
            result[string] = None
    async with aiohttp.ClientSession() as session:
        await check_all_urls(session, result)
    if result != {}:
        print(json.dumps(result, indent=4))


if __name__ == "__main__":
    asyncio.run(main())
