import asyncio
from asyncio import StreamReader, StreamWriter, Queue
from contextlib import suppress
from collections import defaultdict, deque
from typing import Dict
from utils import read_data, write_data


# Maps every channel to a list of subscribers
SUBSCRIBERS: defaultdict[bytes, deque[StreamWriter]] = defaultdict(deque)
# Maps every subscriber to a list of messages to be broadcasted 
SEND_QUEUES: defaultdict[StreamWriter, Queue] = defaultdict(Queue)
# Maps every channel to a list of messages to be broadcasted
CHANNEL_QUEUES: Dict[bytes, Queue] = {}


async def run_broker(reader: StreamReader, writer: StreamWriter):
    peername = writer.get_extra_info('peername')
    subscriber_channel = await read_data(reader)
    SUBSCRIBERS[subscriber_channel].append(writer)
    send_task = asyncio.create_task(send_to_subscriber(writer, SEND_QUEUES[writer]))

    print(f"Remote {peername} subscribed to {subscriber_channel}.")

    try:
        while channel_name := await read_data(reader):
            data = await read_data(reader)
            if channel_name not in CHANNEL_QUEUES:
                CHANNEL_QUEUES[channel_name] = Queue(maxsize=10)
                asyncio.create_task(send_to_channel(channel_name))
            await CHANNEL_QUEUES[channel_name].put(data)
    except asyncio.CancelledError:
        print(f"Remote {peername} closing connection.")
    except asyncio.IncompleteReadError:
        print(f"Remote {peername} disconnected.")
    finally:
        print(f"Remote {peername} closed.")
        await SEND_QUEUES[writer].put(None)
        await send_task
        del SEND_QUEUES[writer]
        SUBSCRIBERS[subscriber_channel].remove(writer)


async def send_to_subscriber(writer: StreamWriter, queue: Queue):
    while True:
        try:
            data = await queue.get()
        except asyncio.CancelledError:
            continue
        
        if not data:
            break
    
        try:
            await write_data(writer, data)
        except asyncio.CancelledError:
            await write_data(writer, data)
    
    writer.close()
    await writer.wait_closed()


async def send_to_channel(channel_name: bytes):
    with suppress(asyncio.CancelledError):
        while True:
            writers = SUBSCRIBERS[channel_name]
            if not writers:
                await asyncio.sleep(1)
                continue
            if not (msg := await CHANNEL_QUEUES[channel_name].get()):
                break
            for writer in writers:
                if not SEND_QUEUES[writer].full():
                    print(f"Send: {msg[:19]}...")
                    await SEND_QUEUES[writer].put(msg)


async def main(*args, **kwargs):
    server = await asyncio.start_server(*args, **kwargs)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main(run_broker, host="127.0.0.1", port=8000))
    except KeyboardInterrupt:
        print("Bye!")
