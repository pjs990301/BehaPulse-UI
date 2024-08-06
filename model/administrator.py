from flask_restx import fields

administrator_model = {
    'adminId': fields.String(required=True, description='Admin ID'),
    'adminPassword': fields.String(required=True, description='Password'),
    'adminName': fields.String(required=True, description='Name'),
    'adminEmail': fields.String(description='Email'),
    'createdAt': fields.DateTime(description='Created At'),
    'securityQuestion': fields.String(required=True, description='Security Question'),
    'securityAnswer': fields.String(required=True, description='Security Answer'),
}

login_model = {
    'adminId': fields.String(required=True, description='Admin ID'),
    'adminPassword': fields.String(required=True, description='Password'),
}
security_question_model = {
    'securityQuestion': fields.String(required=True, description='Security Question'),
    'securityAnswer': fields.String(required=True, description='Security Answer'),
}
