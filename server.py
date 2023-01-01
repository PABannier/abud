import asyncio
from asyncio import StreamReader, StreamWriter, gather
from utils import read_data, write_data


SUBSCRIBERS = []


async def server(reader: StreamReader, writer: StreamWriter):
    peername = writer.get_extra_info('peername')
    print(f"Remote {peername} joined.")
    SUBSCRIBERS.append(writer)

    try:
        while data := await read_data(reader):
            print(f"Send: {data[:19]}...")
            await gather(*[write_data(sub, data) for sub in SUBSCRIBERS])
    except asyncio.CancelledError:
        print(f"Remote {peername} closing connection.")
    except asyncio.IncompleteReadError:
        print(f"Remote {peername} disconnected.")
    finally:
        print(f"Remote {peername} closed.")
        SUBSCRIBERS.remove(writer)


async def main(*args, **kwargs):
    server = await asyncio.start_server(*args, **kwargs)
    async with server:
        await server.serve_forever()


try:
    asyncio.run(main(server, host="127.0.0.1", port=8000))
except KeyboardInterrupt:
    print("Bye!")
