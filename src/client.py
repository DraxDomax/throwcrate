import time
import socket
import json
import os

import file_ops
import list_comparator
import tcp_common

SERVER_HOST = "localhost"
SERVER_PORT = 9181
SOURCE_DIR_POLL_INTERVAL = 3
TRANSFER_CHUNK_SIZE = 1024 * 8
TRANSFER_MSG_ENCODING = "utf-8"


def main():
    source_dir = input("Enter directory to watch (absolute path): ")
    client(source_dir)


def client(source_dir):
    # source_dir = "C:\\Storage\\test\\watched"
    source_dir_treated = source_dir.replace("\\", "/") + "/"

    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((SERVER_HOST, SERVER_PORT))
            tcp_common.write_message(client_socket, "send_cat|")
            des_catalog_serial = tcp_common.read_message(client_socket)

            src_catalog = file_ops.get_current_catalog_dictionary(source_dir)
            src_catalog_serial = json.dumps(src_catalog)

            if des_catalog_serial != src_catalog_serial:

                des_catalog = json.loads(des_catalog_serial)
                des_folders = des_catalog["subdirectories"]
                des_files = des_catalog["files_hashes"]

                src_folders = src_catalog["subdirectories"]
                src_files = src_catalog["files_hashes"]

                dirs_exclusive_to_des, dirs_exclusive_to_src = \
                    list_comparator.annihilate(des_folders, src_folders)
                files_exclusive_to_des, files_exclusive_to_src = \
                    list_comparator.annihilate(des_files, src_files)

                # Semantic sugar and also, let's look out for duplicates:
                dirs_to_create = dirs_exclusive_to_src
                dirs_to_delete = dirs_exclusive_to_des
                files_to_create = files_exclusive_to_src
                files_to_delete = files_exclusive_to_des

                for current_mkdir in dirs_to_create:
                    print("Instructing server to make dir: " + current_mkdir)
                    tcp_common.write_message(client_socket, "mkdir|" + current_mkdir)
                    response = tcp_common.read_message(client_socket)
                    print(response)

                for current_rmdir in dirs_to_delete:
                    print("Instructing server to remove dir: " + current_rmdir)
                    tcp_common.write_message(client_socket, "rmdir|" + current_rmdir)
                    response = tcp_common.read_message(client_socket)
                    print(response)

                for current_rm_file_entry in files_to_delete:
                    current_rm_file = current_rm_file_entry[0]
                    print("Instructing server to remove file: " + current_rm_file)
                    tcp_common.write_message(client_socket, "del_file|" + current_rm_file)
                    response = tcp_common.read_message(client_socket)
                    print(response)

                for current_mk_file_entry in files_to_create:
                    current_mk_file = current_mk_file_entry[0]
                    current_mk_file_hash = current_mk_file_entry[1]
                    print("Instructing server to create file: " + current_mk_file)
                    tcp_common.write_message(client_socket, "crt_file|" + current_mk_file + "|" + current_mk_file_hash)
                    response = tcp_common.read_message(client_socket)
                    print(response)
                    if response != "Server: File cloned.":
                        file_to_send = source_dir_treated + current_mk_file
                        with open(file_to_send, "rb") as current_file:
                            file_size = os.stat(file_to_send).st_size
                            tcp_common.write_message(client_socket, str(file_size))
                            client_socket.sendfile(current_file)
                        response = tcp_common.read_message(client_socket)
                        print(response)

            tcp_common.write_message(client_socket, "hangup|")
            print(".", end="")
            time.sleep(SOURCE_DIR_POLL_INTERVAL)


# Not super confident about "modules"... I am a Java guy, main() is main()!
if __name__ == '__main__':
    main()
