from itertools import count

from flask import (Blueprint, Response, redirect,
                   url_for, render_template)

from ..core.event_queue import EventQueue
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
            yield f"id:{i}\nevent:{event.event_type}\ndata:{event.data}\n\n"
    return Response(event_stream(), mimetype="text/event-stream")


import time


@user_bp.route("/stream-test", methods=["GET"])
def route_stream_test():

    def get_message():
        time.sleep(1)
        return time.ctime(time.time())

    def event_stream():
        while True:
            yield f"data: {get_message()}\n\n"

    return Response(event_stream(), mimetype="text/event-stream")
