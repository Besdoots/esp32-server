from flask import Flask, request, jsonify, send_file
import os
from datetime import datetime
import wave
import openai
from gtts import gTTS

app = Flask(__name__)

UPLOAD_FOLDER = 'recordings'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 👉 API key lấy từ biến môi trường để bảo mật
openai.api_key = os.getenv("OPENAI_API_KEY")

def save_raw_to_wav(raw_path, wav_path):
    with open(raw_path, 'rb') as raw_file:
        raw_data = raw_file.read()

    with wave.open(wav_path, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
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
    mp3_path = raw_path.replace(".raw", ".mp3")

    with open(raw_path, 'wb') as f:
        f.write(raw_data)

    try:
        save_raw_to_wav(raw_path, wav_path)
        text = transcribe_audio(wav_path)
        print("🎤 Nội dung:", text)

        reply = chatgpt_reply(text)
        print("💬 Trả lời:", reply)

        tts = gTTS(reply, lang='vi')
        tts.save(mp3_path)

        return jsonify({"transcript": text, "reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/response-audio", methods=["GET"])
def send_tts_audio():
    files = sorted(
        [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(".mp3")],
        key=lambda x: os.path.getmtime(os.path.join(UPLOAD_FOLDER, x)),
        reverse=True
    )

    if not files:
        return "❌ Không có file TTS!", 400

    latest = os.path.join(UPLOAD_FOLDER, files[0])
    return send_file(latest, mimetype="audio/mpeg")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
