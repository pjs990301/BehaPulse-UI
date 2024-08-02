from flask_restx import Resource, Namespace, reqparse
from model import *
from database import db, cursor
from flask import request

user_device_ns = Namespace('user_device', description='User Device API', doc='/user_device', path='/user_device')
user_device_field = user_device_ns.model('UserDeviceModel', user_device_model)


@user_device_ns.route('/register')
class RegisterResource(Resource):
    @user_device_ns.expect(user_device_field, validate=True)
    def post(self):
        """
        유저 디바이스 등록
        """
        if not request.is_json:
            return {'message': 'Missing JSON in request'}, 400

        data = request.json

        required_keys = ['userId', 'macAddress']
        if not all(key in data for key in required_keys):
            return {"message": "Missing required fields."}, 400

        user_id = data['userId']
        mac_address = data['macAddress']

        try:
            # 유저 존재 여부 확인
            query = "SELECT * FROM user WHERE userId = %s"
            cursor.execute(query, (user_id,))
            existing_user = cursor.fetchone()

            if not existing_user:
                return {'message': 'User not found'}, 404

            # 디바이스 존재 여부 확인 및 deviceId 가져오기
            query = "SELECT deviceId FROM device WHERE macAddress = %s"
            cursor.execute(query, (mac_address,))
            existing_device = cursor.fetchone()

            if not existing_device:
                return {'message': 'Device not found'}, 404

            device_id = existing_device[0]

            # 기존 유저 디바이스 존재 여부 확인
            query = "SELECT * FROM user_device WHERE userId = %s AND deviceId = %s"
            cursor.execute(query, (user_id, device_id))
            existing_user_device = cursor.fetchone()

            if existing_user_device:
                return {'message': 'User device already exists'}, 400

            # 유저 디바이스 등록
            query = "INSERT INTO user_device (userId, deviceId) VALUES (%s, %s)"
            cursor.execute(query, (user_id, device_id))
            db.commit()

            return {'message': 'User device registered successfully'}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500


@user_device_ns.route('/user_devices')
class UserDeviceResource(Resource):
    def get(self):
        """
        모든 유저 디바이스 조회
        """
        try:
            query = "SELECT * FROM user_device"
            cursor.execute(query)
            user_devices = cursor.fetchall()

            if not user_devices:
                return {'message': 'No user device found'}, 404

            return {'user_devices': user_devices}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500


@user_device_ns.route('/user_devices/<string:userId>')
class GetUserDeviceResource(Resource):
    def get(self, userId):
        """
        특정 유저의 디바이스 조회
        """
        try:
            query = "SELECT * FROM user_device WHERE userId = %s"
            cursor.execute(query, (userId,))
            user_devices = cursor.fetchall()

            if not user_devices:
                return {'message': 'No user device found'}, 404

            return {'user_devices': user_devices}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500


@user_device_ns.route('/delete/<string:userId>/<string:macAddress>')
class DeleteUserDeviceResource(Resource):
    def delete(self, userId, macAddress):
        """
        유저 디바이스 삭제
        """
        try:
            # 디바이스 존재 여부 확인 및 deviceId 가져오기
            query = "SELECT deviceId FROM device WHERE macAddress = %s"
            cursor.execute(query, (macAddress,))
            existing_device = cursor.fetchone()

            if not existing_device:
                return {'message': 'Device not found'}, 404

            device_id = existing_device[0]

            # 유저 디바이스 존재 여부 확인
            query = "SELECT * FROM user_device WHERE userId = %s AND deviceId = %s"
            cursor.execute(query, (userId, device_id))
            existing_user_device = cursor.fetchone()

            if not existing_user_device:
                return {'message': 'User device not found'}, 404

            # 유저 디바이스 삭제
            query = "DELETE FROM user_device WHERE userId = %s AND deviceId = %s"
            cursor.execute(query, (userId, device_id))
            db.commit()

            return {'message': 'User device deleted successfully'}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500
