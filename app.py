from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        raw_json = ""
        # ファイルアップロード優先、なければテキスト
        if "file" in request.files and request.files["file"].filename != "":
            raw_json = request.files["file"].read().decode("utf-8")
        else:
            raw_json = request.form.get("json_text", "")

        try:
            data = json.loads(raw_json)
            result_lines = []
            notes_data = data.get("song", {}).get("notes", [])

            for section in notes_data:
                for note in section.get("sectionNotes", []):
                    # note = [time(ms), noteType, sustain(ms), ...]
                    time_sec = note[0] / 1000  # 秒に変換
                    note_type = int(note[1]) + 1  # 0-based → 1〜8
                    sustain = 0
                    if len(note) > 2:
                        sustain = note[2] / 1000  # 伸ばしノーツ(ms→秒)

                    line = f"{{{time_sec:.3f}}}: {{{note_type}}}: {{}}: {{{sustain:.3f}}}"
                    result_lines.append(line)

            result = "\n".join(result_lines)

        except Exception as e:
            result = f"⚠️ JSON解析エラー: {e}"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
