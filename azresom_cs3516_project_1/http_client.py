from datetime import datetime
import socket
import sys
import re


def check_if_ip(ip_input):
    # some of the following filtration code from
    # https://stackoverflow.com/questions/3462784/check-if-a-string-matches-an-ip-address-pattern-in-python
    ip_match = re.match('^' + '[\.]'.join(['(\d{1,3})']*4) + '$', ip_input)
    ip_validate = bool(ip_match)
    if ip_validate:
        ip_validate &= all(map(lambda n: 0 <= int(n) <= 255, ip_match.groups()))
    return ip_validate


def filter_address(server_address):
    if server_address.startswith('http://'):
        server_address = server_address[7:len(server_address)]
    elif server_address.startswith('https://'):
        server_address = server_address[8:len(server_address)]

    if check_if_ip(server_address):
        return server_address, '/'

    path = '/'
    has_path = server_address.find('/')

    if has_path != -1:
        path = server_address[has_path:len(server_address)]
        server_address = server_address[0:has_path]

    sections = server_address.split('.')

    if not server_address.startswith('www.'):
        if len(sections) == 2:
            server_address = 'www.' + server_address
        elif len(sections) > 2:
            if sections[-2] in {'co', 'ac', 'me', 'gov', 'org', 'net', 'com', 'edu', 'io', 'ly', 'sh', 'fm', 'us', 'to',
                                'ly', 'is'}:
                if len(sections) < 4:
                    server_address = 'www.' + server_address
            else:
                if len(sections) < 3:
                    server_address = 'www.' + server_address

    return server_address, path


def request_page(server_address, port, ttl_flag):
    buffer_size = 1024
    host_address, path = filter_address(server_address)

    request = "GET " + path + " HTTP/1.1\r\nHost: " + host_address + "\r\nConnection: close\r\n" \
                                                                     "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\nUpgrade-Insecure-Requests: 1\r\n" \
                                                                     "User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36\r\n\r\n"

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host_address, port))

    time_sent = datetime.utcnow()

    client_socket.send(request)

    result = client_socket.recv(buffer_size)

    time_received = datetime.utcnow()
    rtt = (time_received - time_sent).microseconds / 1000

    if ttl_flag:
        print "\nRTT is equal to ", rtt, " milliseconds\n"

    while len(result) > 0:
        print(result)
        result = client_socket.recv(buffer_size)

    if ttl_flag:
        print "\nRTT is equal to ", rtt, " milliseconds\n"

    client_socket.close()
    sys.exit()


def main():
    if len(sys.argv) == 3 and sys.argv[2].isdigit():
        request_page(sys.argv[1], int(sys.argv[2]), False)
    elif (len(sys.argv) == 4) and (sys.argv[1] == "--ttl"):
        request_page(sys.argv[2], int(sys.argv[3]), True)
    else:
        print ("\nInvalid arguments. Please enter valid arguments.")
        print ("\nUse the following format\n\thttp_client.py [--ttl] server_url port_number")
        print ("\n\t*Hint* --ttl flag is optional\n")
        sys.exit()


main()
