import pathlib
import socket
import os
import json

import tcp_common
import file_ops

SERVER_PORT = 9181
RAM_COPY_CHUNK_SIZE = 16 * 1024 * 1024
TRANSFER_CHUNK_SIZE = 1024 * 8


def main():
    destination = input("Enter directory to watch (absolute path): ")
    server(destination)


def server(destination):
    # destination = "C:\\Storage\\test\\stash"
    destination_treated = destination.replace("\\", "/") + "/"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(("", SERVER_PORT))  # Bind to any address requested on the agreed port
        server_socket.listen(1)
        print("Startup finished. Listening...")

        while True:
            current_socket, client_address = server_socket.accept()
            print("Connected to: ", client_address)
            with current_socket:
                while True:
                    message = tcp_common.read_message(current_socket)
                    message_parts = message.split("|")
                    instruction = message_parts[0]

                    if instruction == "rmdir":
                        file_ops.rmdir(destination_treated + message_parts[1])  # Some validation here?
                        tcp_common.write_message(current_socket, "Server: Directory removed.")

                    elif instruction == "mkdir":
                        pathlib.Path(destination_treated + message_parts[1]) \
                            .mkdir(parents=True, exist_ok=True)
                        tcp_common.write_message(current_socket, "Server: Directory created.")

                    elif instruction == "del_file":
                        file = destination_treated + message_parts[1]
                        if os.path.exists(file):
                            os.remove(file)
                        tcp_common.write_message(current_socket, "Server: File removed")

                    elif instruction == "crt_file":
                        hash_string = message_parts[2]
                        subdirectories, files_hashes = file_ops.get_current_catalog(destination)
                        local_new = destination_treated + message_parts[1]

                        cloned = False
                        for existing_file in files_hashes:
                            if existing_file[1] == hash_string:
                                local_existing = existing_file[0]
                                with open(local_existing, 'rb') as local_src, open(local_new, 'wb') as local_des:
                                    while True:
                                        block = local_src.read(RAM_COPY_CHUNK_SIZE)
                                        if not block:
                                            break
                                        local_des.write(block)
                                cloned = True
                                break

                        if cloned:
                            tcp_common.write_message(current_socket, "Server: File cloned.")
                        else:
                            tcp_common.write_message(current_socket, "Server: Requiring file stream.")
                            file_size = int(tcp_common.read_message(current_socket))

                            written = 0
                            with open(local_new, "wb") as local_des:
                                while True:
                                    file_chunk = current_socket.recv(TRANSFER_CHUNK_SIZE)
                                    if not file_chunk:
                                        break
                                    local_des.write(file_chunk)
                                    written += len(file_chunk)
                                    if written == file_size:
                                        break

                            tcp_common.write_message(current_socket, "Server: Downloaded file.")

                    elif instruction == "hangup":
                        break

                    elif instruction == "send_cat":
                        catalog = file_ops.get_current_catalog_dictionary(destination)
                        catalog_serial = json.dumps(catalog)
                        tcp_common.write_message(current_socket, catalog_serial)


if __name__ == '__main__':
    main()
