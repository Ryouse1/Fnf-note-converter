from flask import Flask, request, render_template, jsonify, send_file
import json
import io
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files.get("file")
    text_data = request.form.get("chart_data")

    # JSONの取得
    if file:
        try:
            data = json.load(file)
        except Exception:
            return jsonify({"error": "JSONファイルの読み込みに失敗しました"}), 400
    elif text_data:
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return jsonify({"error": "JSONの形式が正しくありません"}), 400
    else:
        return jsonify({"error": "JSONデータをアップロードまたは貼り付けてください"}), 400

    converted_lines = []

    # FNFチャート構造からノーツを変換
    if "song" in data and "notes" in data["song"]:
        for section in data["song"]["notes"]:
            for note in section.get("sectionNotes", []):
                if len(note) >= 3:
                    time_ms = float(note[0])
                    direction_raw = int(note[1])
                    sustain_ms = float(note[2])

                    # 秒に変換
                    sec = time_ms / 1000.0
                    sustain = sustain_ms / 1000.0

                    # プレイヤーと方向を数値で設定
                    # プレイヤー2 → 1〜4、プレイヤー1 → 5〜8
                    if direction_raw in [0, 1, 2, 3]:
                        note_type = direction_raw + 1  # 1〜4
                    else:
                        note_type = direction_raw + 1  # 念のため一致させる

                    line = f"{{{round(sec,3)}}}: {{{note_type}}}: {{}}: {{{round(sustain,3)}}}"
                    converted_lines.append(line)
    else:
        return jsonify({"error": "JSON内に'song'や'notes'が見つかりません"}), 400

    result_text = "\n".join(converted_lines)
    return jsonify({"result": result_text})

@app.route('/download', methods=['POST'])
def download():
    content = request.form.get("content", "")
    if not content:
        return jsonify({"error": "内容が空です"}), 400

    buf = io.BytesIO()
    buf.write(content.encode('utf-8'))
    buf.seek(0)
    return send_file(buf, as_attachment=True, download_name="converted.txt", mimetype='text/plain')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
