import requests
import time
from .config import Config


class Device():
    _registration_url = "/master-registration"

    def __init__(self, host):
        self._host = host
        self._last_heartbeat = None

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
            return self

    # TODO: maybe get_config_all and get_config_category?

    def get_config(self, category, key):
        return self._request(
            url="/config",
            data={
                'category': category,
                'key': key
            }
        )

    def set_config(self, entries):
        return self._request(
            url="/config",
            method="POST",
            data={
                'entries': entries
            }
        )

    def set_program(self, commands):
        return self._request(
            url="/program",
            method="POST",
            data={
                'commands': commands
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
                'schedule_time': schedule_time
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
        self,
        year, month, day,
        hour, minute, second, millisecond
    ):
        return self._request(
            url="/system-time",
            method="POST",
            data={
                'year': year,
                'month': month,
                'day': day,
                'hour': hour,
                'minute': minute,
                'second': second,
                'millisecond': millisecond
            }
        )

    def get_system_time(self):
        return self._request(
            url="/system-time"
        )

    def get_locked_state(self):
        return self._request(
            url="/lock"
        )

    def get_fuses(self):
        return self._request(
            url="/fuses"
        )

    def get_program_state(self):
        return self._request(
            url="/program/state",
        )

    def heartbeat(self):
        self._last_heartbeat = time.time()

    def notification(self, data):
        ...
        # TODO

    @property
    def is_locked(self):
        return self.get_locked_state()['locked']

    @property
    def program_state(self):
        return self.get_program_state()['state']

    @property
    def host(self):
        return self._host

    @property
    def last_heartbeat(self):
        return self._last_heartbeat

    @property
    def device_id(self):
        return self._device_id
