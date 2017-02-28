import socket

from contextlib import closing


def can_connect_to(host, port):
    """ Test a connection to a host/port """

    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        return bool(sock.connect_ex((host, port)) == 0)
