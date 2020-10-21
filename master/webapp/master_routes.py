from flask import Blueprint, request, make_response
from ..core.device_controller import DeviceController

master_bp = Blueprint('master_blueprint', __name__)


@master_bp.route("/notification", methods=['POST'])
def route_notification():
    device_id = request.get_json(force=True)['device_id']
    data = request.form['data']
    DeviceController.notification(data, device_id)
    return make_response(dict())


@master_bp.route("/heartbeat", methods=['POST'])
def route_heartbeat():
    device_id = request.get_json(force=True)['device_id']
    DeviceController.heartbeat(device_id)
    return make_response(dict())


@master_bp.route("/connect-devices", methods=['POST'])
def route_connect_devices():
    DeviceController.connect_devices()
    devices = list(DeviceController.get_devices().keys())
    return make_response({'devcies': devices})
