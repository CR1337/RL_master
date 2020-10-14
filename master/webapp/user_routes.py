from itertools import count

from flask import (Blueprint, Response, redirect,
                   url_for, render_template, request)

from ..core.event_queue import EventQueue
from ..util.sys_time import set_system_time

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


@user_bp.route("/system-time", methods=["GET", "POST"])
def route_system_time():
    if request.method == "GET":
        return datetime.datetime.now().isoformat()
    elif request.method == "POST":
        data = request.get_json(force=True)
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
