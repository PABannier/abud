import asyncio
import uuid
from utils import write_data


async def main(host, port):
    me = uuid.uuid4().hex[:8]
    print(f"Starting up {me}")
    _, writer = await asyncio.open_connection(host=host, port=port)
    print(f"I am {writer.get_extra_info('sockname')}")

    try:
        for i in range(100):
            await asyncio.sleep(1)
            message = str(i)
            data = message.encode()
            try:
                await write_data(writer, data)
            except OSError:
                print("Connection ended.")
                break
    except asyncio.CancelledError:
        writer.close()
        await writer.wait_closed()


try:
    asyncio.run(main("127.0.0.1", 8000))
except KeyboardInterrupt:
    print("Bye!")
