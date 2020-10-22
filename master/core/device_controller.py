from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from flask_api import status

from .device import Device
from .config import Config


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

    @classmethod
    def _subnet_hosts(cls):
        # TODO: This is a QAD-Fix!:
        subnet_mask = Config.get("connection", 'subnet_mask')
        network_address = Config.get("connection", 'network_address')

        subnet_mask_bytes = subnet_mask.split('.')
        network_address_bytes = network_address.split('.')

        hosts = list()
        for last_subnet_mask_byte in range(
            255 - int(subnet_mask_bytes[-1]) + 1
        ):
            if last_subnet_mask_byte == 255:
                continue
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
        device = Device(host)
        return device.connect()

    @classmethod
    def connect_devices(cls):
        with ThreadPoolExecutor() as executor:
            futures = list()
            subnet_hosts = cls._subnet_hosts()
            for host in subnet_hosts:
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

    # @classmethod
    # def disconnect_device(cls, device_id):
    #     if device_id in cls._devices.keys():
    #         raise InvalidDeviceId(device_id)

    #     device = cls._devices[device_id]
    #     url = (
    #         f"{device.host}:{Config.get('connection', 'device_port')}"
    #         + f"{cls._registration_url}"
    #     )
    #     try:
    #         response = requests.delete(url=url)
    #         response.raise_for_status()
    #     except requests.HTTPError:
    #         raise DisconnectFailed(device_id)
    #     else:
    #         if response.status_code != status.HTTP_200_OK:
    #             raise DisconnectFailed(device_id)
    #         else:
    #             del cls._devices[device_id]

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
        return device.set_config(entries)

    @classmethod
    def set_config_all(cls, entries):
        responses = dict()
        for device in cls._devices.values():
            responses[device.device_id] = device.set_config(entries)
        return responses

    @classmethod
    def set_program_all(cls, commands):
        responses = dict()
        for device in cls._devices.values():
            responses[device.device_id] = device.set_program(commands)
        return responses

    @classmethod
    def delete_program_all(cls):
        responses = dict()
        for device in cls._devices.values():
            responses[device.device_id] = device.delete_program()
        return responses

    @classmethod
    def run_program_all(cls):
        responses = dict()
        for device in cls._devices.values():
            responses[device.device_id] = device.run_program()
        return responses

    @classmethod
    def pause_program_all(cls):
        responses = dict()
        for device in cls._devices.values():
            responses[device.device_id] = device.pause_program()
        return responses

    @classmethod
    def continue_program_all(cls):
        responses = dict()
        for device in cls._devices.values():
            responses[device.device_id] = device.continue_program()
        return responses

    @classmethod
    def stop_program_all(cls):
        responses = dict()
        for device in cls._devices.values():
            responses[device.device_id] = device.stop_program()
        return responses

    @classmethod
    def schedule_program_all(cls, schedule_time):
        responses = dict()
        for device in cls._devices.values():
            responses[device.device_id] = device.schedule_program(schedule_time)
        return responses

    @classmethod
    def unschedule_program_all(cls):
        responses = dict()
        for device in cls._devices.values():
            responses[device.device_id] = device.unschedule_program()
        return responses

    @classmethod
    def fire(cls, address, device_id):
        device = cls._get_device(device_id)
        return device.fire(address)

    @classmethod
    def testloop(cls, device_id):
        device = cls._get_device(device_id)
        return device.testloop()

    @classmethod
    def testloop_all(cls):
        responses = dict()
        for device in cls._devices.values():
            responses[device.device_id] = device.testloop()
        return responses

    @classmethod
    def lock(cls, device_id):
        device = cls._get_device(device_id)
        return device.lock()

    @classmethod
    def unlock(cls, device_id):
        device = cls._get_device(device_id)
        return device.unlock()

    @classmethod
    def lock_all(cls):
        responses = dict()
        for device in cls._devices.values():
            responses[device.device_id] = device.lock()
        return responses

    @classmethod
    def unlock_all(cls):
        responses = dict()
        for device in cls._devices.values():
            responses[device.device_id] = device.unlock()
        return responses
    @classmethod
    def get_errors(cls, device_id):
        device = cls._get_device(device_id)
        return device.get_errors()

    @classmethod
    def delete_errors(cls, device_id):
        device = cls._get_device(device_id)
        return device.delete_errors()

    @classmethod
    def get_logs(cls):
        # TODO
        device = cls._get_device(device_id)
        device.get_logs()

    @classmethod
    def get_lock_states_all(cls):
        states = dict()
        for device in cls._devices.values():
            states[device.device_id] = device.is_locked
        return states

    @classmethod
    def get_program_state_all(cls):
        states_dict = dict()
        for device in cls._devices.values():
            states_dict[device.device_id] = device.program_state
        return states_dict

    @classmethod
    def get_fuses_all(cls):
        fuses = dict()
        for device in cls._devices.values():
            fuses[device.device_id] = device.fuses
        return fuses

    @classmethod
    def heartbeat(cls, device_id):
        device = cls._get_device(device_id)
        return device.heartbeat()

    @classmethod
    def notification(cls, data, device_id):
        device = cls._get_device(device_id)
        return device.notification(data)

    @classmethod
    def get_host(cls, device_id):
        device = cls._get_device(device_id)
        return device.host

    @classmethod
    def get_devices(cls):
        return cls._devices

    @classmethod
    def set_system_time_all(
        cls,
        year, month, day,
        hour, minute, second, millisecond
    ):
        responses = dict()
        for device in cls._devices.values():
            responses[device.device_id] = device.set_system_time(
                year, month, day, hour, minute, second, millisecond
            )
        return responses

    @classmethod
    def get_systems_times_all(cls):
        times = dict()
        for device in cls._devices.values():
            times[device.device_id] = device.get_system_time()
        return times
