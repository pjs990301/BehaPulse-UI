from flask_restx import fields

user_dashboard_device_model = {
    'userEmail': fields.String(required=True, description='User Email'),
    'deviceId': fields.Integer(required=True, description='Device ID'),
    'personId': fields.Integer(required=True, description='Person ID'),
}
