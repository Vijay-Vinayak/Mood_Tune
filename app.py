import cv2
import os
from flask import Flask, render_template, request, redirect, url_for
from utils.emotion_detector import detect_emotion

app = Flask(__name__)

song_map = {
    "Happy": ["https://www.youtube.com/watch?v=y6Sxv-sUYtM"],
    "Sad": ["https://www.youtube.com/watch?v=hLQl3WQQoQ0"],
    "Angry": ["https://www.youtube.com/watch?v=v2AC41dglnM"],
    "Neutral": ["https://www.youtube.com/watch?v=JGwWNGJdvx8"],
    "Surprise": ["https://www.youtube.com/watch?v=RgKAFK5djSk"],
    "Fear": ["https://www.youtube.com/watch?v=RB-RcX5DS5A"],
    "Disgust": ["https://www.youtube.com/watch?v=OPf0YbXqDm0"]
}

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/capture", methods=["POST"])
def capture():
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    cam.release()

    if not ret:
        return "Failed to capture image"

    os.makedirs("static", exist_ok=True)
    img_path = "static/captured.jpg"
    cv2.imwrite(img_path, frame)

    emotion = detect_emotion(img_path)
    song_link = song_map.get(emotion, [""])[0]

    return render_template("result.html", emotion=emotion, song_url=song_link, img="captured.jpg")

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
