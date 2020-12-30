import os
import socket

if os.name == 'nt':

    def get_network_address():
        own_host = socket.gethostbyname(socket.gethostname())
        host_bytes = own_host.split('.')
        return ".".join(host_bytes[0:3] + ["0"])

else:

    import subprocess

    def get_hostname():
        result = subprocess.run(
            ["ifconfig", "wlan0"],
            encoding='utf-8',
            capture_output=True
        )
        result_str = result.stdout
        idx = result_str.find('inet ')
        return result_str[idx:].split(' ')[1]

    def get_network_address():
        own_host = get_hostname()
        host_bytes = own_host.split('.')
        return ".".join(host_bytes[0:3] + ["0"])
