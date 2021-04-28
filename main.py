# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python38_app]
# [START gae_python3_app]
from flask import Flask, render_template, request, redirect, url_for, flash
# Form imports
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from werkzeug.utils import secure_filename
import pathlib
import textwrap
import requests
import random
import string
from io import BytesIO
import mimetypes

import os, shutil
# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.config["IMAGE_UPLOADS"] = './images'
MAX_W, MAX_H = 200, 200


class MyForm(FlaskForm):
    name = StringField('Meme Text:', validators=[DataRequired()])

class UploadForm(FlaskForm):
    upload = FileField('image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def main():
    """Return a friendly HTTP greeting."""
    return render_template('index.html')

@app.route('/imageUpload')
def upload_form():
    return render_template('upload.html')

@app.route('/urlUpload')
def urlUpload():
    return render_template('urlUpload.html')

@app.route('/textUpload', methods=["GET", "POST"])
def uploadText():
    tmp1 = request.form.get("Memetext1")
    f1 = open("inputTexts/upperText.txt", "w")
    f1.write(tmp1)

    tmp2 = request.form.get("Memetext2")
    f2 = open("inputTexts/lowerText.txt", "w")
    f2.write(tmp2)

    return "Both texts have been taken successfully, time to get the image!"

@app.route('/urlUpload', methods=["GET", "POST"])
def uploadUrl():
    tmp = request.form.get("imageUrl")
    f = open("inputTexts/imageUrl.txt", "w")
    f.write(tmp)
    return "Image url has been taken successfully, submit to generate the meme!!"

@app.route('/imageUpload', methods=["GET", "POST"])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        for fl in os.listdir("static/uploads/"):
            os.remove('static/uploads/' + fl)
        #file = rotate_img('static/uploads/' + filename, 90)
        file.save(os.path.join('static/uploads/', filename))
        flash('Meme successfully generated and displayed below')

        #url = 'https://www.gstatic.com/webp/gallery/1.jpg'
        #response = requests.get(url)
        #im = Image.open(BytesIO(response.content))

        
        color = 'rgb(255, 255, 255)'  # white 
        # Split input text
        with open('inputTexts/upperText.txt', 'r') as file:
            data1 = file.read().replace('\n', '')
        with open('inputTexts/lowerText.txt', 'r') as file:
            data2 = file.read().replace('\n', '')
        
        split1 = textwrap.wrap(data1, width=35)
        split2 = textwrap.wrap(data2, width=35)
        # Load the background image
        for file in os.listdir("static/uploads/"):
            img = Image.open('static/uploads/' + file)
            break
        
        draw = ImageDraw.Draw(img)
        w1, h1 = draw.textsize(data1)
        width, height = img.size
        font = ImageFont.truetype('fonts/Arial Bold.ttf', int(height/12))

        current_h, pad = height/20, 10
        for line in split1:
            w, h = draw.textsize(line, font=font)
            draw.text(((width - w) / 2, current_h), line, font=font)
            current_h += h + pad

        current_h2, pad2 = height*4/5, 10
        for line2 in split2:
            w1, h1 = draw.textsize(line2, font=font)
            draw.text(((width - w1) / 2, current_h2), line2, font=font)
            current_h2 += h1 + pad2
        # draw the message on the background
        #draw.text((width/2, 50), data1, fill=color, font=font)
        #draw.text((width/2, height - 300), data2, fill=color, font=font)

        # save the edited image
        pathlib.Path('./').mkdir(parents=True, exist_ok=True)
        # Create unique filename for each meme generated
        timestamp = str(datetime.now()).split()[0] + str(datetime.now()).split()[1]
        # Create meme filename
        #im.save('static/uploads/image.png')
        img.save(os.path.join(img.filename))
        return render_template('upload.html', filename=filename)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/urlSubmit', methods=["GET", "POST"])
def submitURL():

        
        color = 'rgb(255, 255, 255)'  # white 
        # Split input text
        with open('inputTexts/upperText.txt', 'r') as file:
            data1 = file.read().replace('\n', '')
        with open('inputTexts/lowerText.txt', 'r') as file:
            data2 = file.read().replace('\n', '')
        with open('inputTexts/imageUrl.txt', 'r') as file:
            data3 = file.read().replace('\n', '')
        
        response = requests.get(data3)
        im = Image.open(BytesIO(response.content))
        content_type = response.headers['content-type']
        ext = mimetypes.guess_extension(content_type)

        split1 = textwrap.wrap(data1, width=35)
        split2 = textwrap.wrap(data2, width=35)
        # Load the background image

        draw = ImageDraw.Draw(im)
        w1, h1 = draw.textsize(data1)
        
        width, height = im.size
        font = ImageFont.truetype('fonts/Arial Bold.ttf', int(height/12))

        current_h, pad = height/20, 10
        for line in split1:
            w, h = draw.textsize(line, font=font)
            draw.text(((width - w) / 2, current_h), line, font=font)
            current_h += h + pad

        current_h2, pad2 = height*4/5, 10
        for line2 in split2:
            w1, h1 = draw.textsize(line2, font=font)
            draw.text(((width - w1) / 2, current_h2), line2, font=font)
            current_h2 += h1 + pad2
        # draw the message on the background
        #draw.text((width/2, 50), data1, fill=color, font=font)
        #draw.text((width/2, height - 300), data2, fill=color, font=font)

        # save the edited image
        pathlib.Path('./').mkdir(parents=True, exist_ok=True)
        # Create unique filename for each meme generated
        timestamp = str(datetime.now()).split()[0] + str(datetime.now()).split()[1]
        # Create meme filename
        #im.save('static/uploads/image.png')
        for fl in os.listdir("static/uploads/"):
            os.remove('static/uploads/' + fl)

        letters = string.ascii_lowercase
        newname =  ''.join(random.choice(letters) for i in range(10)) 
        
        im.save(os.path.join('static/uploads/' + newname + ext))

        for file in os.listdir("static/uploads/"):
            imgname = file
            break
        
        return render_template('urlUpload.html', filename=imgname)

@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python3_app]
# [END gae_python38_app]
