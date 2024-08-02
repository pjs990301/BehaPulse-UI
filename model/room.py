from flask_restx import fields

room_model = {
    'roomId': fields.Integer(required=True, description='Room ID'),
}
