import itertools
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from flask_api import status

from .device import Device
from .environment import Environment


class DeviceControllerError(Exception):
    pass


class InvalidDeviceId(DeviceControllerError, KeyError):
    def __init__(self, device_id):
        self.device_id = device_id


class DisconnectFailed(DeviceControllerError):
    def __init__(self, device_id):
        self.device_id = device_id


class DeviceController():
    _devices = dict()
    _registration_url = "/master-registration"

    @classmethod
    def _subnet_hosts(cls):
        # subnet_mask_bytes = [
        #     int(byte) for byte in Environment.get('SUBNET_MASK').split('.')
        # ]
        # hosts = list()
        # for ip_byte_0, ip_byte_1, ip_byte_2, ip_byte_3 in itertools.product(
        #     range(255 - subnet_mask_bytes[0] + 1),
        #     range(255 - subnet_mask_bytes[1] + 1),
        #     range(255 - subnet_mask_bytes[2] + 1),
        #     range(255 - subnet_mask_bytes[3] + 1)
        # ):
        #     hosts.append(".".join(
        #         [
        #             str(byte)
        #             for byte in [ip_byte_0, ip_byte_1, ip_byte_2, ip_byte_3]
        #         ]
        #     ))
        # return hosts

        # TODO: This is a QAD-Fix!:
        subnet_mask = Environment.get('SUBNET_MASK')
        network_address = Environment.get('NETWORK_ADDRESS')

        subnet_mask_bytes = subnet_mask.split('.')
        network_address_bytes = network_address.split('.')

        hosts = list()
        for last_subnet_mask_byte in range(
            255 - int(subnet_mask_bytes[-1]) + 1
        ):
            hosts.append(
                f"{network_address_bytes[0]}"
                + f".{network_address_bytes[1]}"
                + f".{network_address_bytes[2]}"
                + f".{last_subnet_mask_byte}"
            )

        hosts.append("127.0.0.1")

        return hosts

    @classmethod
    def _connection_handler(cls, host):
        url = f"http://{host}:{Environment.get('DEVICE_PORT')}{cls._registration_url}"
        print(url)
        try:
            response = requests.post(
                url=url,
                json={
                    # 'address': Environment.get('MASTER_IP'),
                    'port': Environment.get('EXTERNAL_PORT')
                },
                timeout=0.1  # TODO: make configurable
            )
            response.raise_for_status()
            json_response = response.json()
        except Exception:
            print("ERROR:", url)
            return None
        else:
            if (
                'device_id' not in json_response
                or response.status_code != status.HTTP_202_ACCEPTED
            ):
                return None
            else:
                return Device(json_response['device_id'], host)

    @classmethod
    def connect_devices(cls):
        with ThreadPoolExecutor() as executor:
            futures = list()
            subnet_hosts = cls._subnet_hosts()
            for host in subnet_hosts:
                print(host)
                futures.append(
                    executor.submit(
                        cls._connection_handler,
                        host=host
                    )
                )

        for future in as_completed(futures):
            device = future.result()
            if (
                device is not None
                and device.device_id not in cls._devices.keys()
            ):
                cls._devices[device.device_id] = device

    @classmethod
    def disconnect_device(cls, device_id):
        if device_id in cls._devices.keys():
            raise InvalidDeviceId(device_id)

        device = cls._devices[device_id]
        url = (
            f"{device.host}:{Environment.get('DEVICE_PORT')}"
            + f"{cls._registration_url}"
        )
        try:
            response = requests.delete(url=url)
            response.raise_for_status()
        except requests.HTTPError:
            raise DisconnectFailed(device_id)
        else:
            if response.status_code != status.HTTP_200_OK:
                raise DisconnectFailed(device_id)
            else:
                del cls._devices[device_id]

    @classmethod
    def _get_device(cls, device_id):
        try:
            return cls._devices[device_id]
        except KeyError:
            raise InvalidDeviceId(device_id)

    @classmethod
    def get_config(cls, category, key, device_id):
        device = cls._get_device(device_id)
        return device.get_config(category, key)

    @classmethod
    def set_config(cls, entries, device_id):
        device = cls._get_device(device_id)
        device.set_config(entries)

    @classmethod
    def set_config_all(cls, entries):
        for device in cls._devices.values():
            device.set_config(entries)

    @classmethod
    def get_environment(cls, key, device_id):
        device = cls._get_device(device_id)
        return device.get_environment(key)

    @classmethod
    def set_program_all(cls, commands):
        for device in cls._devices.values():
            device.set_program(commands)

    @classmethod
    def delete_program_all(cls):
        for device in cls._devices.values():
            device.delete_program()

    @classmethod
    def run_program_all(cls):
        for device in cls._devices.values():
            device.run_program()

    @classmethod
    def pause_program_all(cls):
        for device in cls._devices.values():
            device.pause_program()

    @classmethod
    def continue_program_all(cls):
        for device in cls._devices.values():
            device.continue_program()

    @classmethod
    def stop_program_all(cls):
        for device in cls._devices.values():
            device.stop_program()

    @classmethod
    def schedule_program_all(cls, schedule_time):
        for device in cls._devices.values():
            device.schedule_program(schedule_time)

    @classmethod
    def unschedule_program_all(cls):
        for device in cls._devices.values():
            device.unschedule_program()

    @classmethod
    def fire(cls, address, device_id):
        device = cls._get_device(device_id)
        device.fire(address)

    @classmethod
    def testloop(cls, device_id):
        device = cls._get_device(device_id)
        device.testloop()

    @classmethod
    def testloop_all(cls):
        for device in cls._devices.values():
            device.testloop()

    @classmethod
    def lock(cls, device_id):
        device = cls._get_device(device_id)
        device.lock()

    @classmethod
    def unlock(cls, device_id):
        device = cls._get_device(device_id)
        device.unlock()

    @classmethod
    def lock_all(cls):
        for device in cls._devices.values():
            device.lock()

    @classmethod
    def unlock_all(cls):
        for device in cls._devices.values():
            device.unlock()

    @classmethod
    def get_errors(cls, device_id):
        device = cls._get_device(device_id)
        return device.get_errors()

    @classmethod
    def delete_errors(cls, device_id):
        device = cls._get_device(device_id)
        device.delete_errors()

    @classmethod
    def get_logs(cls, device_id):
        device = cls._get_device(device_id)
        device.get_logs()

    @classmethod
    def get_lock_state(cls, device_id):
        device = cls._get_device(device_id)
        return device.is_locked

    @classmethod
    def get_program_state_all(cls):
        states_dict = dict()
        for device in cls._devices.values():
            states_dict[device.device_id] = device.program_state
        return states_dict

    @classmethod
    def get_fuses(cls, device_id):
        device = cls._get_device(device_id)
        return device.fuses

    @classmethod
    def heartbeat(cls, device_id):
        device = cls._get_device(device_id)
        device.heartbeat()

    @classmethod
    def notification(cls, data, device_id):
        device = cls._get_device(device_id)
        device.notification(data)

    @classmethod
    def get_host(cls, device_id):
        device = cls._get_device(device_id)
        return device.host

    @classmethod
    def get_devices(cls):
        return cls._devices

    @classmethod
    def set_system_time_all(cls, year, month, day, hour, minute, second, millisecond):
        for device in cls._devices.values():
            device.set_system_time(
                year, month, day, hour, minute, second, millisecond
            )
