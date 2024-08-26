from flask_restx import Resource, Namespace, reqparse
from model import *

from flask import request
import json
import mysql.connector

# 데이터베이스 설정을 파일에서 불러옵니다.
with open('config/db_config.json', 'r') as f:
    db_config = json.load(f)

device_ns = Namespace('device', description='Device API', doc='/device', path='/device')
device_field = device_ns.model('DeviceModel', device_model)


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

        required_keys = ['macAddress', 'type']
        if not all(key in data for key in required_keys):
            return {"message": "Missing required fields."}, 400

        mac_address = data['macAddress']
        device_type = data['type']
        install_location = data['install_location']
        room = data['room']
        check_date = data['check_date']
        on_off = data['on_off']
        note = data['note']

        db = mysql.connector.connect(
            host=db_config['Database']['host'],
            user=db_config['Database']['user'],
            password=db_config['Database']['password'],
            database=db_config['Database']['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = db.cursor()
        try:
            # MAC 주소 중복 확인
            query = "SELECT * FROM device WHERE macAddress = %s"
            cursor.execute(query, (mac_address,))
            existing_device = cursor.fetchone()

            if existing_device:
                return {'message': 'Device with this MAC address already exists'}, 400

            # 디바이스 등록
            query = "INSERT INTO device (macAddress, type, install_location, room, check_date, note, on_off) " \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (mac_address, device_type, install_location, room, check_date, note, on_off))
            db.commit()

            return {'message': 'Device registered successfully'}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500

        finally:
            cursor.close()


@device_ns.route('/delete/<string:macAddress>')
class DeleteDeviceResource(Resource):
    def delete(self, macAddress):
        """
        디바이스 삭제
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
            query = "DELETE FROM device WHERE macAddress = %s"
            cursor.execute(query, (macAddress,))
            db.commit()

            return {'message': 'Device deleted successfully'}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500

        finally:
            cursor.close()


@device_ns.route('/<int:deviceId>')
class GetDeviceResource(Resource):
    def get(self, deviceId):
        """
        특정 디바이스 조회
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
            query = "SELECT * FROM device WHERE deviceId = %s"
            cursor.execute(query, (deviceId,))
            device = cursor.fetchone()

            if not device:
                return {'message': 'Device not found'}, 404

            device_data = {
                'deviceId': device[0],
                'macAddress': device[1],
                'type': device[2],
                'install_location': device[3],
                'room': device[4],
                'check_date': device[5].strftime('%Y-%m-%d'),
                'on_off': device[6],
                'note': device[7],
            }
            return {'device': device_data}, 200

        except Exception as e:
            db.rollback()  # 롤백 전에 현재 커서의 명령이 완료되었는지 확인
            return {'message': str(e)}, 500

        finally:
            cursor.close()


@device_ns.route('/<string:macAddress>')
class GetDeviceResource(Resource):
    def get(self, macAddress):
        """
        특정 디바이스 조회
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
            query = "SELECT * FROM device WHERE macAddress = %s"
            cursor.execute(query, (macAddress,))
            device = cursor.fetchone()

            if not device:
                return {'message': 'Device not found'}, 404

            device_data = {
                'deviceId': device[0],
                'macAddress': device[1],
                'type': device[2],
                'install_location': device[3],
                'room': device[4],
                'check_date': device[5].strftime('%Y-%m-%d'),
                'on_off': device[6],
                'note': device[7],
            }
            return {'device': device_data}, 200

        except Exception as e:
            db.rollback()

        finally:
            cursor.close()


@device_ns.route('/update/<string:macAddress>')
class UpdateDeviceResource(Resource):
    @device_ns.expect(device_field, validate=True)
    def put(self, macAddress):
        """
        특정 디바이스 정보 수정
        """
        if not request.is_json:
            return {'message': 'Missing JSON in request'}, 400

        data = request.json

        required_keys = ['type']
        if not all(key in data for key in required_keys):
            return {"message": "Missing required fields."}, 400

        macAddress = macAddress
        device_type = data['type']
        install_location = data['install_location']
        room = data['room']
        check_date = data['check_date']
        on_off = data['on_off']
        note = data['note']

        db = mysql.connector.connect(
            host=db_config['Database']['host'],
            user=db_config['Database']['user'],
            password=db_config['Database']['password'],
            database=db_config['Database']['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = db.cursor()
        try:
            query = "UPDATE device SET type = %s, install_location = %s, room = %s, check_date = %s, note = %s, " \
                    "on_off = %s WHERE macAddress = %s"
            cursor.execute(query, (device_type, install_location, room, check_date, note, on_off, macAddress))
            db.commit()

            return {'message': 'Device updated successfully'}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500

        finally:
            cursor.close()
