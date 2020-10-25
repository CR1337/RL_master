from flask import Blueprint, request, make_response
from ..core.device_controller import DeviceController
from ..webapp import handle_exceptions

master_bp = Blueprint('master_blueprint', __name__)


@master_bp.route("/notification", methods=['POST'])
@handle_exceptions
def route_notification():
    data = request.get_json(force=True)
    DeviceController.notification(data)
    return make_response(dict())


@master_bp.route("/heartbeat", methods=['POST'])
@handle_exceptions
def route_heartbeat():
    device_id = request.get_json(force=True)['device_id']
    DeviceController.heartbeat(device_id)
    return make_response(dict())


@master_bp.route("/connect-devices", methods=['POST'])
@handle_exceptions
def route_connect_devices():
    DeviceController.connect_devices()
    devices = list(DeviceController.get_devices().keys())
    return make_response({'devcies': devices})
