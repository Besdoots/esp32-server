from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return 'Server is running!'

@app.route('/upload', methods=['POST'])
def upload_audio():
    if request.data:
        text = request.data.decode('utf-8')  # Giải mã bytes thành chuỗi
        print("ESP32 gửi chuỗi:", text)
        return jsonify({'message': 'Text received', 'data': text}), 200
    else:
        return jsonify({'error': 'No audio file or text received'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
S
