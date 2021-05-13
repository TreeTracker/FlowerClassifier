from flask import Flask, render_template, request, redirect, url_for
import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import os


app = Flask(__name__)

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

finalPrediction = 0
global answer


def classification(fileName):
    np.set_printoptions(suppress=True)
    model = tensorflow.keras.models.load_model('./model/keras_model.h5')
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    image = Image.open(fileName)

    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)
    image_array = np.asarray(image)

    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array

    prediction = model.predict(data)
    try:
        os.remove(fileName)
        print('Sucess')
    except:
        print('Fail')
    finalPrediction = {}

    strPrediction = str(prediction)
    strPrediction = strPrediction.replace('[','')
    strPrediction = strPrediction.replace(']','')

    Daisy = ""
    Dandelion = ""
    Rose = ""
    Sunflower = ""
    Tulip = ""

    strLen = len(strPrediction)
    count = 0
    x = 0
    for x in range(0,strLen-4):
        if strPrediction[x] == " " and strPrediction[x+1] != " ":
            count += 1
        if count == 0:
            Daisy += strPrediction[x]
        elif count == 1:
            Dandelion += strPrediction[x]
        elif count == 2:
            Rose += strPrediction[x]
        elif count == 3:
            Sunflower += strPrediction[x]
        else:
            Tulip += strPrediction[x]

    finalPrediction["Daisy"] = str(round(float(Daisy.strip()),5) * 100 ) + "%"
    finalPrediction["Dandelion"] = str(round(float(Dandelion.strip()),5) * 100) + "%"
    finalPrediction["Rose"] = str(round(float(Rose.strip()),5) * 100) + "%"
    finalPrediction["Sunflower"] = str(round(float(Sunflower.strip()),5) * 100) + "%"
    finalPrediction["Tulip"] = str(round(float(Tulip.strip()),5) * 100) + "%"

    print(finalPrediction)
    return finalPrediction

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result/<filename>')
def result(filename):
    result = classification(filename)
    # return render_template('result.html',result = answer)
    return render_template('result.html', result = result)

@app.route('/loading')
def loading():
    return render_template('loading.html')

@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']

    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)
        # result = classification(uploaded_file.filename)
        file = uploaded_file.filename

    return redirect(url_for('result',filename = file))

app.run(debug=True)