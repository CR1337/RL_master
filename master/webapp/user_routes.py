from itertools import count

from flask import (Blueprint, Response, redirect,
                   url_for, render_template)

from ..core.event_queue import EventQueue

user_bp = Blueprint('user_blueprint', __name__)


@user_bp.route('/', methods=['GET'])
def route_index():
    return redirect(url_for('user_blueprint.route_cockpit'))


@user_bp.route('/cockpit', methods=['GET'])
def route_cockpit():
    return render_template('cockpit.html')


@user_bp.route('/settings', methods=['GET'])
def route_settings():
    render_template('settings.html')


@user_bp.route("/event-stream", methods=["GET"])
def route_event_stream():
    def event_stream():
        for i in count(start=0):
            event = EventQueue.pop_event()
            yield f"id:{i}\nevent:{event.event_type}\ndata:{event.data}\n\n"
    return Response(event_stream(), mimetype="text/event-stream")


@user_bp.route("/logs", methods=["GET"])
def route_logs():
    pass
