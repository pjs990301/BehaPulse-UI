from flask_restx import Namespace, Resource, fields
from model import *
from database import db, cursor
from flask import request

user_room_ns = Namespace('user_room', description='User Room API', doc='/user_room', path='/user_room')
user_room_field = user_room_ns.model('UserRoomModel', user_room_model)


@user_room_ns.route('/user_rooms')
class UserRoomResource(Resource):
    def get(self):
        """
        모든 유저의 호실 조회
        """
        try:
            query = "SELECT * FROM user_room"
            cursor.execute(query)
            user_rooms = cursor.fetchall()

            if not user_rooms:
                return {'message': 'No user room found'}, 404

            return {'user_rooms': user_rooms}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500


@user_room_ns.route('/register')
class RegisterResource(Resource):
    @user_room_ns.expect(user_room_field, validate=True)
    def post(self):
        """
        유저의 호실 등록
        """
        if not request.is_json:
            return {'message': 'Missing JSON in request'}, 400

        data = request.json

        required_keys = ['userId', 'roomId']
        if not all(key in data for key in required_keys):
            return {"message": "Missing required fields."}, 400

        user_id = data['userId']
        room_id = data['roomId']

        try:
            # 기존 유저의 호실 존재 여부 확인
            query = "SELECT * FROM user_room WHERE userId = %s AND roomId = %s"
            cursor.execute(query, (user_id, room_id))
            existing_user_room = cursor.fetchone()

            if existing_user_room:
                return {'message': 'User room already exists'}, 400

            # 유저의 호실 등록
            query = "INSERT INTO user_room (userId, roomId) VALUES (%s, %s)"
            cursor.execute(query, (user_id, room_id))
            db.commit()

            return {'message': 'User room registered successfully'}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500


@user_room_ns.route('/user_rooms/<string:userId>')
class GetUserResource(Resource):
    def get(self, userId):
        """
        특정 유저의 호실 조회
        """
        try:
            query = "SELECT * FROM user_room WHERE userId = %s"
            cursor.execute(query, (userId,))
            user_rooms = cursor.fetchall()

            if not user_rooms:
                return {'message': 'No user room found'}, 404

            return {'user_rooms': user_rooms}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500


@user_room_ns.route('/user_rooms/<int:roomId>')
class GetRoomResource(Resource):
    def get(self, roomId):
        """
        특정 호실의 유저 조회
        """
        try:
            query = "SELECT * FROM user_room WHERE roomId = %s"
            cursor.execute(query, (roomId,))
            user_rooms = cursor.fetchall()

            if not user_rooms:
                return {'message': 'No user room found'}, 404

            return {'user_rooms': user_rooms}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500


@user_room_ns.route('/delete/<string:userId>')
class DeleteUserResource(Resource):
    def delete(self, userId):
        """
        특정 유저의 호실 삭제
        """
        try:
            query = "DELETE FROM user_room WHERE userId = %s"
            cursor.execute(query, (userId,))
            db.commit()

            return {'message': 'User room deleted successfully'}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500


@user_room_ns.route('/delete/<int:roomId>')
class DeleteRoomResource(Resource):
    def delete(self, roomId):
        """
        특정 호실의 유저 삭제
        """
        try:
            query = "DELETE FROM user_room WHERE roomId = %s"
            cursor.execute(query, (roomId,))
            db.commit()

            return {'message': 'User room deleted successfully'}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500


@user_room_ns.route('/update/<string:userId>')
class UpdateUserResource(Resource):
    @user_room_ns.expect(user_room_field, validate=True)
    def put(self, userId):
        """
        특정 유저의 호실 수정
        """
        if not request.is_json:
            return {'message': 'Missing JSON in request'}, 400

        data = request.json

        required_keys = ['roomId']
        if not all(key in data for key in required_keys):
            return {"message": "Missing required fields."}, 400

        room_id = data['roomId']

        try:
            query = "UPDATE user_room SET roomId = %s WHERE userId = %s"
            cursor.execute(query, (room_id, userId))
            db.commit()

            return {'message': 'User room updated successfully'}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500


@user_room_ns.route('/update/<int:roomId>')
class UpdateRoomResource(Resource):
    @user_room_ns.expect(user_room_field, validate=True)
    def put(self, roomId):
        """
        특정 호실의 유저 수정
        """
        if not request.is_json:
            return {'message': 'Missing JSON in request'}, 400

        data = request.json

        required_keys = ['userId']
        if not all(key in data for key in required_keys):
            return {"message": "Missing required fields."}, 400

        user_id = data['userId']

        try:
            query = "UPDATE user_room SET userId = %s WHERE roomId = %s"
            cursor.execute(query, (user_id, roomId))
            db.commit()

            return {'message': 'User room updated successfully'}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500
