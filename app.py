from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        try:
            # ファイルかテキスト入力のどちらかを取得
            if "json_file" in request.files and request.files["json_file"].filename != "":
                data = json.load(request.files["json_file"])
            else:
                data = json.loads(request.form["json_text"])

            result_lines = []

            # BPMなど不要、notes部分をパース
            for section in data.get("song", {}).get("notes", []):
                for note in section.get("sectionNotes", []):
                    time = note[0] / 1000 if note[0] > 10 else note[0]  # ms→秒換算っぽい補正
                    note_type = int(note[1])
                    hold = 0
                    if len(note) > 2:
                        hold = note[2] / 1000 if note[2] > 10 else note[2]
                    result_lines.append(f"{{{time}}}: {{{note_type}}}: {{}}: {{{hold}}}")

            result = "\n".join(result_lines)

        except Exception as e:
            result = f"変換エラー: {e}"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
