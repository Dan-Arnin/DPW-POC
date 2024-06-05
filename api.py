from ai_formatter.format_main import format_changer
from flask import Flask, request, jsonify, render_template
from Extractor import extract_data_from_pdf
import base64
import json

app = Flask(__name__)


@app.route("/")
def init():
    return render_template("index.html")


@app.route("/api/conneqtion/upload", methods=["POST"])
def upload_file():
    # check if the post request has the file part
    if "file" not in request.json:
        return jsonify({"error": "No file part in JSON payload"})
    # Decode the base64 encoded PDF data
    try:
        pdf_data = base64.b64decode(request.json["file"])
        # Call the extraction function
        extracted_data = extract_data_from_pdf(pdf_data)
        if len(extracted_data.keys()) <= 2:
            return jsonify(
                {"error": "No data extracted from PDF. Please Provide a Digital PDF"}
            )
        return json.dumps(extracted_data)
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/api/conneqtion/ai/updater", methods=["POST"])
def change_data():
    data = request.json
    try:
        print(type(data))
        requested_delivery_date, need_identification_date, actual_or_estimated = (
            format_changer(
                data["requested_delivery_date"],
                data["need_identification_date"],
                data["actual_or_estimated"],
            )
        )
        return {
            "requested_delivery_date": requested_delivery_date,
            "need_identification_date": need_identification_date,
            "actual_or_estimated": data["actual_or_estimated"] ,
            "updated_actual_or_estimated": actual_or_estimated,
        }
    except Exception as e:
        print(e)
        return {"warning": "Issue a proper format please"}


if __name__ == "__main__":
    app.run(debug=True)
