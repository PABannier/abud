import asyncio
from abud import Subscriber


async def main(host: str, port: int, channel: str):
    subscriber = Subscriber(host, port)
    await subscriber.connect(channel)
    await subscriber.listen()


if __name__ == "__main__":
    try:
        asyncio.run(main("127.0.0.1", 8000, "/general"))
    except KeyboardInterrupt:
        print("Bye!")
