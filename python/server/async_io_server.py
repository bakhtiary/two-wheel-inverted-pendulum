import multiprocessing as mp
import os

import asyncio

from server.data_descriptors import DataDescriptors, DataDescriptorsFactory
from server.esp_client_handler import Client_Handler
from server.web_server import run_ui_web_server

HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
PORT = 12345  # Port to listen on (non-privileged po rts are > 1023)

filename = f"{os.getenv('REPOSITORY_ROOT')}/WiFiClient/lib_remote_registry/remote_registry_data.h"

ddf = DataDescriptorsFactory(filename)

if __name__ == '__main__':
    mp.set_start_method('spawn')
    q = mp.Queue()
    p = mp.Process(target=run_ui_web_server, args=(q, ddf))
    p.start()

    async def run_server():
        client_Handler = Client_Handler(q, ddf)
        server = await asyncio.start_server(lambda x, y: client_Handler.handle_client(x, y), HOST, PORT)
        async with server:
            await server.serve_forever()

    asyncio.run(run_server())
