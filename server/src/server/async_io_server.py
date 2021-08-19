from asyncio import StreamReader, StreamWriter
from io import StringIO, BytesIO

from construct import Struct, Int32ul, GreedyRange, Rebuffered
import asyncio

HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
PORT = 12345        # Port to listen on (non-privileged ports are > 1023)

format = Struct(
     # "signature" / Const(b"BMP"),
     "width" / Int32ul,
     "height" / Int32ul,
     # "pixels" / Array(this.width * this.height, Byte),
)

t = format.parse(b'\n\x00'*100)
chunk_size = len(format.build(t))


async def handle_client(reader: StreamReader, writer: StreamWriter):
    greedy_format = GreedyRange(format)
    bytes_remaining = b""
    while True:
        incoming_data = await reader.read(4086)
        byte_stream = BytesIO(bytes_remaining+incoming_data)
        request = greedy_format.parse_stream(byte_stream)
        bytes_remaining = byte_stream.read()
        print(len(incoming_data))
        print(len(request))
        # response = str(eval(request)) + '\n'
        # writer.write(response.encode('utf8'))
        # await writer.drain()
    writer.close()

async def run_server():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    async with server:
        await server.serve_forever()

asyncio.run(run_server())
