from flask import request, Response, json, Blueprint

health_checks = Blueprint("health_checks", __name__)

@health_checks.get('/')
def check_health():
    return Response(
        response=json.dumps({'status': "OK"}),
        status=200,
        mimetype='application/json'
    )

