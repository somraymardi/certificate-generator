from flask import Flask, render_template, request, send_file, redirect, url_for
import pdfkit, os, datetime

app = Flask(__name__)
PDFKIT_CONFIG = pdfkit.configuration(wkhtmltopdf="/app/bin/wkhtmltopdf")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        father = request.form["father"]
        address = request.form["address"]

        date = datetime.datetime.now().strftime("%d-%m-%Y")
        cert_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        rendered = render_template("certificate.html", name=name, father=father, address=address, date=date, cert_id=cert_id)
        pdf_path = f"static/{cert_id}.pdf"
        pdfkit.from_string(rendered, pdf_path, configuration=PDFKIT_CONFIG)

        return render_template("result.html", pdf=pdf_path)
    return render_template("index.html")
