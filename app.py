
from flask import Flask, render_template, request, send_file
from weasyprint import HTML
import tempfile
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/generate', methods=['POST'])
def generate():
    name = request.form['name']
    course = request.form['course']

    html_content = render_template('certificate.html', name=name, course=course)

    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as pdf_file:
        HTML(string=html_content).write_pdf(pdf_file.name)
        return send_file(pdf_file.name, as_attachment=True, download_name='certificate.pdf')

if __name__ == '__main__':
    app.run(debug=True)
