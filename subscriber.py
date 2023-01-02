import asyncio
import uuid
from utils import read_data, write_data


async def client(host: str, port: int, channel: str):
    me = uuid.uuid4().hex[:8]
    print(f"Starting up {me}")
    reader, writer = await asyncio.open_connection(host, port)

    # subscribing to `channel`
    chan = channel.encode()
    await write_data(writer, chan)

    try:
        while data := await read_data(reader):
            print(f"Received by {me}: {data[:20]}")
        print("Connection ended.")
    except asyncio.IncompleteReadError:
        print("Server closed.")
    finally:
        writer.close()
        await writer.wait_closed()


if __name__ == "__main__":
    try:
        asyncio.run(client("127.0.0.1", 8000, "/general"))
    except KeyboardInterrupt:
        print("Bye!")
