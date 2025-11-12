from flask import Flask, request, jsonify
import os
import json

app = Flask(__name__)

@app.route("/")
def index():
    return """
    <h2>🎵 Rhythm JSON Converter</h2>
    <p>POST /convert にリズムJSONを送ると、noteのタイミング・タイプ・長さを抽出して返します。</p>
    <p>例: <code>curl -X POST -H "Content-Type: application/json" -d '{"sections":[{"notes":[{"timing":500,"type":"tap","length":0}]}]}' https://your-app-name.onrender.com/convert</code></p>
    """

@app.route("/convert", methods=["POST"])
def convert_json():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "JSONが送られていません"}), 400

        # "sections" キーが存在するかチェック
        if "sections" not in data:
            return jsonify({"error": "'sections'キーが見つかりません"}), 400

        result = []

        # 各sectionを処理
        for section in data["sections"]:
            notes = section.get("notes", [])
            for note in notes:
                # note内のデータを安全に取得
                timing = note.get("timing", 0)
                note_type = note.get("type", "unknown")
                length = note.get("length", 0)

                # 変換結果としてリストに追加
                result.append({
                    "timing": timing,
                    "type": note_type,
                    "length": length
                })

        return jsonify({"converted": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # RenderではPORT環境変数を必ず使用する
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
