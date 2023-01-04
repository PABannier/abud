import asyncio
import uuid
from abud.utils import write_data


class Publisher:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.id = uuid.uuid4().hex[:8]

    async def connect(self):
        try:
            _, self.writer = await asyncio.open_connection(
                host=self.host, port=self.port)
            # subscribing to /null since we are publisher
            await write_data(self.writer, b'/null')
            print(f"Starting up {self.writer.get_extra_info('sockname')} ({self.id})")
        except ConnectionRefusedError as exception:
            print(f"Could not connected to server: {exception}")
        return self

    async def close(self):
        self.writer.close()
        await self.writer.wait_closed()

    async def publish(self, message: str, channel: str):
        bytes_channel = channel.encode()
        bytes_message = message.encode()

        try:
            await write_data(self.writer, bytes_channel)
            await write_data(self.writer, bytes_message)
        except OSError:
            print("Connection ended.")
        except asyncio.CancelledError:
            self.close()
