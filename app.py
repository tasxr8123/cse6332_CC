from flask import Flask
from flask import render_template
from flask import request
from PIL import Image
import csv
import pandas as pd


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
@app.route('/user/', methods = ["POST"])
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
        image = Image.open(photo_name)
        image.show()
    else:
        exit
    return render_template('user.html',user=name,state=state)


      
if __name__ == "__main__":
   app.run(debug = True)
