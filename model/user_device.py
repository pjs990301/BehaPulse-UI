from flask_restx import fields

user_device_model = {
    'userId': fields.String(required=True, description='User ID'),
    'macAddress': fields.String(required=True, description='Mac Address'),
}
