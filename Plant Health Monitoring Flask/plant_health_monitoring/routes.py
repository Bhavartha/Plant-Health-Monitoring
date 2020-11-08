from flask import jsonify, request
import base64
from io import BytesIO
from PIL import Image
import numpy as np

from plant_health_monitoring import app, models, recomender
# from plant_health_monitoring.utils import *


@app.route('/')
@app.route('/home')
def home():
    return "Plant Health Monitoring"


@app.route('/d_detector', methods=["POST"])
def d_detector():
    try:
        data = request.json
        plant = data.get('plant')
        img = data.get('img').split(',')[-1]
        print(models[plant])
        y_hat = models[plant][0].predict(np.array(Image.open(BytesIO(base64.b64decode(img))))[:,:,:3].reshape(-1,28,28,3))[0]
        print(y_hat)
        if len(y_hat) > 1:
            y_hat = np.argmax(y_hat)
        else:
            y_hat = round(y_hat[0])
        print(y_hat)
        _ = models[plant][y_hat+1]
        return jsonify({'msg': _[0],'treatment':_[1],'error': False})
    except:
        return jsonify({'msg': "Please provide valid data", 'error': True})

@app.route("/recommend",methods=["POST"])
def recommend():
    try:
        data = request.json.get('data')
        count = request.json.get('count')
        # print(type(data),data[0])
        y_hat = recomender.recomend(data,count)
        # print(y_hat)
        return jsonify({'msg': list(y_hat),'error': False})
    except Exception as e:
        print(e)
        return jsonify({'msg': "Please provide valid data", 'error': True})
