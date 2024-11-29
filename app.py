from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/generate_email', methods=['POST'])
def generate_email():
    # Log to confirm the request was received
    print("Request received!")

    # Return a test response
    return jsonify({"message": "connected"}), 200

if __name__ == '__main__':
    app.run(debug=True)  # Start the server locally