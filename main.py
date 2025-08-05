from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ ESP32 Text Server đang chạy!"

@app.route('/text', methods=['POST'])
def receive_text():
    if not request.data:
        return jsonify({"error": "❌ Không nhận được dữ liệu"}), 400

    try:
        text = request.data.decode('utf-8')  # Giải mã bytes thành chuỗi
        print(f"📩 ESP32 gửi chuỗi: {text}")
        return jsonify({"message": "✅ Đã nhận chuỗi văn bản!", "data": text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
