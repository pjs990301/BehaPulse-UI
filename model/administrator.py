from flask_restx import fields

administrator_model = {
    'adminEmail': fields.String(required=True, description='Email'),
    'adminPassword': fields.String(required=True, description='Password'),
    'adminName': fields.String(required=True, description='Name'),
    'createdAt': fields.DateTime(description='Created At'),
    'securityQuestion': fields.String(required=True, description='Security Question'),
    'securityAnswer': fields.String(required=True, description='Security Answer'),
}

login_model = {
    'adminEmail': fields.String(required=True, description='Email'),
    'adminPassword': fields.String(required=True, description='Password'),
}
security_question_model = {
    'securityQuestion': fields.String(required=True, description='Security Question'),
    'securityAnswer': fields.String(required=True, description='Security Answer'),
}
