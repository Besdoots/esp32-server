from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return 'Server is running!'

@app.route('/upload', methods=['POST'])
def upload_audio():
    # Trường hợp 1: Nhận file audio (giống như hiện tại)
    if 'audio' in request.files:
        audio = request.files['audio']
        audio.save('received_audio.wav')  # Lưu file nhận được
        print("Đã nhận file âm thanh")
        return jsonify({'message': 'Audio received successfully!'})

    # Trường hợp 2: Nhận chuỗi text hoặc JSON
    try:
        raw_data = request.data.decode('utf-8')  # Lấy dữ liệu thô
        print(f"ESP32 gửi chuỗi: {raw_data}")
        return jsonify({'message': 'Text received', 'data': raw_data})
    except Exception as e:
        return jsonify({'error': 'Không đọc được dữ liệu', 'detail': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
