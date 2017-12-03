import base64
import datetime
import os
import re
import requests
import face_recognition
from englishtts import english
from io import BytesIO
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from hinditr import hindi
from maltr import mallu
from mtranslate import translate
from tamiltr import tamil
from vision.text import get_text
from PIL import Image
from werkzeug import secure_filename
from recognition.face import recog_face
# Initialize the Flask application
app = Flask(__name__)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'images/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set([ 'jpg', 'jpeg', 'JPG','png'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/')
def index():
    return render_template('index.html')


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    checked=request.form['option']
    print(type(file))
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        print (filename)
        cmd='./ba.sh '+filename
        os.system(cmd)
        # time.sleep(1)
        file = open('cap.txt', 'r') 
        line= file.read()
        file.close()
        print(line)

        if checked=='malayalam':
            url=mallu(line)
        elif checked=='hindi':
            url=hindi(line)
        elif checked=='english':
            url=english(line)
        elif checked=='tamil':
            url=tamil(line)

        return redirect(url, code=302)

@app.route('/data', methods=['POST'])
def dat():

    uniq_filename = str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '.')+'.jpg'

    data = request.form
    # for k, v in data.items():
    #     print (k, len(v))

    image1_data = re.sub('^data:image/.+;base64,', '', data['image'])

    image1 = Image.open(BytesIO(base64.b64decode(image1_data)))

    image1.save(os.path.join(app.config['UPLOAD_FOLDER'],uniq_filename))



    # filename='ad.jpg'
    # data = request.form
    # for k, v in data.iteritems():
    #     print k, len(v)
    # #for i in data:
    # #   print data.keys(i),len(data.values(i))
    # #print data.keys
    # print type(data)
    # #f.write(data)
    # image_data = re.sub('^data:image/.+;base64,', '', data['file']).decode('base64')
    # image = Image.open(cStringIO.StringIO(image_data))
    # image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    cmd='./ba.sh '+uniq_filename
    #testcv.image_make(filename)
    os.system(cmd)
    # time.sleep(1)
    file = open('cap.txt', 'r') 
    line= file.read()
    # print line

    file.close()
    a=translate(line,"ml")
    b=a.encode('utf-8').decode('utf-8')
    # print b
    r = requests.post("http://210.212.237.167/tts/festival_cs.php", data={'op':b, 'Languages':'malayalam', 'Voice':'voice1', 'ex':'execute', 'ip':'', 'rate':'normal'})
    print(r.status_code)
    m = re.search('(\d_\d+).wav', r.text)

    url = "http://210.212.237.167/tts/wav_output/fest_out"+m.group(1)+".wav"
    print (url)

    #return jsonify({"result":url})
    return url 

@app.route('/face', methods=['POST'])
def face():

    uniq_filename = str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '.')+'.jpg'

    data = request.form
    # for k, v in data.items():
    #     print (k, len(v))

    image1_data = re.sub('^data:image/.+;base64,', '', data['image'])

    image1 = Image.open(BytesIO(base64.b64decode(image1_data)))

    image1.save(os.path.join(app.config['UPLOAD_FOLDER'],uniq_filename))
    # unknown_image = face_recognition.load_image_file("/images/"+uniq_filename)
    # unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
    # uniq_filename='adam.jpg'
    name=recog_face(uniq_filename)
    return name


@app.route('/text', methods=['POST'])
def text():
    uniq_filename = str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '.')+'.jpg'

    data = request.form
    # for k, v in data.items():
    #     print (k, len(v))

    image1_data = re.sub('^data:image/.+;base64,', '', data['image'])

    image1 = Image.open(BytesIO(base64.b64decode(image1_data)))

    image1.save(os.path.join(app.config['UPLOAD_FOLDER'],uniq_filename))

    label=get_text(uniq_filename)
    print(label)
    url=english(label)
    return url



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("4000"),
        debug=True,
        threaded=True
    )
