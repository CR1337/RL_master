from flask import Blueprint, Response, redirect, render_template, url_for

from ..core.heartbeat_controller import HeartbeatController
from ..webapp import handle_exceptions

user_bp = Blueprint('user_blueprint', __name__)


@user_bp.route('/', methods=['GET'])
@handle_exceptions
def route_index():
    return redirect(url_for('user_blueprint.route_cockpit'))


@user_bp.route('/cockpit', methods=['GET'])
@handle_exceptions
def route_cockpit():
    return render_template('cockpit.html')


@user_bp.route("/heartbeat-stream", methods=["GET"])
@handle_exceptions
def route_heartbeat_stream():
    heartbeat_controller = HeartbeatController()
    return Response(
        heartbeat_controller.heartbeat_stream(),
        mimetype="text/event-stream"
    )


@user_bp.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
