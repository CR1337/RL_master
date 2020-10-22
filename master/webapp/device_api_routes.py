from flask import Blueprint, request, make_response
from datetime import datetime
from ..core.device_controller import DeviceController
from ..util.sys_time import set_system_time
from ..webapp import handle_exceptions

import json

device_api_bp = Blueprint('device_api_blueprint', __name__)


@device_api_bp.route('/<device_id>/config', methods=['GET', 'POST'])
@handle_exceptions
def route_config(device_id):
    if request.method == 'GET':
        return DeviceController.get_config(
            category=request.args['category'],
            key=request.args['key'],
            device_id=device_id
        )
    elif request.method == 'POST':
        return DeviceController.set_config(
            entries=request.args['entries'],
            device_id=device_id
        )


@device_api_bp.route('/program', methods=['POST', 'DELETE'])
@handle_exceptions
def route_program():
    # TODO: make DELETE work from cockpit
    if request.method == 'POST':
        action = request.form['action']
        if action == 'post':
            file = request.files['program_file']
            commands = json.load(file)
            return DeviceController.set_program_all(commands)
        elif action == 'delete':
            return DeviceController.delete_program_all()
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
            request.form['schedule_time']
        )
    elif action == 'unschedule':
        return DeviceController.unschedule_program_all()
    else:
        # TODO: Error
        return make_response(dict())


@device_api_bp.route('/program/state', methods=['GET'])
@handle_exceptions
def route_program_state():
    return DeviceController.get_program_state_all()


@device_api_bp.route('/<device_id>/fire', methods=['POST'])
@handle_exceptions
def route_fire(device_id):
    return DeviceController.fire(request.form['address'], device_id)


@device_api_bp.route('/fuses', methods=['GET'])
@handle_exceptions
def route_fuses():
    return DeviceController.get_fuses_all()


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
            # TODO
            return make_response(dict())


@device_api_bp.route('/<device_id>/errors', methods=['GET', 'DELETE'])
@handle_exceptions
def route_error(device_id):
    if request.method == 'GET':
        return DeviceController.get_errors(device_id)
    elif request.method == 'DELETE':
        return DeviceController.delete_errors(device_id)


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
        data = request.form
        time_params = {
            'year': 0, 'month': 0, 'day': 0,
            'hour': 0, 'minute': 0, 'second': 0, 'millisecond': 0
        }
        for key in time_params.keys():
            try:
                time_params[key] = int(data[key])
            except (ValueError, KeyError):
                continue
        set_system_time(**time_params)
        return DeviceController.set_system_time_all(**time_params)
