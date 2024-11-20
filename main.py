import os
from flask import Flask, request, jsonify
import db_service
from flasgger import Swagger, swag_from
from swagger.swagger_config import swagger_config


app = Flask(__name__)
swagger = Swagger(app, config=swagger_config)


# Check if DB exists, if not create empty new DB
db_service.init()


@app.route('/')
def index():
    return "Welcome to the Guest Microservice API :)"

# Get all guests
@app.route('/guests', methods=['GET'])
@swag_from('swagger/get_guests.yml')
def get_guests():
    try:
        guests = db_service.read_all()
        if guests:
            return jsonify(guests), 200
        else:
            return jsonify(message="No guests found"), 404
    except Exception as e:
        return jsonify(message="Connection Error"), 500

# Get a guest by ID
@app.route('/guests/<int:guest_id>', methods=['GET'])
#@swag_from('swagger/get_guest.yml')
def get_guest(guest_id):
    guest = db_service.read(guest_id)
    if guest:
        return jsonify(guest), 200
    else:
        return jsonify(message="Guest not found"), 404

# Add a new guest
@app.route('/guests', methods=['POST'])
#@swag_from('swagger/add_guest.yml')
def add_guest():
    data = request.get_json()

    if not data:
        return jsonify(message="Data is required"), 400

    if db_service.read(data['guestId']):
        return jsonify(message="Guest already exists"), 409

    guest_id = db_service.create(data)

    if not guest_id:
        return jsonify(message="Error creating guest"), 500

    return jsonify(message=f"Guest created successfully with ID {guest_id}"), 201

# Delete a guest by ID
@app.route('/guests/<int:guest_id>', methods=['DELETE'])
#@swag_from('swagger/delete_guest.yml')
def delete_guest(guest_id):
    guest = db_service.read(guest_id)
    
    if not guest:
        return jsonify(message="Guest not found"), 404

    db_service.delete(guest_id)
    return jsonify(message=f"Guest with ID {guest_id} deleted successfully"), 200

if __name__ == '__main__':
    app.run()

