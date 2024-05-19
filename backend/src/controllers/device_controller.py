from flask import Blueprint, Response, json, request
from src.middlewares.auth_middleware import token_required
from src.models.device_model import Device
from src import db
import dataclasses

from src.utils import send_wol

devices=Blueprint("devices", __name__)

# Route to handle devices for the current user
@devices.route('/', methods=["GET"])
@token_required
def handle_devices(current_user):
    return Response(
            response=json.dumps({ 'status': "success", "message": "Successfully retrieved devices", "data": current_user.devices }),
            status=200,
            mimetype='application/json'
        )

# Route to add a new device for the current user
@devices.route('/add', methods=["POST"])
@token_required
def handle_device_add(current_user):
    data = request.json
    if not all(key in data for key in ["name", "mac"]):
        return Response(
            response=json.dumps({'status': "failed", "message": "User Parameters Name, Mac are required"}),
            status=400,
            mimetype='application/json'
        )

    try: 
        device_obj = Device(
            name=data["name"],
            mac=data["mac"].replace(':', '').replace('-', ''),
            user_id=current_user.id,
        )
        db.session.add(device_obj)
        db.session.commit()

        return Response(
            response=json.dumps({'status': "success", "message": "Device add Successful", "device": dataclasses.asdict(device_obj)}),
            status=201,
            mimetype='application/json'
        )
    except Exception as e:
        return Response(
            response=json.dumps({'status': "failed", "message": "Error Occurred", "error": str(e)}),
            status=500,
            mimetype='application/json'
        )

# Route to remove a device for the current user
@devices.route('/remove/<device_id>', methods=["GET"])
@token_required
def handle_device_remove(current_user, device_id):
    try: 
        device_to_remove=next((device for device in current_user.devices if str(device.id) == device_id), None)
        if device_to_remove:
            db.session.delete(device_to_remove)
            db.session.commit()

            return Response(
                response=json.dumps({'status': "success", "message": "Device removed successfully"}),
                status=200,
                mimetype='application/json'
            )
        else:
            return Response(
                response=json.dumps({'status': "failed", "message": "The specified device does not exist in the database"}),
                status=400,
                mimetype='application/json'
            )
    except Exception as e:
        return Response(
            response=json.dumps({'status': "failed", "message": "Error Occurred", "error": str(e)}),
            status=500,
            mimetype='application/json'
        )
    
# Route to wol a device for the current user
@devices.route('/wol/<device_id>', methods=["GET"])
@token_required
def handle_device_wol(current_user, device_id):
    try: 
        device_to_wol=next((device for device in current_user.devices if str(device.id) == device_id), None)
        if device_to_wol:
            send_wol(device_to_wol.mac)
            return Response(
                response=json.dumps({'status': "success", "message": "Device wol successfully"}),
                status=200,
                mimetype='application/json'
            )
        else:
            return Response(
                response=json.dumps({'status': "failed", "message": "The specified device does not exist in the database"}),
                status=400,
                mimetype='application/json'
            )
    except Exception as e:
        return Response(
            response=json.dumps({'status': "failed", "message": "Error Occurred", "error": str(e)}),
            status=500,
            mimetype='application/json'
        )
