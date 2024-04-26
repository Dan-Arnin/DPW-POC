from flask import Flask, request, jsonify,render_template
from Extractor import extract_data_from_pdf
import base64
import json

app = Flask(__name__)
@app.route('/')
def init():
    return render_template("index.html")

@app.route('/api/conneqtion/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.json:
        return jsonify({'error': 'No file part in JSON payload'})
    # Decode the base64 encoded PDF data
    try:
        pdf_data = base64.b64decode(request.json['file'])
        # Call the extraction function
        extracted_data = extract_data_from_pdf(pdf_data)
        if (len(extracted_data.keys()) <= 2):
            return jsonify({'error': 'No data extracted from PDF. Please Provide a Digital PDF'})
        return json.dumps(extracted_data)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
