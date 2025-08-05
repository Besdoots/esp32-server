from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return '✅ Server is running!'

@app.route('/upload', methods=['POST'])
def upload():
    if request.data:
        try:
            text = request.data.decode('utf-8')
            print("📩 ESP32 gửi:", text)
            return jsonify({'message': 'Text received', 'data': text}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'No data received'}), 400
