from flask_restx import fields

device_model = {
    # 'deviceId': fields.Integer(required=True, description='Device ID'),
    'macAddress': fields.String(required=True, description='Mac Address'),
    'type': fields.String(required=True, description='Device Type'),
    'install_location': fields.String(description='Install Location'),
    'room': fields.String(description='Room'),
    'check_date': fields.Date(description='Check Date'),
    'note': fields.String(description='Note'),
    'on_off': fields.String(description='On/Off'),
}
