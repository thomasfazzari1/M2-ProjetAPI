from flask import Blueprint, request, jsonify
import requests
import os

match_bp = Blueprint('match', __name__)
MATCH_SERVICE_URL = os.getenv('MATCH_SERVICE_URL')


@match_bp.route('/create_sport', methods=['POST'])
def create_sport():
    response = requests.post(f"{MATCH_SERVICE_URL}/create_sport", json=request.get_json())
    return jsonify(response.json()), response.status_code


@match_bp.route('/get_all_sports', methods=['GET'])
def get_all_sports():
    response = requests.get(f"{MATCH_SERVICE_URL}/get_all_sports")
    return jsonify(response.json()), response.status_code
