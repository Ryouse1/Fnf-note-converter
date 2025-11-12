from flask import Flask, render_template, request, send_file
import os
import json
import io

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")
        if not file:
            return render_template("index.html", error="ファイルを選択してください。")

        try:
            data = json.load(file)
            result_lines = []

            # 曲データに応じた変換
            if "song" in data and "notes" in data["song"]:
                for section in data["song"]["notes"]:
                    bpm = section.get("bpm", 120)
                    for note in section.get("sectionNotes", []):
                        # note構造: [time(ms?), type, length?, extra?]
                        time_val = note[0]
                        note_type = note[1] if len(note) > 1 else 0
                        length = note[2] if len(note) > 2 else 0

                        # ミリ秒→秒変換（仮にbpmが使える場合）
                        sec = round((time_val / (bpm / 60) / 1000) * 95, 3)

                        result_lines.append(f"{sec}: {{type:{note_type}, length:{length}}}")

            elif "sections" in data:
                # 別フォーマット対応
                for section in data["sections"]:
                    for note in section.get("notes", []):
                        t = note.get("timing", 0)
                        ntype = note.get("type", "unknown")
                        length = note.get("length", 0)
                        result_lines.append(f"{t/1000:.3f}: {{type:{ntype}, length:{length}}}")
            else:
                return render_template("index.html", error="不明なJSON構造です。")

            # テキストにまとめる
            result_text = "\n".join(result_lines)

            # コピペ用表示 + ダウンロードリンク用
            return render_template("index.html", result=result_text)

        except Exception as e:
            return render_template("index.html", error=f"エラー: {e}")

    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
