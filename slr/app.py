from camera import VideoCamera
from flask import Flask, render_template, Response, jsonify, request
import time
from werkzeug.utils import secure_filename
import requests
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index2.html')


@app.route('/predict', methods=['POST'])
def predict_api():
    req = requests.post('http://127.0.0.1:5000/predict').json()
    list_all = []
    for data in req['data']:
        dict1 = {}
        dict1['prediction'] = data['prediction']
        dict1['time_stamp'] = time.strftime(
            '%H:%M:%S', time.localtime(int(data['time_stamp'])))
        list_all.append(dict1)
    req2 = {'sentence': req['sentence'],
            'words': list_all, 'message': req['message']}
    return jsonify({'data': req2})


def gen(camera):
    while True:
        try:
            frame = camera.get_frame()
            print(frame)
        except Exception:
            print("Video is finished or empty")
            # return None
            frame = camera.get_heartbeat()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/file/', methods=['POST'])
def file_api():
    fileStorage = request.files['file']
    file_name = secure_filename(fileStorage.filename)
    fileStorage.save('./static/video/%s' % file_name)
    req = requests.post('http://127.0.0.1:5000/predict').json()
    print(req)
    list_all = []
    for data in req['data']['words']:
        dict1 = {}
        dict1['prediction'] = data['prediction']
        dict1['time_stamp'] = data['time_stamp']
        list_all.append(dict1)
    req2 = {'sentence': req['data']['sentence'],
            'words': list_all, 'message': req['data']['message']}
    return jsonify({'data': '/static/video/%s' % file_name, 'data2': req2})



if __name__ == '__main__':
    app.run(app.run(host='0.0.0.0', threaded=True,port=8888))
