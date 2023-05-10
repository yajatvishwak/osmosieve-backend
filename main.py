from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from flask_cors import CORS
from os.path import join, dirname, realpath
from llm import transform

app = Flask(__name__)
CORS(app)

# enable debugging mode
app.config["DEBUG"] = True

# Upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Root URL
@app.route('/')
def index():
    return "hey - Osmosieve is running!"


@app.route("/process-file", methods=['POST'])
def processFile():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(
            app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(file_path)
    return jsonify({'filename': uploaded_file.filename})


@app.route("/transform-data", methods=['POST'])
def transformData():
    request_data = request.get_json()
    filename = request_data['filename']
    command = request_data['command']
    file_path = os.path.join(
        app.config['UPLOAD_FOLDER'], filename)
    data = transform(file_path, command)
    print(data)
    return jsonify(data)


if (__name__ == "__main__"):
    app.run(port=5000, debug=True)
