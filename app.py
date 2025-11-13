from flask import Flask, render_template, request
import json

app = Flask(__name__)

def convert_notes(data):
    result = []
    for note in data:
        ms = note.get("ms", 0)
        note_type = note.get("type", 0)
        length = note.get("length", 0)
        
        # プレイヤー判定（1〜4: player2、5〜8: player1）
        if note_type in [1, 2, 3, 4]:
            player = "player2"
        else:
            player = "player1"

        result.append(f"{ms}: {note_type}: {player}: {length}")
    return "\n".join(result)

@app.route("/", methods=["GET", "POST"])
def index():
    converted_text = ""
    if request.method == "POST":
        if "file" in request.files:
            file = request.files["file"]
            try:
                data = json.load(file)
                converted_text = convert_notes(data)
            except Exception as e:
                converted_text = f"JSON読み込みエラー: {e}"
        elif "json_text" in request.form:
            try:
                data = json.loads(request.form["json_text"])
                converted_text = convert_notes(data)
            except Exception as e:
                converted_text = f"JSON読み込みエラー: {e}"
    return render_template("index.html", converted_text=converted_text)

if __name__ == "__main__":
    # 0.0.0.0 で外部アクセス可能に、portも指定
    app.run(host="0.0.0.0", port=5000, debug=True)
