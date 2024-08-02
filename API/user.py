from flask_restx import Resource, Namespace, reqparse
from model import *
from database import db, cursor
from flask import request

user_ns = Namespace('user', description='User API', doc='/user', path='/user')
user_field = user_ns.model('UserModel', user_model)


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

        required_keys = ['userId', 'userName', 'Birth']
        if not all(key in data for key in required_keys):
            return {"message": "Missing required fields."}, 400

        id = data['userId']
        name = data['userName']
        birth = data['Birth']

        try:
            # 기존 유저 존재 여부 확인
            query = "SELECT * FROM user WHERE userId = %s"
            cursor.execute(query, (id,))
            existing_user = cursor.fetchone()

            if existing_user:
                return {'message': 'User already exists'}, 400

            # 유저 등록
            query = "INSERT INTO user (userId, userName, Birth) VALUES (%s, %s, %s)"
            cursor.execute(query, (id, name, birth))
            db.commit()

            return {'message': 'User registered successfully'}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500


@user_ns.route('/users')
class UserResource(Resource):
    def get(self):
        """
        모든 유저 조회
        """
        try:
            query = "SELECT * FROM user"
            cursor.execute(query)
            users = cursor.fetchall()

            if not users:
                return {'message': 'No user found'}, 404

            user_list = []
            for user in users:
                user_list.append({
                    'userId': user[0],
                    'userName': user[1],
                    'Birth': user[2].strftime('%Y-%m-%d')
                })

            return {'users': user_list}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500


@user_ns.route('/update/<string:userId>')
class UpdateUserResource(Resource):
    @user_ns.expect(user_field, validate=True)
    def put(self, userId):
        """
        특정 유저 정보 수정
        """
        if not request.is_json:
            return {'message': 'Missing JSON in request'}, 400

        data = request.json

        required_keys = ['userName', 'Birth']
        if not all(key in data for key in required_keys):
            return {"message": "Missing required fields."}, 400

        name = data['userName']
        birth = data['Birth']

        try:
            # 유저 존재 여부 확인
            query = "SELECT * FROM user WHERE userId = %s"
            cursor.execute(query, (userId,))
            existing_user = cursor.fetchone()

            if not existing_user:
                return {'message': 'User not found'}, 404

            # 유저 정보 수정
            query = "UPDATE user SET userName = %s, Birth = %s WHERE userId = %s"
            cursor.execute(query, (name, birth, userId))
            db.commit()

            return {'message': 'User updated successfully'}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500


@user_ns.route('/delete/<string:userId>')
class DeleteUserResource(Resource):
    def delete(self, userId):
        """
        특정 유저 삭제
        """
        try:
            # 유저 존재 여부 확인
            query = "SELECT * FROM user WHERE userId = %s"
            cursor.execute(query, (userId,))
            existing_user = cursor.fetchone()

            if not existing_user:
                return {'message': 'User not found'}, 404

            # 유저 삭제
            query = "DELETE FROM user WHERE userId = %s"
            cursor.execute(query, (userId,))
            db.commit()

            return {'message': 'User deleted successfully'}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500


@user_ns.route('/<string:userId>')
class GetUserResource(Resource):
    def get(self, userId):
        """
        특정 유저 조회
        """
        try:
            # 유저 존재 여부 확인
            query = "SELECT * FROM user WHERE userId = %s"
            cursor.execute(query, (userId,))
            user = cursor.fetchone()

            if not user:
                return {'message': 'User not found'}, 404

            user_data = {
                'userId': user[0],
                'userName': user[1],
                'Birth': user[2].strftime('%Y-%m-%d')  # Convert date to string
            }

            return {'user': user_data}, 200

        except Exception as e:
            return {'message': str(e)}, 500
