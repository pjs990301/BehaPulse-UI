from flask_restx import fields

user_dashboard_model = {
    'userEmail': fields.String(required=True, description='User Email'),
    'personId': fields.Integer(required=True, description='Person Name'),
}
