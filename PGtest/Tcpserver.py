from distutils.command.clean import clean
from pydoc import cli
import socket
import sys


def start_tcp_server(ip, port):
    # create socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (ip, port)
    # bind port
    print ('starting listen on ip %s, port %s' % server_address)
    sock.bind(server_address)
    # starting listening, allow only one connection
    try:
        sock.listen(1)
    except socket.error as e:
        print ("fail to listen on port %s" % e)
        sys.exit(1)
    while True:
        print ("waiting for connection")
        client, addr = sock.accept()
        print ('having a connection:%s',addr)
        b = "get out\n"
        a = b.encode()
        client.send(a)
        client.close()

if __name__ == '__main__':
    start_tcp_server('localhost', 8080)