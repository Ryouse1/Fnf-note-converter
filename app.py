from flask import Flask, render_template, request, send_file
import json
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    if request.method == 'POST':
        try:
            raw_json = request.form['chart']
            data = json.loads(raw_json)
            text_data = convert_fnf_chart(data)
            
            # テキストをメモリ上に保存
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
            result = f"Error: {e}"
    return render_template('index.html', result=result)

def convert_fnf_chart(data):
    output = []
    for section in data["song"]["notes"]:
        bpm = section.get("bpm", 120)
        step_to_seconds = (60 / bpm) / 4  # 1ステップ = 1/4拍

        for note in section["sectionNotes"]:
            time = note[0]
            note_type = note[1]
            sustain = note[2] if len(note) > 2 and note[2] != 0 else None
            extra = note[-1] if len(note) > 3 else 0

            start_sec = time * step_to_seconds
            sustain_sec = sustain * step_to_seconds if sustain else None

            if sustain_sec:
                line = f"{{{start_sec:.3f}}}: {{{note_type}}}: {{{sustain_sec:.3f}}}: {{{extra}}}"
            else:
                line = f"{{{start_sec:.3f}}}: {{{note_type}}}: {{}}: {{{extra}}}"
            output.append(line)
    return "\n".join(output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
