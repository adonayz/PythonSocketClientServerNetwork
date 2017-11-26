import sys
import socket
import thread


buffer_size = 1024
address = "localhost"


def start_server_thread(conn, client_address):
    file_path = ""

    print ("Thread started")
    print "Connection from ", client_address

    get_request = conn.recv(buffer_size)

    if get_request.startswith('GET /'):
        path_end = get_request.find(' HTTP/')
        if path_end != -1:
            file_path = get_request[5:path_end]

    response_header = "HTTP/1.1 200 OK\r\n"

    try:
        file_object = open(file_path, "r")
        conn.send(response_header)
        line = file_object.read(buffer_size)
        while line:
            conn.send(line)
            line = file_object.read(buffer_size)
        file_object.close()
    except IOError:
        response_header = "404 Not Found"
        conn.send(response_header)

    conn.shutdown(socket.SHUT_RDWR)
    conn.close()


def main():
    if len(sys.argv) == 2:
        server_socket = socket.socket()
        server_socket.bind((address, int(sys.argv[1])))
        server_socket.listen(10)
        while True:
            print ("Server Running...")
            connection_info = server_socket.accept()
            thread.start_new_thread(start_server_thread, connection_info)
    else:
        print ("\nInvalid arguments. Please enter valid arguments.")
        print ("\nUse the following format\n\thttp_server.py port_number")
        sys.exit()
main()
