from flask import Flask, request, jsonify
from database import connect_to_mysql

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to Flight Explorer"

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    connection = connect_to_mysql()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if user:
        return jsonify({"message": "Login successful", "user": user})
    else:
        return jsonify({"error": "Invalid username or password"}), 401

if __name__ == '__main__':
    app.run(debug=True)
