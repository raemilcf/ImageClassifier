
    # Load model and tokenizer
import tensorflow as tf
from transformers import TFBartForConditionalGeneration
import pickle
import re
from utils import util

import os
from werkzeug.utils import secure_filename

from flask import Flask, render_template, request,jsonify

app = Flask(__name__)
app.static_folder = 'static'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["GET"])
def getSumarization():
    userText = request.args.get('fullText')
    minWords = request.args.get('minWords')
    maxWords = request.args.get('maxWords')
    # if minWords == '':
    #     minWords=40

    # if maxWords =='':
    #     maxWords=100
    



    # #get summary 
    # result =  getSummary(userText, int(minWords), int(maxWords))

   
    return userText

#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/upload_images', methods=['POST'])
def upload_images():
    if 'images' not in request.files:
        return jsonify({"error": "No files part in the request"}), 400
    
    files = request.files.getlist('images')
    
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    file_paths = []
    for file in files:
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # Save the file
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        file_paths.append(file_path)
    
    return jsonify({"message": "Files successfully uploaded", "file_paths": file_paths}), 200


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=4700)
    app.run()
