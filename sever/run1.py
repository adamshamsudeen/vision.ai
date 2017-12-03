import os
# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done
# and send_from_directory will help us to send/show on the
# browser the file that the user just uploaded
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
import os
import time
import unicodedata
from urllib import urlretrieve
import webbrowser
import requests
import re
from mtranslate import translate
import cStringIO
from PIL import Image
from flask import jsonify
from mtranslate import translate
from hinditr import hindi
from maltr import mallu
from tamiltr import tamil


# Initialize the Flask application
app = Flask(__name__)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'images/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set([ 'jpg', 'jpeg', 'JPG'])

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
@app.route('/data', methods=['POST'])
def dat():
    filename='ad.jpg'
    data = request.form
    for k, v in data.iteritems():
        print k, len(v)
    #for i in data:
    #   print data.keys(i),len(data.values(i))
    #print data.keys
    print type(data)
    #f.write(data)
    image_data = re.sub('^data:image/.+;base64,', '', data['file']).decode('base64')
    image = Image.open(cStringIO.StringIO(image_data))
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    cmd='./ba.sh '+filename
    #testcv.image_make(filename)
    os.system(cmd)
    time.sleep(1)
    file = open('cap.txt', 'r') 
    line= file.read()
    print line

    file.close()
    a=translate(line,"ml")
    b=a.encode('utf-8').decode('utf-8')
    print b
    r = requests.post("http://210.212.237.167/tts/festival_cs.php", data={'op':b, 'Languages':'malayalam', 'Voice':'voice1', 'ex':'execute', 'ip':'', 'rate':'normal'})
    print r.status_code
    m = re.search('(\d_\d+).wav', r.text)

    url = "http://210.212.237.167/tts/wav_output/fest_out"+m.group(1)+".wav"+"$"+line+"\n"+b
    print url

    strn="http://audio.prokerala.com/downloads/ringtones/files/mp3/sony-ericsson-28128.mp3"
    #return jsonify({"result":url})
    return url 

    # Get the name of the uploaded file


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    checked=request.form['option']
    print type(file)
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        print filename
      #  cmd='./ba.sh '+filename
        #testcv.image_make(filename)
        '''
        os.system(cmd)
        time.sleep(1)
        file = open('cap.txt', 'r') 
        line= file.read()
        file.close()'''
        line=image_desc(filename)

        if checked=='malayalam':
            url=mallu(line)
        elif checked=='hindi':
            url=hindi(line)
        elif checked=='tamil':
            url=tamil(line)

        #return url
        return redirect(url, code=302)



        #return redirect(url_for('uploaded_file',
         #                       filename=filename))

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
    app.run(
        host="127.0.0.1",
        port=int("5000"),
        debug=True
    )

