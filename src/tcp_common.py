BUFFER_SIZE = 8096
TIMEOUT = 6
HEADER_SIZE = 4
TRANSFER_MSG_ENCODING = "utf-8"


def write_message(socket, message):
    msg_bytes = message.encode(TRANSFER_MSG_ENCODING)
    header_value = len(msg_bytes)
    header_bytes = header_value.to_bytes(HEADER_SIZE, "big")

    socket.send(header_bytes)
    socket.sendall(msg_bytes)


def read_message(socket):
    header = socket.recv(HEADER_SIZE)
    message_length = int.from_bytes(header, byteorder='big', signed=False)
    message_bytes = socket.recv(message_length)
    return message_bytes.decode(TRANSFER_MSG_ENCODING)


