from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return 'Server is running!'

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file uploaded'}), 400

    audio = request.files['audio']
    audio.save('received_audio.wav')  # Lưu file nhận được

    return jsonify({'message': 'Audio received successfully!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
