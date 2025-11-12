from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        try:
            # ファイルまたはテキストからJSON読み込み
            if "json_file" in request.files and request.files["json_file"].filename != "":
                data = json.load(request.files["json_file"])
            else:
                data = json.loads(request.form["json_text"])

            result_lines = []

            # sectionNotesをすべて処理
            for section in data.get("song", {}).get("notes", []):
                for note in section.get("sectionNotes", []):
                    time = note[0]
                    note_type = int(note[1])
                    hold = note[2] if len(note) > 2 else 0
                    result_lines.append(f"{{{time}}}: {{{note_type}}}: {{}}: {{{hold}}}")

            result = "\n".join(result_lines)

        except Exception as e:
            result = f"変換エラー: {e}"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
