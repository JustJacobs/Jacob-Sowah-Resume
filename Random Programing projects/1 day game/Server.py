import socket
import threading
import json
import sqlite3

import sql_functions

HOST = '127.0.0.1'
PORT = 5050

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

clients = []
host_connection = None
start_command_issued = False
finished_clients = set()
host_socket = None
c = sqlite3.connect('Projectiles_leaderbord.db')


def handle_client(client_socket, address):
    global host_connection, start_command_issued, finished_clients, host_socket, c

    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break

            received_data = data.decode()
            received_dict = json.loads(received_data)

            if received_dict.get("command") == "Databace":
                if received_dict.get("ececute") == "Leaderbored":
                    info_to_send = sql_functions.SQL_select(f"SELECT * FROM {received_dict.get('Table')}", ())
                    client_socket.send(json.dumps(info_to_send).encode())
                elif received_dict.get("ececute") == "ADD":
                    sql_functions.SQL_insert(
                        f"INCERT INTO {received_dict.get('Table')} (NAME,SCORE) VALUES ({received_dict.get('NAME')},{received_dict.get('SCORE')})",
                        ())



            elif received_dict.get("command") == "Host":
                if host_connection is None:
                    host_socket = client_socket
                    host_connection = address
                    print(f"Host connected: {address}")
                    print(host_socket)
                else:
                    print("Another host tried to connect, only one host allowed at a time")

            elif received_dict.get("command") == "Join":
                if host_connection and not start_command_issued:
                    clients.append([client_socket, address, received_dict])
                    print(f"Client joined: {address}")
                    # Send the list of dictionaries to the host
                    client_info = received_dict.get("info")
                    message = {"command": "name", "info": client_info}
                    host_socket.sendall(json.dumps(message).encode())
                    print(f"sent{client_info} to {host_socket}")

                elif start_command_issued:
                    print("Start command issued, cannot accept new 'Join' clients")
                else:
                    print("No host connected, cannot accept 'Join' command")

            elif received_dict.get("command") == "Start":
                if host_connection == address:
                    start_command_issued = True
                    print("recieved")
                    start_msg = {"command": "start"}
                    for client in clients:
                        client[0].send(json.dumps(start_msg).encode())
                    print("Sent 'start' command to all Join clients")

            elif received_dict.get("command") == "Finished":
                finished_clients.add(address)
                print(f"Client {address} finished")
                host_socket.sendall(json.dumps(received_dict).encode())
                print(f"sent{received_dict} to {host_socket}")

                # Check if all Join clients have finished
                join_clients = [client for client, data in clients if data["command"] == "Join"]
                if len(finished_clients) == len(join_clients):
                    if host_connection:
                        host_socket = [client[0] for client in clients if client[0] == host_connection][0]
                        host_socket.send("finished".encode())
                        print("Sent 'finished' command to host")

        except Exception as e:
            print(f"Error: {e}")
            break

    if address == host_connection:
        host_connection = None
        print(f"Host disconnected: {address}")

    if (address) in clients:
        clients.remove((address))
        print(f"Client disconnected: {address}")

    client_socket.close()


def start_server():
    server.listen()
    print(f"Server is listening on {HOST}:{PORT}")

    while True:
        client_socket, address = server.accept()
        print(f"Connection from {address} has been established!")

        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()


start_server()
