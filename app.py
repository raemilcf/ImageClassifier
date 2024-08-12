
    # Load model and tokenizer
import re
import os
import torch
from ultralytics import YOLO
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request,jsonify
from pathlib import Path



app = Flask(__name__)
app.static_folder = 'static'


#dictionary with all the cancer types 
cancerTypes = {
    'A': 'Adenocarcinoma: Subtyped by IDs with "A", it is a frequently seen subcategory of non-small cell lung cancer (NSCLC) that originates in glandular cells that are usually located at the periphery of the lungs. ',
    'B': 'Small Cell Carcinoma: Labelled as "B" in the patient IDs, this is known as a progressive lung cancer, which is closely related to smoking and marks itself by the proliferation of small, round cancer cells. ',
    'E': 'Large Cell Carcinoma: Characterized by "E", it is an NSCLC variant with large and distorted cells that also has a propensity for brisk growth and is thus a treat to manage.',
    'G': 'Squamous Cell Carcinoma: This type is seen in patients with "G" ID, and it originates from squamous cells of the airways; smoking is often associated with this type.',

}


# Configure upload folder and allowed extensions
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['PREDICT_FOLDER'] = 'static/uploads/predictions'

app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# check allowed file extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def has_folder(directory, folder_name):
    folder_path = os.path.join(directory, folder_name)
    if os.path.isdir(folder_path):
        # List all files in the folder
        files = os.listdir(folder_path)
        # Check for .txt files
        return any(file.endswith('.txt') for file in files)
    return False


# Load the model
model_path = 'yolov8n_trained.pt'
model = YOLO(model_path)



@app.route("/")
def home():
    return render_template("index.html")


#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/upload_images', methods=['POST'])
def upload_images():

    if 'images' not in request.files:
        return jsonify({"error": "No files part in the request"}), 400
    
    files = request.files.getlist('images')
    
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    file_paths = []
    for file in files:
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        if file and allowed_file(file.filename):

            # Save the uploaded file temporarily
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            file_paths.append(file_path)

        # Run inference on the uploaded image
        results = model.predict(source=file_path, save=True, save_txt=True, save_conf=True, project=app.config['PREDICT_FOLDER'])
        
        # You can process the results here and return the response
        print(results[0].save_dir)
        # View results
        
        # Process results
        status = ''
        for result in results:
            print('Object containing class probabilities for classification tasks', result.verbose())
            cancerType =re.sub(r'[0-9(),]', '', result.verbose())
            print( cancerType)
            if 'no' in cancerType.lower():
                status='No Cancer Detected in the image ' + file.filename
            else:
                status ='Cancer Detected: ' +  cancerTypes.get(cancerType.strip())

        pathCancer = results[0].save_dir + '/'+ file.filename

    return  [file_path , pathCancer, status]


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=4700)
    app.run()
