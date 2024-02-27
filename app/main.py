# Uncomment this to pass the first stage
import socket
import threading

def handleConnect(conn, data):
    with conn:
        while True:
            conn.recv(1024)
            conn.send(data.encode())

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    pong = "+PONG\r\n"

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    
    
    #the with statement used for continuse use case
    while True:
        conn, addr = server_socket.accept()
        conn_thread = threading.Thread(target=handleConnect, args=(conn,pong))
        conn_thread.start()


if __name__ == "__main__":
    main()
