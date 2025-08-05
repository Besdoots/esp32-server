from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ ESP32 Voice Server đang chạy!"

@app.route("/audio", methods=["POST"])
def receive_audio():
    audio_data = request.data
    print(f"📥 Nhận được {len(audio_data)} byte từ ESP32")
    return "✅ Đã nhận âm thanh!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
