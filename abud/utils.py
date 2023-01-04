from asyncio import StreamReader, StreamWriter


async def read_data(stream: StreamReader) -> bytes:
    """Read data from a stream by reading the size of the payload then the payload.

    Arguments
    ---------
    stream : StreamReader
        Read open socket to stream.

    Returns
    -------
    data : bytes
        Bytes of received data.
    """
    size_bytes = await stream.readexactly(4)
    size = int.from_bytes(size_bytes, byteorder="big")
    data = await stream.readexactly(size)
    return data


async def write_data(stream: StreamWriter, data: bytes):
    """Write data to a stream.

    The data is sent using the following format: the 4 first bytes correspond to the
    size of the payload in bytes, the subsequent bytes represent the actual payload.

    Arguments
    ---------
    stream : StreamWriter
        Write open socket to stream.

    data : bytes
        Bytes of data to send.
    """
    size_bytes = len(data).to_bytes(4, byteorder="big")
    stream.writelines([size_bytes, data])
    await stream.drain()
