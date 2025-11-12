from flask import Flask, render_template, request, send_file
import io
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/convert', methods=['POST'])
def convert_chart():
    file = request.files['file']
    data = json.load(file)

    output_lines = []

    for section in data["song"]["notes"]:
        bpm = section.get("bpm", 120)
        step_to_seconds = (60 / bpm) / 4  # 1 step = 1/4 beat

        for note in section["sectionNotes"]:
            time = note[0]
            note_type = note[1]
            sustain = note[2] if len(note) > 2 and note[2] != 0 else 0
            extra = note[-1] if len(note) > 3 else 0

            start_sec = round(time * step_to_seconds, 3)
            sustain_sec = round(sustain * step_to_seconds, 3) if sustain > 0 else None

            if sustain_sec:
                line = f"{{{start_sec}}}: {{{note_type}}}: {{{sustain_sec}}}: {{{extra}}}"
            else:
                line = f"{{{start_sec}}}: {{{note_type}}}: {{}}: {{{extra}}}"

            output_lines.append(line)

    txt_data = "\n".join(output_lines)
    buffer = io.BytesIO()
    buffer.write(txt_data.encode('utf-8'))
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="converted_chart.txt",
        mimetype="text/plain"
    )


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
