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


@match_bp.route('/delete_sport', methods=['POST'])
def delete_sport():
    response = requests.post(f"{MATCH_SERVICE_URL}/delete_sport", json=request.get_json())
    return jsonify(response.json()), response.status_code


@match_bp.route('/create_evenement', methods=['POST'])
def create_evenement():
    response = requests.post(f"{MATCH_SERVICE_URL}/create_evenement", json=request.get_json())
    return jsonify(response.json()), response.status_code


@match_bp.route('/get_all_evenements', methods=['GET'])
def get_all_evenements():
    response = requests.get(f"{MATCH_SERVICE_URL}/get_all_evenements")
    return jsonify(response.json()), response.status_code


@match_bp.route('/delete_evenement', methods=['POST'])
def delete_evenement():
    response = requests.post(f"{MATCH_SERVICE_URL}/delete_evenement", json=request.get_json())
    return jsonify(response.json()), response.status_code