import select
import socket


HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
PORT = 12345        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    while True:

        try:
            conns = [s]
            while True:
                try:
                    ready_to_read, ready_to_write, in_error = \
                        select.select(conns, [], conns, 1)

                except select.error:
                    conn.shutdown(2)    # 0 = done receiving, 1 = done sending, 2 = both
                    conn.close()
                    # connection error event here, maybe reconnect
                    print('connection error')
                    break
                for cur_conn in ready_to_read:
                    if cur_conn == s:
                        print("going to accept")
                        conn, addr = s.accept()
                        print(conn)
                        conns.append(conn)
                    else:
                        recv = cur_conn.recv(16)
                        # do stuff with received data
                        print(f'received: {recv}')
                # for cur_conn in ready_to_write:
                #     # connection established, send some stuff
                #     cur_conn.send(b'.\n.')
        except Exception as e:
            print(e)




#
# import socket
# import select
#
# HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
# PORT = 12345        # Port to listen on (non-privileged ports are > 1023)
# while True:
#     print("starting a new socket\n")
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.bind((HOST, PORT))
#         s.listen()
#         conn, addr = s.accept()
#         with conn:
#             print('Connected by', addr)
#             has_data = True
#             while has_data:
#                 read_sockets, write_sockets, error_sockets = select.select([conn], [], [])
#                 for sock in read_sockets:
#                     data = conn.recv(10)
#                     if not data:
#                         has_data = False;
#                         break
#                     print(data, "\n")
#                     conn.sendall(data)
#     print("socket closed")
