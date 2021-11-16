import asyncio
from asyncio import StreamReader, StreamWriter

from construct import Int32ul

from server.data_descriptors import DataDescriptors, DataDescriptorsFactory


class Client_Handler:
    def __init__(self, queue, ddf: DataDescriptorsFactory):
        self.queue = queue
        self.ddf = ddf

    async def handle_client(self, reader: StreamReader, writer: StreamWriter):

        filename = "tmp2.log"  # datetime.now().strftime('%Y-%m-%dT%H-%M-%SZ')+".log"
        dd: DataDescriptors = self.ddf.makeDD()
        with open(filename, "w") as output:

            count = 0
            while True:
                count += 1
                try:
                    incoming_data = await asyncio.wait_for(reader.read(4086), 0.5)
                    request = dd.parse_incoming_data(incoming_data)
                    for r in request:
                        output.write(f"{r}\n")
                        output.flush()

                    if count % 100 == 0:
                        print(f"processed {count} logs.")
                except Exception :
                    pass

                if not self.queue.empty():
                    print("sending stuff!")
                    container_to_send = self.queue.get()
                    print(container_to_send)
                    bytes_to_send = dd.build(container_to_send)
                    writer.write(bytes_to_send)
                    await writer.drain()
                else:
                    pass