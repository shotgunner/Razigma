from flask import Flask, request, jsonify, send_from_directory
import hmac
import hashlib
import json
from urllib.parse import parse_qs
import time
import os
from dotenv import load_dotenv
from DataBase.admin import setup_admin
from DataBase.init import db
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

app = Flask(__name__)
migrate = Migrate(app, db)
setup_admin(app, db)

def generate_secret_key(bot_token):
    return hmac.new("WebAppData".encode(), bot_token.encode(), hashlib.sha256).digest()

def validate_telegram_data(init_data, secret_key):
    parsed_data = parse_qs(init_data)
    received_hash = parsed_data.pop('hash', None)
    
    if not received_hash:
        return False, "No hash provided"

    data_check_string = '\n'.join(f"{k}={v[0]}" for k, v in sorted(parsed_data.items()))
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    
    if not hmac.compare_digest(calculated_hash, received_hash[0]):
        return False, "Invalid hash"
    
    auth_date = int(parsed_data.get('auth_date', [0])[0])
    if int(time.time()) - auth_date > 86400:  # 24 hours
        return False, "Data is outdated"
    
    return True, parsed_data

@app.route('/validate', methods=['POST'])
def validate_data():
    init_data = request.form.get('init_data')
    if not init_data:
        return jsonify({"error": "No init_data provided"}), 400

    is_valid, result = validate_telegram_data(init_data, generate_secret_key(BOT_TOKEN))

    if is_valid:
        user_data = json.loads(result.get('user', ['{}'])[0])
        return jsonify({
            "status": "success",
            "message": "Data is valid and from Telegram",
            "user": user_data
        })
    else:
        return jsonify({
            "status": "error",
            "message": result
        }), 400

def get_level_data(user_data):
    pass
    
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/script.js')
def serve_script():
    return send_from_directory('.', 'script.js')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
