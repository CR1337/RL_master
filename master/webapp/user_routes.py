from itertools import count
import json

from flask import (Blueprint, Response, redirect,
                   url_for, render_template)

from ..core.event_queue import EventQueue
from ..webapp import handle_exceptions
from ..core.heartbeat_controller import HeartbeatController

user_bp = Blueprint('user_blueprint', __name__)


@user_bp.route('/', methods=['GET'])
@handle_exceptions
def route_index():
    return redirect(url_for('user_blueprint.route_cockpit'))


@user_bp.route('/cockpit', methods=['GET'])
@handle_exceptions
def route_cockpit():
    return render_template('cockpit.html')


@user_bp.route('/settings', methods=['GET'])
@handle_exceptions
def route_settings():
    render_template('settings.html')


@user_bp.route("/event-stream", methods=["GET"])
@handle_exceptions
def route_event_stream():
    def event_stream():
        for i in count(start=0):
            event = EventQueue.pop_event()
            data = {
                'count': i,
                'type': event.event_type,
                'data': event.data
            }
            yield f"data: {json.dumps(data)}\n\n"
    return Response(event_stream(), mimetype="text/event-stream")


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
