from asyncio import StreamReader, StreamWriter
from io import BytesIO

from construct import GreedyRange
from construct.lib import Container


class Client_Handler:
    def __init__(self, reader_format, writer_format, queue):
        self.reader_format = reader_format
        self.writer_format = writer_format
        self.queue = queue

    async def handle_client(self, reader: StreamReader, writer: StreamWriter):
        greedy_format = GreedyRange(self.reader_format)

        filename = "tmp.log"  # datetime.now().strftime('%Y-%m-%dT%H-%M-%SZ')+".log"

        with open(filename, "w") as output:

            bytes_remaining = b""
            count = 0
            while True:
                count += 1
                incoming_data = await reader.read(4086)
                byte_stream = BytesIO(bytes_remaining + incoming_data)
                request = greedy_format.parse_stream(byte_stream)
                bytes_remaining = byte_stream.read()
                for r in request:
                    # output.write(f"{r.event_id},{r.start_time},{r.end_time},{r.ax},{r.ay},{r.az},{r.aw},{r.gx},{r.gy},{r.gz},{r.gw}\n")
                    output.write(f"{r}\n")
                    output.flush()
                if count % 10 == 0:
                    print(f"processed {count} logs.")

                if not self.queue.empty():
                    print("sending stuff!")
                    container_to_send = self.queue.get()
                    print(container_to_send)
                    bytes_to_send = self.writer_format.build(container_to_send)
                    print(container_to_send)
                    print(bytes_to_send)
                    writer.write(bytes_to_send)
                    await writer.drain()

                else:
                    print("not sending stuff")
