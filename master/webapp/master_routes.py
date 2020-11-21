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
    data = request.get_json(force=True)
    DeviceController.heartbeat(data)
    return make_response(dict())


@master_bp.route("/connect-devices", methods=['POST'])
@handle_exceptions
def route_connect_devices():
    DeviceController.connect_devices()
    # devices = list(DeviceController.get_devices().keys())
    devices = [
        {'device_id': device.device_id, 'n_chips': device.n_chips}
        for device in DeviceController.get_devices().values()
    ]
    return make_response({'devices': devices})


@master_bp.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
