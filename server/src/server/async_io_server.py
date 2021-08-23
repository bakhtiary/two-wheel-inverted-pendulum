from asyncio import StreamReader, StreamWriter
from datetime import datetime

from io import BytesIO

from construct import Struct, Int32ul, GreedyRange, Rebuffered, Int64ul, Single, Single, Double, Float32b, Float32l, \
    Float64l, Int64ub
import asyncio

HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
PORT = 12345        # Port to listen on (non-privileged ports are > 1023)

format = Struct(
     # "signature" / Const(b"BMP"),
     "event_id" / Int32ul,
     "start_time" / Int32ul,
     "end_time" / Int32ul,
     "ax" / Float32l,
     "ay" / Float32l,
     "az" / Float32l,
     "gx" / Float32l,
     "gy" / Float32l,
     "gz" / Float32l,
)

t = format.parse(b'\n\x00'*100)
chunk_size = len(format.build(t))

print(f"chunk_size is {chunk_size}")

async def handle_client(reader: StreamReader, writer: StreamWriter):
    greedy_format = GreedyRange(format)

    filename = "tmp.log" #datetime.now().strftime('%Y-%m-%dT%H-%M-%SZ')+".log"

    with open(filename, "w") as output:

        bytes_remaining = b""
        count = 0
        while True:
            count += 1
            incoming_data = await reader.read(4086)
            byte_stream = BytesIO(bytes_remaining+incoming_data)
            request = greedy_format.parse_stream(byte_stream)
            bytes_remaining = byte_stream.read()
            for r in request:
                # output.write(f"{r.event_id},{r.start_time},{r.end_time},{r.ax},{r.ay},{r.az},{r.aw},{r.gx},{r.gy},{r.gz},{r.gw}\n")
                output.write(f"{r}")
                output.flush()
            if count % 10 == 0:
                print(f"processed {count} logs.")
            # response = str(eval(request)) + '\n'
            # writer.write(response.encode('utf8'))
            # await writer.drain()

        writer.close()

async def run_server():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    async with server:
        await server.serve_forever()

asyncio.run(run_server())
