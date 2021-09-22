import multiprocessing as mp
from construct import Container
import asyncio

from server.communication_structures import robot_read_format2, robot_write_format2
from server.esp_client_handler import Client_Handler
from server.web_server import run_ui_web_server

HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
PORT = 12345  # Port to listen on (non-privileged po rts are > 1023)


if __name__ == '__main__':
    mp.set_start_method('spawn')
    q = mp.Queue()
    default_initial_control_params = Container(proportional=200, integration=10, derivative=500, minimal_motor_power=5, offset=0.0, delay_time=0)
    p = mp.Process(target=run_ui_web_server, args=(q, default_initial_control_params))
    p.start()

    async def run_server():
        client_Handler = Client_Handler(robot_read_format2, robot_write_format2, q)
        server = await asyncio.start_server(lambda x, y: client_Handler.handle_client(x, y), HOST, PORT)
        async with server:
            await server.serve_forever()

    asyncio.run(run_server())