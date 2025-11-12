from flask import Flask, render_template, request, send_file
import json
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            raw_json = request.form['chart']
            data = json.loads(raw_json)
            text_data = convert_fnf_chart(data)
            
            # TXTファイルとして返す
            buffer = io.BytesIO()
            buffer.write(text_data.encode('utf-8'))
            buffer.seek(0)
            return send_file(
                buffer,
                as_attachment=True,
                download_name='converted_notes.txt',
                mimetype='text/plain'
            )
        except Exception as e:
            return render_template('index.html', result=f"❌ Error: {e}")

    return render_template('index.html', result="")

def convert_fnf_chart(data):
    output = []
    song_data = data.get("song", {})
    global_bpm = song_data.get("bpm", 120)  # 全体BPM（もし個別セクションにない場合）
    current_bpm = global_bpm
    current_offset = 0.0  # BPM変更のたびに累積するオフセット（秒）

    for section in song_data.get("notes", []):
        # BPM変更がある場合
        if section.get("changeBPM", False):
            current_bpm = section.get("bpm", global_bpm)
        step_to_sec = (60 / current_bpm) / 4  # 1ステップ＝1/4拍

        # 各ノーツ処理
        for note in section.get("sectionNotes", []):
            time = note[0]
            note_type = note[1]
            sustain = note[2] if len(note) > 2 and note[2] != 0 else None
            extra = note[-1] if len(note) > 3 else 0

            start_sec = current_offset + time * step_to_sec
            sustain_sec = sustain * step_to_sec if sustain else None

            if sustain_sec:
                line = f"{{{start_sec:.3f}}}: {{{note_type}}}: {{{sustain_sec:.3f}}}: {{{extra}}}"
            else:
                line = f"{{{start_sec:.3f}}}: {{{note_type}}}: {{}}: {{{extra}}}"
            output.append(line)

        # セクション終了後、累積オフセットを加算
        section_length = section.get("lengthInSteps", 16)
        current_offset += section_length * step_to_sec

    return "\n".join(output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
