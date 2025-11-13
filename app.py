from flask import Flask, request, render_template, send_file
import json
import io

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    output_texts = {}
    if request.method == "POST":
        # JSONアップロード or コピペ
        json_data = ""
        if "json_file" in request.files:
            file = request.files["json_file"]
            if file.filename != "":
                json_data = file.read().decode("utf-8")
        elif "json_text" in request.form:
            json_data = request.form["json_text"]

        try:
            data = json.loads(json_data)
            players = {}
            for note in data:
                player = note.get("player", "player1")
                ms = note.get("ms", 0)
                note_type = note.get("type", "tap")
                hold_length = note.get("hold", 0) if note_type == "hold" else 0
                line = f"{ms}: {note_type}: {{}}: {hold_length}"
                players.setdefault(player, []).append(line)

            # ソート
            for player in players:
                players[player].sort(key=lambda x: int(x.split(":")[0]))
                output_texts[player] = "\n".join(players[player])
        except Exception as e:
            output_texts["error"] = str(e)

    return render_template("index.html", output_texts=output_texts)

@app.route("/download/<player>")
def download(player):
    text = request.args.get("text", "")
    return send_file(
        io.BytesIO(text.encode("utf-8")),
        as_attachment=True,
        download_name=f"{player}.txt",
        mimetype="text/plain"
    )

if __name__ == "__main__":
    app.run(debug=True)
