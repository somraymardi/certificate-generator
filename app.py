from flask import Flask, render_template, request, send_file, redirect, url_for
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import qrcode, io, os, datetime

app = Flask(__name__)
BG_PATH = "static/certificate_bg.png"  # replace with your designed background

# Text positions (pixels on A4 595x842)
NAME_POS   = (70, 585)
FATHER_POS = (70, 560)
ADDR_POS   = (70, 535)
THANA_POS  = (70, 510)
DIST_POS   = (150, 510)
REQ_POS    = (200, 640)
DATE_POS   = (200, 622)
QR_POS     = (80, 160)
QR_SIZE    = 120

FONT = "Helvetica-Bold"
FONT_SIZE = 12

def make_certificate_pdf(data):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    bg = ImageReader(BG_PATH)
    c.drawImage(bg, 0, 0, width=595, height=842)
    c.setFont(FONT, FONT_SIZE)
    c.drawString(*REQ_POS,  data["req_no"])
    c.drawString(*DATE_POS, data["date"])
    c.drawString(*NAME_POS, f"{data['name'].upper()}, पिता – {data['father'].upper()}")
    c.drawString(*ADDR_POS,  data['addr'].upper())
    c.drawString(*THANA_POS, f"थाना – {data['thana'].upper()},")
    c.drawString(*DIST_POS,  f"जिला – {data['district'].upper()}")
    qr_data = f"https://your-domain.com/verify/{data['req_no']}"
    qr_img = qrcode.make(qr_data)
    qbuf = io.BytesIO()
    qr_img.save(qbuf, format="PNG"); qbuf.seek(0)
    c.drawImage(ImageReader(qbuf), *QR_POS, width=QR_SIZE, height=QR_SIZE)
    c.showPage(); c.save(); buf.seek(0)
    return buf

@app.route("/")
def index():
    today = datetime.date.today().isoformat()
    return render_template("index.html", today=today)

@app.route("/generate", methods=["POST"])
def generate():
    data = {k: request.form[k] for k in ["name","father","addr","thana","district","req_no","date"]}
    pdf = make_certificate_pdf(data)
    filename = f"certificate_{data['req_no']}.pdf"
    path = os.path.join("static", filename)
    with open(path, "wb") as f:
        f.write(pdf.read())
    return redirect(url_for("result", file=filename))

@app.route("/result")
def result():
    f = request.args.get("file")
    return render_template("result.html", file=f)

@app.route("/download/<file>")
def download(file):
    return send_file(os.path.join("static", file), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
