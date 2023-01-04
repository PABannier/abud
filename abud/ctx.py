import asyncio
from contextlib import AbstractAsyncContextManager
from threading import Thread
import time
from abud.publisher import Publisher
from abud.server import connect_to_broker


def _start_server(host: str, port: int):
    async def _start_cb(server_fn, host, port):
        broker = await asyncio.start_server(server_fn, host=host, port=port)
        async with broker:
            await broker.serve_forever()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_start_cb(connect_to_broker, host, port))
    loop.close()


class stream_data(AbstractAsyncContextManager):
    """Context manager for streaming data."""

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    async def __aenter__(self):
        """Spawn a thread to run a broker and yield a publisher."""
        self.server_thread = Thread(
            target=_start_server, args=(self.host, self.port), daemon=True)
        self.server_thread.start()
        time.sleep(2)  # TODO: rm that
        self.publisher = await Publisher(self.host, self.port).connect()
        return self.publisher

    async def __aexit__(self, *args, **kwargs):
        """Close the connection to broker and kills the thread."""
        await self.publisher.close()
