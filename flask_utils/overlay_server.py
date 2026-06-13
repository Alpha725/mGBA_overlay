from flask import Flask, render_template
from flask_socketio import SocketIO
import os

class OverlayServer:
    def __init__(self, debug=False):
        self.app = Flask(__name__, template_folder=f"{os.path.abspath('./')}/flask_utils")
        self.socketio = SocketIO(self.app)
        self.debug = debug
        self._setup_routes()

    def _setup_routes(self):
        @self.app.route('/')
        def index():
            return render_template('index.html')

    def update_element(self, element_id, content):
        """Replaces your old global update_overlay() function."""
        self.socketio.emit('update_data', {'id': element_id, 'content': content})

    def start_background_task(self, background_function):
        """Schedules your data processing loop to run in the background."""
        self.socketio.start_background_task(background_function)

    def run(self, host='127.0.0.1', port=5000):
        """Starts the Flask server."""
        self.socketio.run(self.app, host=host, port=port, debug=self.debug)
