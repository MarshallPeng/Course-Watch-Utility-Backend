from flask import Flask, request
import json

from src.controller.WatchController import WatchController

app = Flask(__name__)


@app.route('/api/new_request', methods=['POST', 'OPTIONS'])
def add_new_request():
    controller = WatchController()
    data = json.loads(request.data)
    result = controller.new_request(data)
    return result


@app.route('/api/check_courses')
def check_courses():
    controller = WatchController()
    result = controller.check_courses()
    return result


@app.route('/api/current_requests', methods=['POST', 'OPTIONS'])
def current_courses():
    data = json.loads(request.data)
    controller = WatchController()
    result = controller.get_current_requests(data)
    return result


@app.route('/api/reset_courses')
def reset_courses():
    controller = WatchController()
    result = controller.reset_requests()
    return result


if __name__ == '__main__':
    app.run(debug=True)
