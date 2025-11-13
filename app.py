from flask import Flask, render_template, request, send_file
import json
import io

app = Flask(__name__)

# --- ノーツタイプの設定 ---
NOTE_MAP = {
    1: "左", 2: "下", 3: "上", 4: "右",
    5: "左", 6: "下", 7: "上", 8: "右"
}

def convert_notes(data):
    notes_output = []

    # --- JSON構造の自動検出 ---
    if isinstance(data, dict):
        possible_keys = ["notes", "chart", "objects", "noteData", "events"]
        for key in possible_keys:
            if key in data:
                data = data[key]
                break

    # --- ノーツ抽出 ---
    for note in data:
        try:
            # 各ノーツの基本情報
            time = float(note.get("time") or note.get("startTime") or note.get("sec") or 0)
            note_type = int(note.get("type") or note.get("lane") or note.get("noteType") or 0)

            # --- プレイヤー識別 ---
            if note_type in range(1, 5):  # プレイヤー2
                player = 2
            elif note_type in range(5, 9):  # プレイヤー1
                player = 1
            else:
                continue  # 無効ノーツはスキップ

            # --- 伸ばしノーツ処理 ---
            hold_length = 0.0
            if "endTime" in note and note["endTime"]:
                hold_length = float(note["endTime"]) - time
            elif "hold" in note and note["hold"]:
                hold_length = float(note["hold"])
            elif "length" in note:
                hold_length = float(note["length"])

            # --- 出力整形 ---
            notes_output.append({
                "time": time,
                "note_type": note_type,
                "player": player,
                "hold": round(hold_length, 3)
            })
        except Exception:
            continue

    # --- 時間でソート ---
    notes_output.sort(key=lambda x: x["time"])

    # --- 出力フォーマット ---
    lines = []
    for n in notes_output:
        lines.append(f"{n['time']:.3f}: {n['note_type']}: {{}}: {n['hold']:.3f}")

    return "\n".join(lines)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    try:
        json_data = request.form['json_data']
        data = json.loads(json_data)
        output_text = convert_notes(data)

        # --- ダウンロード or コピペ用 ---
        if 'download' in request.form:
            return send_file(
                io.BytesIO(output_text.encode('utf-8')),
                mimetype='text/plain',
                as_attachment=True,
                download_name='converted_chart.txt'
            )
        else:
            return render_template('index.html', output_text=output_text)
    except Exception as e:
        return render_template('index.html', output_text=f"エラー: {str(e)}")

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=8080)
