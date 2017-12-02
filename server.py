import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
import os
import time
import unicodedata
import webbrowser
from flask import jsonify



# Initialize the Flask application
app = Flask(__name__)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'images/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set([ 'jpg', 'jpeg', 'JPG'])

@app.route('/')
def index():
    return 'welcome'



if __name__ == '__main__':
    app.run(
        host="127.0.0.1",
        port=int("4000"),
        debug=True
    )

