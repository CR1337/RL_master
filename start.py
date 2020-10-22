from master import app
from flask import redirect, url_for
import os
from master.core.config import Config

debug = True


@app.route("/", methods=["GET"])
def route_index():
    return redirect(url_for('user_blueprint.route_index'))


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    if debug:
        app.run(
            use_debugger=True,
            use_reloader=True,
            passthrough_errors=True,
            port=Config.get('connection', 'internal_port'),
            host="0.0.0.0"
        )
    else:
        app.run(
            port=Config.get('connection', 'internal_port'),
            host="0.0.0.0"
        )
