#!/usr/bin/env python3

# spin_async.py

# credits: Example by Luciano Ramalho inspired by
# Michele Simionato's multiprocessing example in the python-list:
# https://mail.python.org/pipermail/python-list/2009-February/538048.html

# BEGIN PRIME_ASYNCIO
import asyncio
import itertools
import time
import aiohttp

import images

async def spin(msg):  # <1>
    for char in itertools.cycle('⠇⠋⠙⠸⠴⠦'):
        status = f'\r{char} {msg}'
        print(status, flush=True, end='')
        try:
            await asyncio.sleep(.1)  # <2>
        except asyncio.CancelledError:  # <3>
            break
    blanks = ' ' * len(status)
    print(f'\r{blanks}\r', end='')



async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            assert response.status == 200
            return await response.read()



async def fetch_by_size(target_size):
    size, path = images.pick_by_size(target_size)
    url = images.BASE_URL + path

    octets = await fetch(url)

    name = images.save(url, octets)
    return (size, name)


async def slow_function():  # <4>
    return await fetch_by_size(7_000_000)


async def supervisor():  # <6>
    spinner = asyncio.create_task(spin('thinking!'))  # <7>
    print('spinner object:', spinner)  # <8>
    result = await slow_function()  # <9>
    spinner.cancel()  # <10>
    return result


def main():
    t0 = time.perf_counter()
    size, name = asyncio.run(supervisor())  # <11>
    dt = time.perf_counter() - t0
    print(f'{size:_d} bytes downloaded')
    print('Name:', name)
    print(f'Elapsed time: {dt:0.3}s')


if __name__ == '__main__':
    main()
# END SPINNER_ASYNCIO
