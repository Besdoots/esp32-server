from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ ESP32 Voice Server đang chạy!"

@app.route("/audio", methods=["POST"])
def receive_audio():
    audio_data = request.data
    print(f"📥 Nhận được {len(audio_data)} byte từ ESP32")
    
    # In rõ nội dung chuỗi (nếu là text)
    try:
        print("📄 Nội dung gửi lên:")
        print(audio_data.decode())  # giải mã từ byte sang chuỗi UTF-8
    except Exception as e:
        print("⚠️ Không thể giải mã nội dung:", e)

    return "✅ Đã nhận âm thanh!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
