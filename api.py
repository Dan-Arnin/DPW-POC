from flask import Flask, request, jsonify,render_template
from Extractor import extract_data_from_pdf
import base64

app = Flask(__name__)

def pdf_extractor(pdf_data):

    decoded_data = base64.b64decode(pdf_data)
    return {'text': decoded_data.decode('utf-8')}
@app.route('/')
def init():
    return render_template("index.html")

@app.route('/api/conneqtion/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    # if user does not select file, browser also submit an empty part without filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        pdf_data = file.read()
        extracted_data = extract_data_from_pdf(pdf_data)
        return extracted_data

    return jsonify({'error': 'Invalid file type'})

if __name__ == '__main__':
    app.run(debug=True)
