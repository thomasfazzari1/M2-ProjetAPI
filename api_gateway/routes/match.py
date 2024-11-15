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


@match_bp.route('/create_equipe', methods=['POST'])
def create_equipe():
    response = requests.post(f"{MATCH_SERVICE_URL}/create_equipe", json=request.get_json())
    return jsonify(response.json()), response.status_code


@match_bp.route('/get_all_equipes', methods=['GET'])
def get_all_equipes():
    response = requests.get(f"{MATCH_SERVICE_URL}/get_all_equipes")
    return jsonify(response.json()), response.status_code


@match_bp.route('/delete_equipe', methods=['POST'])
def delete_equipe():
    response = requests.post(f"{MATCH_SERVICE_URL}/delete_equipe", json=request.get_json())
    return jsonify(response.json()), response.status_code


@match_bp.route('/create_match', methods=['POST'])
def create_match():
    response = requests.post(f"{MATCH_SERVICE_URL}/create_match", json=request.get_json())
    return jsonify(response.json()), response.status_code


@match_bp.route('/get_all_matchs', methods=['GET'])
def get_all_matchs():
    response = requests.get(f"{MATCH_SERVICE_URL}/get_all_matchs")
    return jsonify(response.json()), response.status_code


@match_bp.route('/delete_match', methods=['POST'])
def delete_match():
    response = requests.post(f"{MATCH_SERVICE_URL}/delete_match", json=request.get_json())
    return jsonify(response.json()), response.status_code
