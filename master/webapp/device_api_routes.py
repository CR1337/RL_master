from flask import Blueprint, request
from datetime import datetime
from ..core.device_controller import DeviceController
from ..util.sys_time import set_system_time
from ..webapp import handle_exceptions, InvalidRequest

import json

device_api_bp = Blueprint('device_api_blueprint', __name__)


@device_api_bp.route('/program', methods=['POST', 'DELETE'])
@handle_exceptions
def route_program():
    if request.method == 'POST':
        print(request.form)
        commands = json.loads(request.form['commands'])
        print(commands)
        program_name = request.form['program_name']
        print(program_name)
        return DeviceController.set_program_all(commands, program_name)
    elif request.method == 'DELETE':
        return DeviceController.delete_program_all()


@device_api_bp.route('/program/control', methods=['POST'])
@handle_exceptions
def route_program_control():
    action = request.form['action']
    if action == 'run':
        return DeviceController.run_program_all()
    elif action == 'pause':
        return DeviceController.pause_program_all()
    elif action == 'continue':
        return DeviceController.continue_program_all()
    elif action == 'stop':
        return DeviceController.stop_program_all()
    elif action == 'schedule':
        return DeviceController.schedule_program_all(
            request.form['time']
        )
    elif action == 'unschedule':
        return DeviceController.unschedule_program_all()
    else:
        raise InvalidRequest


@device_api_bp.route('/<device_id>/fire', methods=['POST'])
@handle_exceptions
def route_fire(device_id):
    return DeviceController.fire(request.form['address'], device_id)


@device_api_bp.route('/<device_id>/testloop', methods=['POST'])
@handle_exceptions
def route_testloop(device_id):
    return DeviceController.testloop(device_id)


@device_api_bp.route('/testloop', methods=['POST'])
@handle_exceptions
def route_testloop_all():
    return DeviceController.testloop_all()


@device_api_bp.route('/lock-all', methods=['GET', 'POST'])
@handle_exceptions
def route_lock_all():
    if request.method == 'GET':
        return DeviceController.get_lock_states_all()
    elif request.method == 'POST':
        action = request.form['action']
        if action == 'lock':
            return DeviceController.lock_all()
        elif action == 'unlock':
            return DeviceController.unlock_all()
        else:
            raise InvalidRequest()


@device_api_bp.route("/system-time", methods=["GET", "POST"])
@handle_exceptions
def route_system_time():
    if request.method == "GET":
        times = DeviceController.get_systems_times_all()
        times.update({
            "master": {"system_time": datetime.now().isoformat()}
        })
        return times
    elif request.method == "POST":
        time = request.form['time']
        set_system_time(time)
        return DeviceController.set_system_time_all(time)


@device_api_bp.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
