from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        raw_json = ""
        # ファイルアップロード優先、なければテキスト入力
        if "file" in request.files and request.files["file"].filename != "":
            raw_json = request.files["file"].read().decode("utf-8")
        else:
            raw_json = request.form.get("json_text", "")

        try:
            # JSON読み込み
            data = json.loads(raw_json)
            notes_data = data.get("song", {}).get("notes", [])
            all_notes = []

            # 全セクションからノーツ抽出
            for section in notes_data:
                for note in section.get("sectionNotes", []):
                    # note = [time(ms), type, sustain(ms), ...]
                    time_ms = note[0]
                    note_type = int(note[1]) + 1  # 0-based → 1〜8に補正
                    sustain_ms = note[2] if len(note) > 2 else 0
                    all_notes.append((time_ms, note_type, sustain_ms))

            # 時間でソート
            all_notes.sort(key=lambda x: x[0])

            # 整形
            result_lines = []
            for time_ms, note_type, sustain_ms in all_notes:
                time_sec = time_ms / 1000
                sustain_sec = sustain_ms / 1000
                line = f"{{{time_sec:.3f}}}: {{{note_type}}}: {{}}: {{{sustain_sec:.3f}}}"
                result_lines.append(line)

            result = "\n".join(result_lines)

        except Exception as e:
            result = f"⚠️ JSON解析エラー: {e}"

    return render_template("index.html", result=result)


if __name__ == "__main__":
    # Renderでも動くようにポート明示
    app.run(host="0.0.0.0", port=10000)
