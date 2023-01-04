import asyncio
from abud.server import run_broker


async def main(*args, **kwargs):
    server = await asyncio.start_server(*args, **kwargs)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main(run_broker, host="127.0.0.1", port=8000))
    except KeyboardInterrupt:
        print("Bye!")
