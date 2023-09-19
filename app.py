from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from deepface import DeepFace

app = Flask(__name__)


@app.route('/age', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part', 400
        file = request.files['file']
        # If the user does not select a file, the browser might
        # submit an empty file without a filename.
        if file.filename == '':
            return 'No selected file', 400
        filename = secure_filename(file.filename)
        file.save(filename)
        try:
            result = DeepFace.analyze(img_path=filename, actions=[
                                      'age', 'gender'], detector_backend='retinaface')
            return 'This is a ' + str(result[0]["dominant_gender"]) + ' and the age is ' + str(result[0]["age"]), 200
        except Exception as e:
            return str(e), 400
    return render_template('index.html')


@app.route('/compare', methods=['GET', 'POST'])
def compare_faces():
    if request.method == 'POST':
        # Check if the post request has the file parts
        if 'file1' not in request.files or 'file2' not in request.files:
            return 'No file part', 400
        file1 = request.files['file1']
        file2 = request.files['file2']
        # If the user does not select a file, the browser might
        # submit an empty file without a filename.
        if file1.filename == '' or file2.filename == '':
            return 'No selected file', 400
        filename1 = secure_filename(file1.filename)
        file1.save(filename1)
        filename2 = secure_filename(file2.filename)
        file2.save(filename2)
        try:
            result = DeepFace.verify(
                filename1, filename2, model_name="Facenet", detector_backend='retinaface')
            if result['verified']:
                return 'The images are of the same person', 200
            else:
                return 'The images are of different people', 200
        except Exception as e:
            return str(e), 400
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
