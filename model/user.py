from flask_restx import fields

user_model = {
    'userId': fields.String(required=True, description='User ID'),
    'userName': fields.String(required=True, description='User Name'),
    'Birth': fields.Date(required=True, description='Birth'),
}
