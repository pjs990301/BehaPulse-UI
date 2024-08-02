from flask_restx import fields

device_model = {
    # 'deviceId': fields.Integer(required=True, description='Device ID'),
    'macAddress': fields.String(required=True, description='Mac Address'),
}
