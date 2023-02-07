from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from PIL import Image
import csv
import pandas as pd
from PIL import Image
import base64
import io
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from azure.storage.blob import BlobServiceClient
import os
from io import BytesIO
from IPython.display import HTML


app = Flask(__name__)
app = Flask(__name__, static_folder='static', static_url_path='')


#LAUNCH WELCOME PAGE
@app.route('/', methods = ["GET","POST"])
def hello_world():
    return render_template("welcomeassgn1.html")

#GET SALARIES

@app.route('/get_salary', methods = ["GET", "POST"])
def salary_input():
    return render_template('get_salary.html')
#DISPLAY SALARIES

@app.route('/user', methods = ["POST"])
def user():
    df = pd.read_csv("people.csv")
    name = request.form["name"]
    for i in df["Name"]:
        if i !=name:
            next
        elif i ==name:
            pdict = zip(df.Name,df.Picture)
            pdict=dict(pdict)
            state = df[df["Name"]==i]["State"].values[0]
            print("{}'s state is {}".format(i,state)) 
            photo_name = pdict[i]
            image = Image.open(photo_name)
            data=io.BytesIO()
            image.save(data,"JPEG")
            encoded_img_data = base64.b64encode(data.getvalue())
            return render_template('user.html',user=name,state=state,photo_name=encoded_img_data.decode('utf-8')) 
        return render_template('not_found.html'
        
if __name__ == "__main__":
    app.run(debug = True)

