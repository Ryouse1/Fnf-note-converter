from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# 方向変換マップ
DIRECTION_MAP = {
    1: "←", 2: "↓", 3: "↑", 4: "→",
    5: "←", 6: "↓", 7: "↑", 8: "→"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    try:
        data = request.files.get('file')
        if not data:
            return jsonify({"error": "No file uploaded."}), 400

        # JSON読み込み
        json_data = json.load(data)

        # "section" や "note" から情報を抽出
        result_lines = []
        for section in json_data.get("sections", []):
            for note in section.get("notes", []):
                time_sec = note.get("time", 0)
                note_type = note.get("type", 0)
                hold_time = note.get("hold", 0)

                # ノーツタイプを方向に変換
                direction = DIRECTION_MAP.get(note_type, "?")

                # 指定形式に変換
                line = f"{{{time_sec}}}: {{{direction}}}: {{}}: {{{hold_time}}}"
                result_lines.append(line)

        output_text = "\n".join(result_lines)
        return jsonify({"result": output_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
