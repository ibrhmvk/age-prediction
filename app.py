from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from deepface import DeepFace

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part', 400
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(filename)
        result = DeepFace.analyze(img_path=filename, actions=['age', 'gender'])
        return 'The estimated age is ' + str(result[0]['age']), 200
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
