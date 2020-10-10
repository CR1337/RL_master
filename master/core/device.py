import requests
import time
from flask_api import status
from .environment import Environment


class DeviceError(Exception):
    pass


class ApiException(DeviceError):
    def __init__(self, exception_type, exception_args):
        self.exception_type = exception_type
        self.exception_args = exception_args


class UnauthorizedError(DeviceError):
    pass


class UnknownApiError(DeviceError):
    pass


class Device():

    def __init__(self, device_id, host):
        self._device_id = device_id
        self._host = host
        self._last_heartbeat = None

    def _request(self, url, args=None, params={}, method='GET'):
        url = f"http://{self._host}:{Environment.get('DEVICE_PORT')}" + url

        if method == 'GET':
            response = requests.get(url, args=args)
        elif method == 'POST':
            response = requests.post(url, json=params)
        elif method == 'DELETE':
            response = requests.delete(url, json=params)

        if response.status_code == status.HTTP_400_BAD_REQUEST:
            json_data = response.json()
            if 'exception_type' in json_data and 'exception_args' in json_data:
                raise ApiException(
                    json_data['exception_type'], json_data['exception_args']
                )
            else:
                raise UnknownApiError()
        elif response.status_code == status.HTTP_401_UNAUTHORIZED:
            raise UnauthorizedError()
        elif response.status_code >= status.HTTP_400_BAD_REQUEST:
            raise UnknownApiError()
        else:
            return response

    def _simple_request(self, url, args=None, params={}, method='GET'):
        self._request(url, args, params, method)

    def _json_request(self, url, args=None, params=None, method='GET'):
        response = self._request(url, args, params, method)
        return response.json()

    def get_config(self, category, key):
        return self._json_request(
            url="/config",
            args={
                'category': category,
                'key': key
            }
        )

    def set_config(self, entries):
        self._simple_request(
            url="/config",
            params={
                "entries": entries
            },
            method="POST"
        )

    def get_environment(self, key):
        return self._json_request(
            url="/environment",
            args={
                "key": key
            }
        )

    def set_program(self, commands):
        self._simple_request(
            url="/program",
            params={
                'commands': commands
            },
            method='POST'
        )

    def delete_program(self):
        self._simple_request(
            url="/program",
            method="DELETE"
        )

    def run_program(self):
        self._simple_request(
            url="/program/control",
            params={
                'action': 'run'
            },
            method='POST'
        )

    def pause_program(self):
        self._simple_request(
            url="/program/control",
            params={
                'action': 'pause'
            },
            method='POST'
        )

    def continue_program(self):
        self._simple_request(
            url="/program/control",
            params={
                'action': 'continue'
            },
            method='POST'
        )

    def stop_program(self):
        self._simple_request(
            url="/program/control",
            params={
                'action': 'stop'
            },
            method='POST'
        )

    def schedule_program(self, schedule_time):
        self._simple_request(
            url="/program/control",
            params={
                'action': 'schedule',
                'schedule_time': schedule_time
            },
            method='POST'
        )

    def unschedule_program(self):
        self._simple_request(
            url="/program/control",
            params={
                'action': 'unschedule'
            },
            method='POST'
        )

    def fire(self, address):
        self._simple_request(
            url="/fire",
            params={
                'address': address
            },
            method="POST"
        )

    def testloop(self):
        self._simple_request(
            url="/testloop",
            method="POST"
        )

    def lock(self):
        self._simple_request(
            url="/lock",
            params={
                'action': 'lock'
            },
            method='POST'
        )

    def unlock(self):
        self._simple_request(
            url="/lock",
            params={
                'action': 'unlock'
            },
            method='POST'
        )

    def get_errors(self):
        return self._json_request(
            url="/errors"
        )

    def delete_errors(self):
        self._simple_request(
            url="/errors",
            method='DELETE'
        )

    def get_logs(self, amount):
        # TODO
        return self._json_request(
            url="/logs",
            args={
                'amount': amount
            }
        )

    def heartbeat(self):
        self._last_heartbeat = time.time()

    def notification(self, data):
        pass
        # TODO

    @property
    def is_locked(self):
        return self._json_request(
            url="/lock",
        )['locked']

    @property
    def program_state(self):
        return self._json_request(
            url="/program/state",
        )['state']

    @property
    def fuses(self):
        return self._json_request(
            url="/fuses"
        )

    @property
    def host(self):
        return self._host

    @property
    def last_heartbeat(self):
        return self._last_heartbeat

    @property
    def device_id(self):
        return self._device_id
