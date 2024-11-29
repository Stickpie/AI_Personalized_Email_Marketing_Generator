from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow all origins to access this server

@app.route('/api/generate_email', methods=['POST'])
def generate_email():
    print("Request received!")
    return jsonify({"message": "connected"}), 200

if __name__ == '__main__':
    app.run(debug=True)
