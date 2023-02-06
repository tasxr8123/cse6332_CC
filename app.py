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
        
 if __name__ == "__main__":
    app.run(debug = True)
