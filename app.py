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

app.config.from_pyfile('config.py')
account = app.config['ACCOUNT_NAME']   # Azure account name
key = app.config['ACCOUNT_KEY']      # Azure Storage account access key  
connect_str = app.config['CONNECTION_STRING']
container = app.config['CONTAINER'] # Container name
allowed_ext = app.config['ALLOWED_EXTENSIONS'] # List of accepted extensions


blob_service_client = BlobServiceClient.from_connection_string(connect_str)

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
        return render_template('not_found.html')

@app.route('/salary', methods = ["POST"])
def salary():
    df_op = pd.DataFrame()
    photo_list = []
    sal = request.form["salary"]
    print(sal)
    df = pd.read_csv("people.csv")

    #df['Salary'] = df['Salary'].fillna(0)
    #df['Salary'] = df[~df['Salary']].isnull()
    #df['Salary'] = df[df['Salary'].str.isnumeric()]
    #df[['Salary']] = df[['Salary']].astype(int)
    df_op['Name'] = df.loc[df['Salary'] > sal, 'Name']
    df_op['Salary'] = df.loc[df['Salary'] >sal, 'Salary']
    df_op['Picture'] = df.loc[df['Salary'] > sal, 'Picture']

    for p in df_op['Picture']:
        N = ' '
        if p == N:
            p = "No Image"
        else:
            image = Image.open(p)
            data=io.BytesIO()
            image.save(data,"JPEG")
            enc_img = base64.b64encode(data.getvalue())
            #df_op['Picture_new']=enc_img.decode('UTF-8')
            enc_img = base64.b64encode(data.getvalue())
            return render_template('salary.html', tables=[df_op.to_html()], titles=['Name','Salary','Picture'],photo_list = enc_img.decode('UTF-8'))


@app.route('/upload', methods = ["GET","POST"])
def upload():
    if request.method == 'POST':
        img = request.files['file']
        #if img and allowed_file(img.filename):
        filename = secure_filename(img.filename)
        img.save(filename)
        blob_client = blob_service_client.get_blob_client(container = container, blob = filename)
        with open(filename, "rb") as data:
                try:
                    blob_client.upload_blob(data, overwrite=True)
                    #msg = "Upload Done ! "
                except:
                    pass
        #os.remove(filename)
    return render_template("index.html")

@app.route('/keywords', methods = ["GET", "POST"])
def get_keywords():
    return render_template('keywords.html')

@app.route('/keywords_show', methods = ["POST"])
def keywords_show():
    name = request.form["name"]
    df = pd.read_csv("people.csv")
    words = df[df["Name"]==name]["Keywords"].values
    return render_template('keywords_show.html',name=name, words=words)

@app.route(('/update'),methods = ["GET","POST"])
def update():
    name = request.form["name"]
    kw = request.form["text"]
    df = pd.read_csv("people.csv")
    if kw is None:
        return render_template('welcomeassign1.html')
    else:
        df['Keywords'] = kw
        msg = kw
        df.to_csv ("people.csv", index = None, header=True)
    return render_template("update.html",name=name,tables = [df.to_html()],msg=msg)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
