import asyncio
import uuid
from utils import write_data


async def main(host: str, port: int, channel: str):
    me = uuid.uuid4().hex[:8]
    print(f"Starting up {me}")
    _, writer = await asyncio.open_connection(host=host, port=port)
    print(f"I am {writer.get_extra_info('sockname')}")

    # subscribing to /null since we are publisher
    await write_data(writer, b'/null')

    chan = channel.encode()

    try:
        for i in range(100):
            await asyncio.sleep(1)
            message = str(i).encode()
            try:
                await write_data(writer, chan)
                await write_data(writer, message)
            except OSError:
                print("Connection ended.")
                break
    except asyncio.CancelledError:
        writer.close()
        await writer.wait_closed()


if __name__ == "__main__":
    try:
        asyncio.run(main("127.0.0.1", 8000, "/general"))
    except KeyboardInterrupt:
        print("Bye!")
