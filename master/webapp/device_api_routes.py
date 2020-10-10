from flask import Blueprint, request, redirect
from ..core.device_controller import DeviceController

import json

device_api_bp = Blueprint('device_api_blueprint', __name__)


@device_api_bp.route('/<device>/config', methods=['GET', 'POST'])
def route_config(device='all'):
    if request.method == 'GET':
        return DeviceController.get_config(
            category=request.args['category'],
            key=request.args['key'],
            device_id=request.args['device_id']
        )
    elif request.method == 'POST':
        if 'device_id' in request.args:
            DeviceController.set_config(
                entries=request.args['entries'],
                device_id=request.args['device_id']
            )
        else:
            DeviceController.set_config_all(
                entries=request.args['entries']
            )
        return ""


@device_api_bp.route('/<device>/environment', methods=['GET'])
def route_environment(device='all'):
    return DeviceController.get_environment(
            key=request.args['key'],
            device_id=request.args['device_id']
        )


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
        return ""
    elif request.method == 'DELETE':
        DeviceController.delete_program_all()
        return ""


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

    return ""


@device_api_bp.route('/program/state', methods=['GET'])
def route_program_state():
    return DeviceController.get_program_state_all()


@device_api_bp.route('/<device_id>/fire', methods=['POST'])
def route_fire(device_id):
    DeviceController.fire(request.form['address'], device_id)


@device_api_bp.route('/<device_id>/fuses', methods=['GET'])
def route_fuses(device_id):
    return DeviceController.get_fuses(device_id)


@device_api_bp.route('/<device_id>/testloop', methods=['POST'])
def route_testloop(device_id):
    DeviceController.testloop(device_id)


@device_api_bp.route('/testloop-all', methods=['POST'])
def route_testloop_all():
    DeviceController.testloop_all()
    return ""


@device_api_bp.route('/<device_id>/lock', methods=['GET', 'POST'])
def route_lock(device_id):
    if request.method == 'GET':
        return DeviceController.get_lock_state(device_id)
    elif request.method == 'POST':
        DeviceController.lock(device_id)


@device_api_bp.route('/<device_id>/unlock', methods=['POST'])
def route_unlock(device_id):
    DeviceController.unlock(device_id)


@device_api_bp.route('/lock-all', methods=['GET'])
def route_lock_all():
    DeviceController.lock_all()


@device_api_bp.route('/unlock-all', methods=['GET'])
def route_unlock_all():
    DeviceController.unlock_all()


@device_api_bp.route('/<device_id>/error', methods=['GET', 'DELETE'])
def route_error(device_id):
    if request.method == 'GET':
        return DeviceController.get_errors(device_id)
    elif request.method == 'DELETE':
        DeviceController.delete_errors(device_id)


@device_api_bp.route('/<device_id>/logs', methods=['GET'])
def route_logs(device_id):
    host = DeviceController.get_host(device_id)
    return redirect(f"http://{host}/logs")
