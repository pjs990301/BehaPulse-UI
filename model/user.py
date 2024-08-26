from flask_restx import fields

user_model = {
    'userEmail': fields.String(required=True, description='Email'),
    'userPassword': fields.String(required=True, description='Password'),
    'userName': fields.String(required=True, description='Name'),
    'createdAt': fields.DateTime(description='Created At'),
    'securityQuestion': fields.String(required=True, description='Security Question'),
    'securityAnswer': fields.String(required=True, description='Security Answer'),
}

login_model = {
    'userEmail': fields.String(required=True, description='Email'),
    'userPassword': fields.String(required=True, description='Password'),
}
security_question_model = {
    'securityQuestion': fields.String(required=True, description='Security Question'),
    'securityAnswer': fields.String(required=True, description='Security Answer'),
}
