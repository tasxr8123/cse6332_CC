from flask import Flask
from flask import render_template
from flask import request
from PIL import Image
import csv
import pandas as pd
from PIL import Image
import base64
import io


app = Flask(__name__)

@app.route('/', methods = ["GET","POST"])
def hello_world():
    return render_template("welcomeassgn1.html")

"""""
@app.route('/user/', methods = ["POST"])
def user():
    user = request.form["name"]
    df = pd.read_csv("people.csv")
    state = df[df["Name"]==user]["State"].values[0] 

    return render_template('user.html',user=user,state=state)
"""
@app.route('/user', methods = ["POST"])
def user():
    name = request.form["name"]
    df = pd.read_csv("people.csv")
    pdict = zip(df.Name,df.Picture)
    pdict=dict(pdict)
    state = df[df["Name"]==name]["State"].values[0]
    print("{}'s state is {}".format(name,state))
    
#rint(p_dict)
    
    if name in pdict:
        photo_name = pdict[name]
        #file=open(photo_name,'rb').read()
        #file=base64.b64encode(file)
        #df1 = pd.DataFrame()
        #df1['photo_name']=[file]
        image = Image.open(photo_name)
        data=io.BytesIO()
        image.save(data,"JPEG")
        encoded_img_data = base64.b64encode(data.getvalue())
        #image.show()
    else:
        exit
    return render_template('user.html',user=name,state=state,photo_name=encoded_img_data.decode('utf-8'))      
if __name__ == "__main__":
   app.run(debug = True)
