from flask_restx import Resource, Namespace, reqparse
from model import *
from database import db, cursor
from flask import request

room_ns = Namespace('room', description='Room API', doc='/room', path='/room')
room_field = room_ns.model('RoomModel', room_model)


@room_ns.route('/rooms')
class RoomResource(Resource):
    def get(self):
        """
        모든 호실 조회
        """
        try:
            query = "SELECT * FROM room"
            cursor.execute(query)
            rooms = cursor.fetchall()

            if not rooms:
                return {'message': 'No room found'}, 404

            return {'rooms': rooms}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500


@room_ns.route('/register')
class RegisterResource(Resource):
    @room_ns.expect(room_field, validate=True)
    def post(self):
        """
        호실 등록
        """
        if not request.is_json:
            return {'message': 'Missing JSON in request'}, 400

        data = request.json

        required_keys = ['roomId']
        if not all(key in data for key in required_keys):
            return {"message": "Missing required fields."}, 400

        id = data['roomId']

        try:
            # 기존 호실 존재 여부 확인
            query = "SELECT * FROM room WHERE roomId = %s"
            cursor.execute(query, (id,))
            existing_room = cursor.fetchone()

            if existing_room:
                return {'message': 'Room already exists'}, 400

            # 호실 등록
            query = "INSERT INTO room (roomId) VALUES (%s)"
            cursor.execute(query, (id,))
            db.commit()

            return {'message': 'Room registered successfully'}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500


@room_ns.route('/delete/<int:roomId>')
class DeleteRoomResource(Resource):
    def delete(self, roomId):
        """
        호실 삭제
        """
        try:
            query = "SELECT * FROM room WHERE roomId = %s"
            cursor.execute(query, (roomId,))
            existing_room = cursor.fetchone()

            if not existing_room:
                return {'message': 'Room not found'}, 404

            query = "DELETE FROM room WHERE roomId = %s"
            cursor.execute(query, (roomId,))
            db.commit()

            return {'message': 'Room deleted successfully'}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500

@room_ns.route('/test')
class RegisterResource(Resource):

    def get(self):
        return {'message': 'test success'}, 200

    def post(self):
        if request.is_json:
            json_data = request.get_json()
            print(json_data)
            return {'message': 'JSON received successfully', 'data': json_data}, 200
        else:
            return {'message': 'Request body must be JSON'}, 400