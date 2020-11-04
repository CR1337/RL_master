import socket
import os

if os.name == 'nt':

    def get_network_address():
        own_host = socket.gethostbyname(socket.gethostname())
        host_bytes = own_host.split('.')
        return ".".join(host_bytes[0:3] + ["0"])

else:

    import fcntl
    import struct

    def get_hostname():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', 'wlan0'[:15])
        )[20:24])

    def get_network_address():
        own_host = get_hostname()
        host_bytes = own_host.split('.')
        return ".".join(host_bytes[0:3] + ["0"])
