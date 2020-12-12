from concurrent.futures import ThreadPoolExecutor, as_completed

from .device import Device
from ..util import network
from .event import Event
from .event_queue import EventQueue


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
        network_address_bytes = network.get_network_address().split('.')
        hosts = list()
        hosts.append("127.0.0.1")
        for last_byte in range(1, 255):
            hosts.append(
                ".".join(network_address_bytes[0:3] + [str(last_byte)])
            )
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
    def set_program_all(cls, commands, program_name):
        responses = dict()
        for device in cls._devices.values():
            responses[device.device_id] = device.set_program(
                commands, program_name
            )
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
            responses[device.device_id] = device.schedule_program(
                schedule_time
            )
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
    def heartbeat(cls, data):
        # event = Event('device_heartbeat', {'device_id': device_id, 'time': time})
        # EventQueue.push_event(event)
        device = cls._get_device(data['device_id'])
        return device.heartbeat(data)

    @classmethod
    def notification(cls, data):
        event = Event(data['type'], data)
        EventQueue.push_event(event)

    @classmethod
    def get_host(cls, device_id):
        device = cls._get_device(device_id)
        return device.host

    @classmethod
    def get_devices(cls):
        return cls._devices

    @classmethod
    def set_system_time_all(cls, time):
        responses = dict()
        for device in cls._devices.values():
            responses[device.device_id] = device.set_system_time(
                time
            )
        return responses

    @classmethod
    def get_systems_times_all(cls):
        times = dict()
        for device in cls._devices.values():
            times[device.device_id] = device.get_system_time()
        return times
