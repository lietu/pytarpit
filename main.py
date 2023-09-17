import asyncio
import random
from datetime import datetime
from math import floor
from time import monotonic

from settings import conf

CONNECTIONS = 0
WASTED_TIME = 0


async def ssh_handler(_reader, writer):
    global CONNECTIONS, WASTED_TIME
    CONNECTIONS += 1
    start = monotonic()

    try:
        while True:
            await asyncio.sleep(10)
            writer.write(b"%x\r\n" % random.randint(0, 2**32))  # nosec B311
            await writer.drain()

            current = monotonic()
            WASTED_TIME += current - start
            start = current
    except ConnectionResetError:
        pass
    finally:
        elapsed = monotonic() - start
        CONNECTIONS -= 1
        WASTED_TIME += elapsed


async def http_handler(_reader, writer):
    global CONNECTIONS, WASTED_TIME
    CONNECTIONS += 1
    start = monotonic()

    writer.write(b"HTTP/1.1 200 OK\r\n")
    try:
        while True:
            await asyncio.sleep(5)
            header = random.randint(0, 2**32)  # nosec B311
            value = random.randint(0, 2**32)  # nosec B311
            writer.write(b"X-%x: %x\r\n" % (header, value))
            await writer.drain()

            current = monotonic()
            WASTED_TIME += current - start
            start = current
    except ConnectionResetError:
        pass
    finally:
        elapsed = monotonic() - start
        CONNECTIONS -= 1
        WASTED_TIME += elapsed


async def ssh_server():
    host = "0.0.0.0"  # nosec B104
    server = await asyncio.start_server(ssh_handler, host, conf.SSH_PORT)
    async with server:
        print(f"Listening for SSH connections on port {conf.SSH_PORT}")
        await server.serve_forever()


async def http_server():
    host = "0.0.0.0"  # nosec B104
    server = await asyncio.start_server(http_handler, host, conf.HTTP_PORT)
    async with server:
        print(f"Listening for HTTP connections on port {conf.HTTP_PORT}")
        await server.serve_forever()


def format_elapsed(total_seconds: float) -> str:
    seconds = total_seconds
    days, remainder = divmod(seconds, 86400)  # Get days
    hours, remainder = divmod(seconds, 3600)  # Get hours
    minutes, seconds = divmod(remainder, 60)  # Get minutes & seconds

    days = floor(days)
    hours = floor(hours)
    minutes = floor(minutes)
    seconds = floor(seconds)

    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")

    return " ".join(parts)


async def status():
    while True:
        timestamp = datetime.now().isoformat("T")
        elapsed = format_elapsed(WASTED_TIME)
        print(
            f"{timestamp} {CONNECTIONS} connection(s) stuck in tarpit. Wasted {elapsed}"
        )

        await asyncio.sleep(conf.STATUS_INTERVAL)


async def main():
    waits = [ssh_server(), http_server(), status()]

    await asyncio.gather(*waits)


asyncio.run(main())
