from flask_restx import Resource, Namespace, reqparse
from model import *
from flask import request

import json
import mysql.connector

# 데이터베이스 설정을 파일에서 불러옵니다.
with open('config/db_config.json', 'r') as f:
    db_config = json.load(f)

user_ns = Namespace('user', description='User API', doc='/user', path='/user')
user_field = user_ns.model('UserModel', user_model)
login_field = user_ns.model('LoginModel', login_model)
security_question_field = user_ns.model('SecurityQuestionModel', security_question_model)


@user_ns.route('/register')
class RegisterResource(Resource):
    @user_ns.expect(user_field, validate=True)
    def post(self):
        """
        유저 등록
        """
        if not request.is_json:
            return {'message': 'Missing JSON in request'}, 400

        data = request.json

        required_keys = ['userEmail', 'userPassword', 'userName', 'securityQuestion', 'securityAnswer']
        if not all(key in data for key in required_keys):
            return {"message": "Missing required fields."}, 400

        email = data['userEmail']
        password = data['userPassword']
        name = data['userName']
        security_question = data['securityQuestion']
        security_answer = data['securityAnswer']

        db = mysql.connector.connect(
            host=db_config['Database']['host'],
            user=db_config['Database']['user'],
            password=db_config['Database']['password'],
            database=db_config['Database']['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = db.cursor()
        try:
            # 기존 유저 존재 여부 확인
            query = "SELECT * FROM user WHERE userEmail = %s"
            cursor.execute(query, (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                return {'message': 'user already exists'}, 400

            # 유저 등록
            query = "INSERT INTO user (userEmail, userPassword, userName, securityQuestion, securityAnswer) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (email, password, name, security_question, security_answer))
            db.commit()

            return {'message': 'user registered successfully'}, 201

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500

        finally:
            cursor.close()


@user_ns.route('/login')
class LoginResource(Resource):
    @user_ns.expect(login_field, validate=True)
    def post(self):
        """
        유저 로그인
        """
        if not request.is_json:
            return {'message': 'Missing JSON in request'}, 400

        data = request.json

        required_keys = ['userEmail', 'userPassword']
        if not all(key in data for key in required_keys):
            return {"message": "Missing required fields."}, 400

        email = data['userEmail']
        password = data['userPassword']

        db = mysql.connector.connect(
            host=db_config['Database']['host'],
            user=db_config['Database']['user'],
            password=db_config['Database']['password'],
            database=db_config['Database']['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = db.cursor()
        try:
            # 유저 존재 여부 확인
            query = "SELECT * FROM user WHERE userEmail = %s AND userPassword = %s"
            cursor.execute(query, (email, password))
            user = cursor.fetchone()

            if not user:
                return {'message': 'user not found'}, 404

            return {'message': 'user logged in successfully'}, 200

        except Exception as e:
            return {'message': str(e)}, 500

        finally:
            cursor.close()


@user_ns.route('/find_password/<string:userEmail>')
class FindPasswordResource(Resource):
    def get(self, userEmail):
        """
        비밀번호 찾기
        """
        db = mysql.connector.connect(
            host=db_config['Database']['host'],
            user=db_config['Database']['user'],
            password=db_config['Database']['password'],
            database=db_config['Database']['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = db.cursor()
        try:
            query = "SELECT securityQuestion FROM user WHERE userEmail = %s"
            cursor.execute(query, (userEmail,))
            security_question = cursor.fetchone()

            if not security_question:
                return {'message': 'user not found'}, 404

            return {'securityQuestion': security_question[0]}, 200

        except Exception as e:
            return {'message': str(e)}, 500

        finally:
            cursor.close()

    @user_ns.expect(security_question_field, validate=True)
    def post(self, userEmail):
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

        db = mysql.connector.connect(
            host=db_config['Database']['host'],
            user=db_config['Database']['user'],
            password=db_config['Database']['password'],
            database=db_config['Database']['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = db.cursor()

        try:
            query = "SELECT userPassword FROM user WHERE userEmail = %s AND securityAnswer = %s"
            cursor.execute(query, (userEmail, security_answer))
            user_password = cursor.fetchone()

            if not user_password:
                return {'message': 'user not found'}, 404

            return {'userPassword': user_password[0]}, 200

        except Exception as e:
            return {'message': str(e)}, 500

        finally:
            cursor.close()


@user_ns.route('/delete/<string:userEmail>')
class DeleteUserResource(Resource):
    def delete(self, userEmail):
        """
        특정 유저 삭제
        """
        db = mysql.connector.connect(
            host=db_config['Database']['host'],
            user=db_config['Database']['user'],
            password=db_config['Database']['password'],
            database=db_config['Database']['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = db.cursor()
        try:
            # 유저 존재 여부 확인
            query = "SELECT * FROM user WHERE userEmail = %s"
            cursor.execute(query, (userEmail,))
            existing_user = cursor.fetchone()

            if not existing_user:
                return {'message': 'User not found'}, 404

            # 유저 삭제
            query = "DELETE FROM user WHERE userEmail = %s"
            cursor.execute(query, (userEmail,))
            db.commit()

            return {'message': 'User deleted successfully'}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500
        finally:
            cursor.close()


@user_ns.route('/<string:userEmail>')
class GetUserResource(Resource):
    def get(self, userEmail):
        """
        특정 유저 조회
        """
        db = mysql.connector.connect(
            host=db_config['Database']['host'],
            user=db_config['Database']['user'],
            password=db_config['Database']['password'],
            database=db_config['Database']['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = db.cursor()

        try:
            # 유저 존재 여부 확인
            query = "SELECT * FROM user WHERE userEmail = %s"
            cursor.execute(query, (userEmail,))
            user = cursor.fetchone()

            if not user:
                return {'message': 'User not found'}, 404

            user_data = {
                'userEmail': user[0],
                'userName': user[2],
                'createdAt': user[3].strftime('%Y-%m-%d'),
                'securityQuestion': user[4],
                'securityAnswer': user[5],
            }

            return {'user': user_data}, 200

        except Exception as e:
            return {'message': str(e)}, 500

        finally:
            cursor.close()
