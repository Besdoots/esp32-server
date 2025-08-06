from flask import Flask, request, jsonify, send_file
import os
from datetime import datetime
import wave
import openai
from gtts import gTTS

app = Flask(__name__)

UPLOAD_FOLDER = 'recordings'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ✅ Thay bằng API key của bạn
openai.api_key = "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"  # <-- THAY VÀO API KEY THỰC

# ----------------------
# 🔧 Hàm hỗ trợ xử lý âm thanh
# ----------------------

def save_raw_to_wav(raw_path, wav_path):
    with open(raw_path, 'rb') as raw_file:
        raw_data = raw_file.read()
    with wave.open(wav_path, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)  # 16-bit = 2 byte
        wav_file.setframerate(8000)
        wav_file.writeframes(raw_data)

def transcribe_audio(file_path):
    with open(file_path, "rb") as f:
        transcript = openai.Audio.transcribe("whisper-1", f)
    return transcript['text']

def chatgpt_reply(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Bạn là trợ lý thân thiện."},
            {"role": "user", "content": text}
        ]
    )
    return response['choices'][0]['message']['content']

# ----------------------
# 🔵 Các route chính
# ----------------------

@app.route("/")
def home():
    return "✅ ESP32 Voice Server đang chạy!"

@app.route("/audio", methods=["POST"])
def receive_audio():
    raw_data = request.data
    if not raw_data:
        return "❌ Không có dữ liệu!", 400

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    raw_path = os.path.join(UPLOAD_FOLDER, f"audio_{timestamp}.raw")
    wav_path = raw_path.replace(".raw", ".wav")

    with open(raw_path, 'ab') as f:
        f.write(raw_data)

    # 🔄 Chuyển sang WAV
    save_raw_to_wav(raw_path, wav_path)

    try:
        # 🧠 Nhận diện giọng nói
        text = transcribe_audio(wav_path)
        print("👊 Văn bản nhận được:", text)

        # 💬 ChatGPT trả lời
        reply = chatgpt_reply(text)
        print("🔊 Trả lời:", reply)

        # 🗣️ Tạo file MP3 từ trả lời
        tts = gTTS(reply, lang='vi')
        tts_path = os.path.join(UPLOAD_FOLDER, f"reply_{timestamp}.mp3")
        tts.save(tts_path)

        return jsonify({
            "transcript": text,
            "reply": reply,
            "audio_url": f"/speak/{os.path.basename(tts_path)}"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/playback", methods=["GET"])
def playback():
    files = sorted(
        [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(".wav")],
        key=lambda x: os.path.getmtime(os.path.join(UPLOAD_FOLDER, x)),
        reverse=True
    )
    if not files:
        return "❌ Không có file để phát!", 404

    latest = os.path.join(UPLOAD_FOLDER, files[0])
    return send_file(latest, mimetype="audio/wav")

@app.route("/speak/<filename>")
def speak(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(path):
        return "❌ Không tìm thấy file âm thanh.", 404
    return send_file(path, mimetype="audio/mpeg")

# ----------------------
# ✅ Khởi động Flask
# ----------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
