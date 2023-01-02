import asyncio
from contextlib import asynccontextmanager
import uuid
from utils import write_data


@asynccontextmanager
async def publish_to_stream(host: str, port: int):
    me = uuid.uuid4().hex[:8]
    print(f"Starting up {me}")
    _, writer = await asyncio.open_connection(host=host, port=port)
    print(f"I am {writer.get_extra_info('sockname')}")

    # subscribing to /null since we are publisher (handshake with broker)
    await write_data(writer, b'/null')

    try:
        yield writer
    except asyncio.CancelledError:
        writer.close()
        await writer.wait_closed()
    finally:
        writer.close()
        await writer.wait_closed()
        print("Released connection to broker.")
