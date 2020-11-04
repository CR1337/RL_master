import socket
import os

if os.name == 'nt':

    def get_network_address():
        own_host = socket.gethostbyname(socket.gethostname())
        host_bytes = own_host.split('.')
        return ".".join(host_bytes[0:3] + ["0"])

else:

    # import fcntl
    # import struct
    import subprocess

    # def _get_hostname():
    #     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #     return socket.inet_ntoa(fcntl.ioctl(
    #         s.fileno(),
    #         0x8915,  # SIOCGIFADDR
    #         struct.pack('256s', 'wlan0'[:15])
    #     )[20:24])

    def get_hostname():
        result = subprocess.run(["ifconfig", "wlan0"], encoding='utf-8', capture_output=True)
        result_str = result.stdout
        idx = result_str.find('inet ')
        return result_str[idx:].split(' ')[1]

    def get_network_address():
        own_host = get_hostname()
        host_bytes = own_host.split('.')
        return ".".join(host_bytes[0:3] + ["0"])
