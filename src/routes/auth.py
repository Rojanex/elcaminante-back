from flask import Blueprint, request, jsonify
import uuid
from firebase_admin import firestore, auth, credentials
from requests import post
from .decorators import role_required

db = firestore.client()
userRef = db.collection('user')

auth_bp = Blueprint('auth', __name__)


def get_db():
    return firestore.client()

@auth_bp.route('/add', methods=['POST'])
@role_required('client')
def create():
    try:
        id = uuid.uuid4()
        db = get_db()
        user_data = request.json
        role = user_data.pop('role', None)  # Get role from user_data, remove it from user_data
        print(role)
        userRef.document(id.hex).set(user_data)
        user = auth.create_user(email=user_data['email'], password=user_data['password'])
        auth.set_custom_user_claims(user.uid, {'role': role})
        return jsonify({"success": True}), 200
    except Exception as err:
        return f"An error occured: {err}"
    

@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    try:
        user = auth.get_user_by_email(email)
    except auth.UserNotFoundError:
        return jsonify({"message": "User not found"}), 404
    try:
        # Use Firebase's REST API to authenticate the user
        response = post(
            'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyDm7RVoLr71IqKiKP4_Z06XGU_SxBNMQSo',
            json={
                'email': email,
                'password': password,
                'returnSecureToken': True
            }
        )
        response.raise_for_status()
    except Exception as e:
        return jsonify({"message": "Invalid credentials"}), 401
    user_data = response.json()
    id_token = user_data['idToken']
    return jsonify({"id_token": id_token}), 200

@auth_bp.route('/list')
def read():
    try:
        all_users = [doc.to_dict() for doc in auth_bp.stream()]
        return jsonify(all_users), 200
    except Exception as err:
        return f"An error occured: {err}"