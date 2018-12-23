from flask import jsonify, Response
import json


class ResponseUtil:
    """
    Helper class to make building http responses a little easier.
    """

    def build_error_response(self, code, message):
        response = jsonify(
            {
                'status' : 'error',
                'code' : code,
                'message' : message
            }
        )
        response.status_code = code
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    def build_success_response(self, code, message, data):

        response = Response()
        response.data = json.dumps(
            {
                'status' : 'ok',
                'code' : code,
                'message': message,
                'result' : data,
            }
        )
        response.status_code = code
        response.headers['Access-Control-Allow-Origin'] = '*'


        return response