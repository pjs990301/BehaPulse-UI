from flask_restx import fields

user_room_model = {
    'userId': fields.String(required=True, description='User ID'),
    'roomId': fields.Integer(required=True, description='Room ID'),
}
