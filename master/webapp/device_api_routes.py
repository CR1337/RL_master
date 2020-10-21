from flask import Blueprint, request, redirect, make_response
from datetime import datetime
from ..core.device_controller import DeviceController
from ..util.sys_time import set_system_time

import json

device_api_bp = Blueprint('device_api_blueprint', __name__)


@device_api_bp.route('/<device_id>/config', methods=['GET', 'POST'])
def route_config(device_id):
    if request.method == 'GET':
        return DeviceController.get_config(
            category=request.args['category'],
            key=request.args['key'],
            device_id=device_id
        )
    elif request.method == 'POST':
        DeviceController.set_config(
            entries=request.args['entries'],
            device_id=device_id
        )
        return make_response(dict())


@device_api_bp.route('/program', methods=['POST', 'DELETE'])
def route_program():
    if request.method == 'POST':
        action = request.form['action']
        if action == 'post':
            file = request.files['program_file']
            commands = json.load(file)
            DeviceController.set_program_all(commands)
        elif action == 'delete':
            DeviceController.delete_program_all()
        return make_response(dict())
    elif request.method == 'DELETE':
        DeviceController.delete_program_all()
        return make_response(dict())


@device_api_bp.route('/program/control', methods=['POST'])
def route_program_control():
    action = request.form['action']
    if action == 'run':
        DeviceController.run_program_all()
    elif action == 'pause':
        DeviceController.pause_program_all()
    elif action == 'continue':
        DeviceController.continue_program_all()
    elif action == 'stop':
        DeviceController.stop_program_all()
    elif action == 'schedule':
        DeviceController.schedule_program_all(request.form['schedule_time'])
    elif action == 'unschedule':
        DeviceController.unschedule_program_all()
    else:
        # TODO: Error
        pass

    return make_response(dict())


@device_api_bp.route('/program/state', methods=['GET'])
def route_program_state():
    return DeviceController.get_program_state_all()


@device_api_bp.route('/<device_id>/fire', methods=['POST'])
def route_fire(device_id):
    DeviceController.fire(request.form['address'], device_id)
    return make_response(dict())


@device_api_bp.route('/fuses', methods=['GET'])
def route_fuses():
    return DeviceController.get_fuses_all()


@device_api_bp.route('/<device_id>/testloop', methods=['POST'])
def route_testloop(device_id):
    DeviceController.testloop(device_id)
    return make_response(dict())


@device_api_bp.route('/testloop', methods=['POST'])
def route_testloop_all():
    DeviceController.testloop_all()
    return make_response(dict())


@device_api_bp.route('/lock-all', methods=['GET', 'POST'])
def route_lock_all():
    # DeviceController.lock_all()
    if request.method == 'GET':
        return DeviceController.get_lock_states_all()
    elif request.method == 'POST':
        action = request.form['action']
        if action == 'lock':
            DeviceController.lock_all()
        elif action == 'unlock':
            DeviceController.unlock_all()
        else:
            ...
    return make_response(dict())


@device_api_bp.route('/<device_id>/errors', methods=['GET', 'DELETE'])
def route_error(device_id):
    if request.method == 'GET':
        return DeviceController.get_errors(device_id)
    elif request.method == 'DELETE':
        DeviceController.delete_errors(device_id)
        return make_response(dict())


@device_api_bp.route('/<device_id>/logs', methods=['GET'])
def route_logs(device_id):
    host = DeviceController.get_host(device_id)
    return redirect(f"http://{host}/logs")


@device_api_bp.route("/system-time", methods=["GET", "POST"])
def route_system_time():
    if request.method == "GET":
        times = DeviceController.get_systems_times_all()
        times.update({
            "master": {"system_time": datetime.now().isoformat()}
        })
        return times
    elif request.method == "POST":
        data = request.form
        year = int(data['year']) if 'year' in data else 0
        month = int(data['month']) if 'month' in data else 0
        day = int(data['day']) if 'day' in data else 0
        hour = int(data['hour']) if 'hour' in data else 0
        minute = int(data['minute']) if 'minute' in data else 0
        second = int(data['second']) if 'second' in data else 0
        millisecond = int(data['millisecond']) if 'millisecond' in data else 0
        set_system_time(
            year, month, day, hour, minute, second, millisecond
        )
        DeviceController.set_system_time_all(
            year, month, day, hour, minute, second, millisecond
        )
        return make_response(dict())
