from flask import Flask, request, render_template, jsonify, send_file
import json
import io
import os

app = Flask(__name__)

# ノーツタイプ対応表
DIRECTION_MAP = {
    0: "左", 1: "下", 2: "上", 3: "右",
    4: "左", 5: "下", 6: "上", 7: "右"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files.get("file")
    text_data = request.form.get("chart_data")

    # JSON読み込み
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

    # song -> notes -> sectionNotes
    if "song" in data and "notes" in data["song"]:
        for section in data["song"]["notes"]:
            for note in section.get("sectionNotes", []):
                if len(note) >= 3:
                    sec = float(note[0]) / 1000.0
                    note_type = int(note[1])
                    sustain = float(note[2]) / 1000.0
                    direction = DIRECTION_MAP.get(note_type, "不明")

                    line = f"{{{round(sec,3)}}}: {{{direction}}}: {{}}: {{{round(sustain,3)}}}"
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


# 🔥 Renderが自動で環境変数PORTを割り当てる
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
