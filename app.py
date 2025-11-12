from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files.get('jsonFile')
    if not file:
        return jsonify({'error': 'ファイルがありません'}), 400

    try:
        data = json.load(file)
        output = []

        song = data.get("song", {})
        bpm = song.get("bpm", 120)
        notes = song.get("notes", [])

        for section in notes:
            for note in section.get("sectionNotes", []):
                start_ms = note[0]
                note_type = note[1]
                sustain_ms = note[2] if len(note) > 2 else 0
                extra = note[3] if len(note) > 3 else 0

                # ミリ秒 → 秒変換
                time_sec = round(start_ms / 1000.0, 3)
                sustain_sec = round(sustain_ms / 1000.0, 3)

                line = f"{time_sec}: {note_type}: {sustain_sec}: {extra}"
                output.append(line)

        return jsonify({
            "bpm": bpm,
            "converted": output
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
