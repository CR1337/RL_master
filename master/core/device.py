import time

import requests

from .config import Config


class Device():
    _registration_url = "/master-registration"

    def __init__(self, host):
        self._host = host
        self._last_heartbeat = None

        self._system_time = None
        self._locked = None
        self._program_state = None
        self._scheduled_time = None
        self._program_name = None
        self._fuse_states = None
        self._error_states = None

    def _request(self, url, method='GET', data=None):
        assert method in ['GET', 'POST', 'DELETE']
        url = f"http://{self._host}:" \
            f"{Config.get('connection', 'device_port')}{url}"
        data = dict() if data is None and method != 'GET' else data
        timeout = Config.get('timeouts', 'device_request')

        try:
            if method == 'GET':
                response = requests.get(
                    url, params=data, timeout=timeout).json()
            elif method == 'POST':
                response = requests.post(
                    url, json=data, timeout=timeout).json()
            elif method == 'DELETE':
                response = requests.delete(
                    url, json=data, timeout=timeout).json()
        except requests.Timeout:
            response = {'error': f"timeout after {timeout} sec."}
        except Exception:
            response = {'error': "unknown connection error."}

        return response

    def connect(self):
        print(self._host)
        response = self._request(
            url=Device._registration_url,
            method='POST',
            data={'port': Config.get('connection', 'external_port')}
        )

        if 'error' in response.keys() or 'device_id' not in response.keys():
            return None
        else:
            self._device_id = response['device_id']
            self._n_chips = response['n_chips']
            return self

    def disconnect(self):
        return self._request(
            url="/disconnect",
            method='POST'
        )

    def set_program(self, commands, program_name):
        return self._request(
            url="/program",
            method="POST",
            data={
                'commands': commands,
                'program_name': program_name
            }
        )

    def delete_program(self):
        return self._request(
            url="/program",
            method="DELETE"
        )

    def run_program(self):
        return self._request(
            url="/program/control",
            method='POST',
            data={
                'action': 'run'
            }

        )

    def pause_program(self):
        return self._request(
            url="/program/control",
            method='POST',
            data={
                'action': 'pause'
            }

        )

    def continue_program(self):
        return self._request(
            url="/program/control",
            method='POST',
            data={
                'action': 'continue'
            }

        )

    def stop_program(self):
        return self._request(
            url="/program/control",
            method='POST',
            data={
                'action': 'stop'
            }
        )

    def schedule_program(self, schedule_time):
        return self._request(
            url="/program/control",
            method='POST',
            data={
                'action': 'schedule',
                'time': schedule_time
            }
        )

    def unschedule_program(self):
        return self._request(
            url="/program/control",
            method='POST',
            data={
                'action': 'unschedule'
            }
        )

    def fire(self, address):
        return self._request(
            url="/fire",
            method="POST",
            data={
                'address': address
            }
        )

    def testloop(self):
        return self._request(
            url="/testloop",
            method="POST"
        )

    def lock(self):
        return self._request(
            url="/lock",
            method='POST',
            data={
                'action': 'lock'
            }
        )

    def unlock(self):
        return self._request(
            url="/lock",
            method='POST',
            data={
                'action': 'unlock'
            }
        )

    def get_errors(self):
        return self._request(
            url="/errors",
        )

    def delete_errors(self):
        return self._request(
            url="/errors",
            method='DELETE'
        )

    def set_system_time(
        self, time
    ):
        return self._request(
            url="/system-time",
            method="POST",
            data={
                'time': time
            }
        )

    def get_system_time(self):
        return self._request(
            url="/system-time"
        )

    def get_fuses(self):
        return self._request(
            url="/fuses"
        )

    def heartbeat(self, data):
        self._last_heartbeat = time.time()

        self._system_time = data['system_time']
        self._locked = data['locked']
        self._program_state = data['program_state']
        self._scheduled_time = data['scheduled_time']
        self._program_name = data['program_name']
        self._fuse_states = data['fuse_states']
        self._error_states = data['error_states']

    @property
    def system_time(self):
        return self._system_time

    @property
    def is_locked(self):
        return self._locked

    @property
    def program_state(self):
        return self._program_state

    @property
    def host(self):
        return self._host

    @property
    def last_heartbeat(self):
        return self._last_heartbeat

    @property
    def device_id(self):
        return self._device_id

    @property
    def n_chips(self):
        return self._n_chips

    @property
    def scheduled_time(self):
        return self._scheduled_time

    @property
    def program_name(self):
        return self._program_name

    @property
    def fuse_states(self):
        return self._fuse_states

    @property
    def error_states(self):
        return self._error_states
