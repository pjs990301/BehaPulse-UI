from flask_restx import Resource, Namespace, reqparse
from model import *
from database import db, cursor
from flask import request

admin_ns = Namespace('admin', description='Admin API', doc='/admin', path='/admin')
admin_field = admin_ns.model('AdminModel', administrator_model)
login_field = admin_ns.model('LoginModel', login_model)
security_question_field = admin_ns.model('SecurityQuestionModel', security_question_model)


@admin_ns.route('/register')
class RegisterResource(Resource):
    @admin_ns.expect(admin_field, validate=True)
    def post(self):
        """
        관리자 등록
        """
        if not request.is_json:
            return {'message': 'Missing JSON in request'}, 400

        data = request.json

        required_keys = ['adminEmail', 'adminPassword', 'adminName', 'securityQuestion', 'securityAnswer']
        if not all(key in data for key in required_keys):
            return {"message": "Missing required fields."}, 400

        email = data['adminEmail']
        password = data['adminPassword']
        name = data['adminName']
        security_question = data['securityQuestion']
        security_answer = data['securityAnswer']

        try:
            # 기존 관리자 존재 여부 확인
            query = "SELECT * FROM administrator WHERE adminEmail = %s"
            cursor.execute(query, (email,))
            existing_admin = cursor.fetchone()

            if existing_admin:
                return {'message': 'Admin already exists'}, 400

            # 관리자 등록
            query = "INSERT INTO administrator (adminEmail, adminPassword, adminName, securityQuestion, securityAnswer) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (email, password, name, security_question, security_answer))
            db.commit()

            return {'message': 'Admin registered successfully'}, 201

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500


@admin_ns.route('/login')
class LoginResource(Resource):
    @admin_ns.expect(login_field, validate=True)
    def post(self):
        """
        관리자 로그인
        """
        if not request.is_json:
            return {'message': 'Missing JSON in request'}, 400

        data = request.json

        required_keys = ['adminEmail', 'adminPassword']
        if not all(key in data for key in required_keys):
            return {"message": "Missing required fields."}, 400

        email = data['adminEmail']
        password = data['adminPassword']

        try:
            # 관리자 존재 여부 확인
            query = "SELECT * FROM administrator WHERE adminEmail = %s AND adminPassword = %s"
            cursor.execute(query, (email, password))
            admin = cursor.fetchone()

            if not admin:
                return {'message': 'Admin not found'}, 404

            return {'message': 'Admin logged in successfully'}, 200

        except Exception as e:
            return {'message': str(e)}, 500


@admin_ns.route('/find_password/<string:adminEmail>')
class FindPasswordResource(Resource):
    def get(self, adminEmail):
        """
        비밀번호 찾기
        """
        try:
            query = "SELECT securityQuestion FROM administrator WHERE adminEmail = %s"
            cursor.execute(query, (adminEmail,))
            security_question = cursor.fetchone()

            if not security_question:
                return {'message': 'Admin not found'}, 404

            return {'securityQuestion': security_question[0]}, 200

        except Exception as e:
            return {'message': str(e)}, 500

    @admin_ns.expect(security_question_field, validate=True)
    def post(self, adminEmail):
        """
        비밀번호 찾기
        """
        if not request.is_json:
            return {'message': 'Missing JSON in request'}, 400

        data = request.json

        required_keys = ['securityAnswer']
        if not all(key in data for key in required_keys):
            return {"message": "Missing required fields."}, 400

        security_answer = data['securityAnswer']

        try:
            query = "SELECT adminPassword FROM administrator WHERE adminEmail = %s AND securityAnswer = %s"
            cursor.execute(query, (adminEmail, security_answer))
            admin_password = cursor.fetchone()

            if not admin_password:
                return {'message': 'Admin not found'}, 404

            return {'adminPassword': admin_password[0]}, 200

        except Exception as e:
            return {'message': str(e)}, 500
