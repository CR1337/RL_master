import json
import time
from itertools import count

from ..util.sys_time import get_system_time
from .config import Config
from .device_controller import DeviceController


class HeartbeatController:

    def __init__(self):
        self._period = Config.get('timings', 'heartbeat_period')

    def heartbeat_stream(self):
        time.sleep(self._period)
        for i in count(start=0):
            data = {
                'system_time': get_system_time()
            }
            data['devices'] = dict()
            for device in DeviceController.get_devices().values():
                device_data = {
                    'system_time': device.system_time,
                    'locked': device.is_locked,
                    'program_state': device.program_state,
                    'scheduled_time': device.scheduled_time,
                    'program_name': device.program_name,
                    'fuse_states': device.fuse_states,
                    'error_states': device.error_states,
                    'last_heartbeat': device.last_heartbeat
                }
                data['devices'][device.device_id] = device_data
            yield f"data: {json.dumps(data)}\nid: {str(i)}\n\n"
            time.sleep(self._period)
