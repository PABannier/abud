"""Typical use case for the pub/sub messaging system"""
import asyncio
from ctx import publish_to_stream
from utils import write_data

host = "127.0.0.1"
port = 8000
channel = "/general"


async def main(host, port, channel):
    async with publish_to_stream(host, port) as writer:
        print("Initiating the program...")
        assert 1 + 1 == 2
        print("Doing a bunch of stuff...")

        chan = channel.encode()

        for i in range(10):
            msg = str(i).encode()
            try:
                await write_data(writer, chan)
                await write_data(writer, msg)
            except OSError:
                print("Connection ended.")
                break
        print("Done")


if __name__ == "__main__":
    try:
        asyncio.run(main("127.0.0.1", 8000, "/general"))
    except KeyboardInterrupt:
        print("Bye!")
