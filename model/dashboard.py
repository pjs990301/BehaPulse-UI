from flask_restx import fields

dashboard_model = {
    'name': fields.String(required=True, description='Name'),
    'gender': fields.String(required=True, description='Gender'),
    'birth': fields.Date(description='Birth'),
    'location': fields.String(description='Location'),
}
