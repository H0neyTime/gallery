from flask import Flask, request, render_template, redirect, url_for
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"

def load_paintings():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_paintings(paintings):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(paintings, f, indent=4, ensure_ascii=False)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        artist = request.form.get("artist")
        title = request.form.get("title")
        year = request.form.get("year")
        note = request.form.get("note")

        if artist and title and year:
            paintings = load_paintings()
            paintings.append({
                "artist": artist,
                "title": title,
                "year": year,
                "note": note or "—"
            })
            save_paintings(paintings)
        return redirect(url_for("index"))

    paintings = load_paintings()
    return render_template("index.html", paintings=paintings)

if __name__ == "__main__":
    app.run(debug=True)
