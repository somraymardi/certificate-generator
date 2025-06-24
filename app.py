from flask import Flask, render_template, request, send_file, redirect, url_for
import pdfkit, os, datetime

app = Flask(__name__)

@app.route("/")
def index():
    today = datetime.date.today().isoformat()
    return render_template("index.html", today=today)

@app.route("/generate", methods=["POST"])
def generate():
    data = {k: request.form[k] for k in ["name","father","addr","thana","district","req_no","date"]}
    rendered = render_template("certificate.html", **data)
    filename = f"certificate_{data['req_no']}.pdf"
    path = os.path.join("static", filename)
    pdfkit.from_string(rendered, path)
    return redirect(url_for("result", file=filename))

@app.route("/result")
def result():
    f = request.args.get("file")
    return render_template("result.html", file=f)

@app.route("/download/<file>")
def download(file):
    return send_file(os.path.join("static", file), as_attachment=True)

if __name__ == "__main__":
    app.run()
