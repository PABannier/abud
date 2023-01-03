"""Typical use case for the pub/sub messaging system"""
import asyncio
from ctx import stream_data


async def main(host, port, channel):
    async with stream_data(host, port) as publisher:
        print("Initiating the program...")
        assert 1 + 1 == 2
        print("Doing a bunch of stuff...")
        for i in range(10):
            msg = str(i)
            await publisher.publish(msg, channel)
            await asyncio.sleep(1)
        print("Done")


if __name__ == "__main__":
    try:
        asyncio.run(main("127.0.0.1", 8000, "/general"))
    except KeyboardInterrupt:
        print("Bye!")
