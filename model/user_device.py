from flask_restx import fields

user_device_model = {
    'userEmail': fields.String(required=True, description='User Email'),
    'macAddress': fields.String(required=True, description='Mac Address'),
}
