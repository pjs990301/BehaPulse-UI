from flask_restx import Resource, Namespace, reqparse
from model import *
from database import db, cursor
from flask import request

device_ns = Namespace('device', description='Device API', doc='/device', path='/device')
device_field = device_ns.model('DeviceModel', device_model)


@device_ns.route('/devices')
class DeviceResource(Resource):
    def get(self):
        """
        모든 디바이스 조회
        """
        try:
            query = "SELECT * FROM device"
            cursor.execute(query)
            devices = cursor.fetchall()

            if not devices:
                return {'message': 'No device found'}, 404

            return {'devices': devices}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500


@device_ns.route('/register')
class RegisterResource(Resource):
    @device_ns.expect(device_field, validate=True)
    def post(self):
        """
        디바이스 등록
        """
        if not request.is_json:
            return {'message': 'Missing JSON in request'}, 400

        data = request.json

        required_keys = ['macAddress']
        if not all(key in data for key in required_keys):
            return {"message": "Missing required fields."}, 400

        mac_address = data['macAddress']

        try:
            # MAC 주소 중복 확인
            query = "SELECT * FROM device WHERE macAddress = %s"
            cursor.execute(query, (mac_address,))
            existing_device = cursor.fetchone()

            if existing_device:
                return {'message': 'Device with this MAC address already exists'}, 400

            # 디바이스 등록
            query = "INSERT INTO device (macAddress) VALUES (%s)"
            cursor.execute(query, (mac_address,))
            db.commit()

            return {'message': 'Device registered successfully'}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500


@device_ns.route('/delete/<string:macAddress>')
class DeleteDeviceResource(Resource):
    def delete(self, macAddress):
        """
        디바이스 삭제
        """
        try:
            query = "DELETE FROM device WHERE macAddress = %s"
            cursor.execute(query, (macAddress,))
            db.commit()

            return {'message': 'Device deleted successfully'}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500
