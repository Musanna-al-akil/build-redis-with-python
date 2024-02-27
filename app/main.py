# Uncomment this to pass the first stage
import socket
import logging
from threading import Thread

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("redis_server")

PONG_MSG = "+PONG\r\n"
kv = {}

def encodeString(data):
    return b"$" +str(len(data)).encode() + b"\r\n" + data.encode() + b"\r\n"


def processString(data, conn):
    num_opts = data[0]
    length = data[1]
    command = data[2].lower()
    
    if command == "ping":
        conn.send(PONG_MSG.encode())
        logger.info("Reply PONG to client")
    elif command == "echo":
        echo_str = data[4]
        conn.send(encodeString(echo_str))
        logger.info(f"Echo {message} back to client")
    elif command == "set":
        key = data[4]
        value = data[6]
        kv[key] = value
        conn.send(encodeString('OK'))
        logger.info(f"Set {key} to {value}")
    elif command == "get":
        key = data[4]
        if data[4] in kv:
            conn.send(encodeString(kv[key]))
            logger.info(f"Get {key} from store")
        else:
            conn.send(b"-1\r\n")
            logger.warning(f"get key not found")

    else:
        conn.send(encodeString('no command found'))
        logger.error(f"no command found")

def handleConnect(conn, addr):
    with conn:
        while True:
            data =  conn.recv(1024).decode().split("\r\n")
            if not data:
                break
            if len(data)> 0:
                if len(data[0]):
                    if data[0][0]  == "$" or data[0][0] == "*":
                        processString(data, conn)

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")


    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    server_socket.listen()

    logger.info("server created at 127.0.0.1:6379")
    #the with statement used for continuse use case
    while True:
        conn, addr = server_socket.accept()
        conn_thread = Thread(target=handleConnect, args=(conn, addr))
        conn_thread.start()


if __name__ == "__main__":
    main()
