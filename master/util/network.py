import socket


def get_network_address():
    own_host = socket.gethostbyname(socket.gethostname())
    host_bytes = own_host.split('.')
    return ".".join(host_bytes[0:3] + ["0"])
