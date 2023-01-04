import asyncio
import uuid
from abud.utils import read_data, write_data


class Subscriber:
    """Subscriber to stream channels.

    Attributes
    ----------
    host : str
        Host.

    port : int
        Port.

    id : str
        Unique id.
    """

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.id = uuid.uuid4().hex[:8]

    async def connect(self, channel: str):
        """Connect to the specified channel.

        Parameters
        ----------
        channel : str
            Channel to connect.
        """
        try:
            self.reader, self.writer = await asyncio.open_connection(
                self.host, self.port)
            chan = channel.encode()
            await write_data(self.writer, chan)  # subscribing to `channel`
            print(f"Starting up {self.writer.get_extra_info('sockname')} ({self.id})")
            print(f"Subscribed to {channel}.")
        except ConnectionRefusedError as exception:
            print(f"Could not connected to server: {exception}")

    async def listen(self):
        """Keep listening to the specified channel waiting for data to read."""
        try:
            while data := await read_data(self.reader):
                print(f"Received: {data[:20]}")
            print("Connection ended.")
        except asyncio.IncompleteReadError:
            print("Server closed.")
        finally:
            self.writer.close()
            await self.writer.wait_closed()
