import socket

from contextlib import closing

def test_connection(host, port):
    """ Test a connection to a host/port """

    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        return bool(sock.connect_ex((host, port)) == 0)
