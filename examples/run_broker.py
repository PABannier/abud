import asyncio
from abud import connect_to_broker


async def main(*args, **kwargs):
    server = await asyncio.start_server(*args, **kwargs)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main(connect_to_broker, host="127.0.0.1", port=8000))
    except KeyboardInterrupt:
        print("Bye!")
