from flask import Flask, render_template,request,session, redirect, url_for
from pymongo import MongoClient


app = Flask(__name__)

app.secret_key = "hello"

seq1 = ['start']

#myclient = pymongo.MongoClient("mongodb+srv://cluster0.j2pzr.mongodb.net/img")
#mydb =myclient['img']


myclient = MongoClient("mongodb+srv://abc123:21Keerthana@cluster0.j2pzr.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient.test


@app.route("/",methods=["POST","GET"])
def index():
    if request.method == "POST":
        sym = request.form["auth"]
        print(sym)
        if sym == "admin":
            return redirect(url_for("admin"))
        else:
            return redirect(url_for("voter"))
    else:
        return render_template("index.html")

@app.route("/admin", methods=["POST","GET"])
def admin():
    if request.method == "POST":
        usr = request.form["uname"]
        pas = request.form['psw']
        if usr=="abc" and pas=="1234":
            return redirect(url_for("adminauth"))
        return render_template("admin.html",x="1")
    return render_template("admin.html",x="0")

@app.route("/adminauth",methods=["POST","GET"])
def adminauth():
    with myclient:
        docs = mydb["registered"].find()
        emails = []
        keys = []
        for i in docs:
            emails.append(list(i.keys())[1])
            keys.append(list(i.values())[1])
        print(emails)    
        print(keys)
        polls = mydb["polls"].find()
        pols = []
        for i in polls:
            pols.append(list(i.values())[1][0])
        print(pols)
    if request.method == "POST":
        poll = request.form["poll"]
        vis = request.form["vis"]
        datef = request.form["datefrom"]
        datet = request.form["datetill"]
        print(poll,vis,datef,datet)
        mycol=mycol=mydb['polls']
        mydict={}
        mydict['x']=[poll,vis,datef,datet]
        if poll not in pols:
            mycol.insert_one(mydict)
        print(poll)
        if vis=="logout":
            return redirect(url_for("admin"))        
    return render_template("dashboard.html",emails=emails,keys=keys,x=len(emails),y=len(keys[0]),polls=pols,p=len(pols))

@app.route("/show", methods=["POST","GET"])
def show():
    with myclient:
        docs = mydb["candidates"].find()
        cans = []
        cansp = []
        for i in docs:
            cans.append(list(i.values())[1][0])
            cansp.append(list(i.values())[1][1])
        print(cans)
    return render_template("show.html",cans=cans,cansp=cansp,x=len(cansp))


@app.route("/results", methods=["POST","GET"])
def result():
    with myclient:
        docs = mydb["candidates"].find()
        docs1 = mydb["results"].find()
        res = []
        cans = []
        cansp = []
        for i in docs:
            cans.append(list(i.values())[1][0])
            cansp.append(list(i.values())[1][1])
        for i in docs1:
            res.append(list(i.values())[1])
        print(res)
        print(cans)
    return render_template("results.html",cans=cans,cansp=cansp,x=len(cansp),res=res)     

@app.route("/voter", methods=["POST","GET"])
def voter():
    if request.method == "POST":
        
        # load signed up details
        with myclient:
            docs = mydb["name"].find()
            emails = []
            keys = []
            for i in docs:
                emails.append(list(i.keys())[1])
                keys.append(list(i.values())[1])
            print(emails)    
            print(keys)
        # get data
        email = request.form["email"]
        psw = request.form["psw"]
        login = False
        for i in range(0,len(emails)):
            if str(email) == str(emails[i]) and str(psw) == str(keys[i]):
                login = True
        #login       
        if login:            
            return redirect(url_for('dashboard'))
        if email not in emails:
            mycol=mycol=mydb['name']
            mydict={}
            mydict[email]=psw
            mycol.insert_one(mydict)      
            return redirect(url_for('dashboard'))
        return render_template("voter.html",x=1)
    else:
        return render_template("voter.html",x=0)

@app.route("/dashboard", methods=["POST","GET"])
def dashboard():
    with myclient:
        polls = mydb["polls"].find()
        pols = []
        for i in polls:
            pols.append(list(i.values())[1][0])
        print(pols)
    if request.method == "POST":
        name = request.form["firstname"]
        address = request.form["address"]
        state = request.form["state"]
        zip1 = request.form["zip"]
        city = request.form["city"]
        idtype = request.form["idtype"]        
        print(name)
        mycol=mycol=mydb['registered']
        mydict={}
        mydict['x']=[name,address,state,zip1,city,idtype]
        mycol.insert_one(mydict)
        if vis=="logout":
            return redirect(url_for("voter"))        
        return render_template("voterdashboard.html",polls=pols,p=len(pols))
    else:
        return render_template("voterdashboard.html",polls=pols,p=len(pols))

@app.route("/filen", methods=["POST","GET"])
def filen():
    if request.method == "POST":
        name = request.form["firstname"]
        party = request.form["party"]
        mycol=mycol=mydb['candidates']
        mycol1=mycol1=mydb['results']
        mydict={}
        mydict1={}
        mydict['poll1']=[name,party]
        mydict1[name]=[0]
        mycol.insert_one(mydict)
        mycol1.insert_one(mydict1)
        return redirect(url_for('dashboard')) 
    return render_template("filen.html")     

@app.route("/vote", methods=["POST","GET"])
def vote():
    with myclient:
        docs = mydb["candidates"].find()
        docs1 = mydb["results"].find()
        res = []
        cans = []
        cansp = []
        for i in docs:
            cans.append(list(i.values())[1][0])
            cansp.append(list(i.values())[1][1])
        for i in docs1:
            res.append(list(i.values())[1])
        print(res)
        print(cans)
    if request.method == "POST":
        vote = int(request.form["voted"])
        mycol1= mydb['results']
        myquery = { cans[vote]: int(res[vote]) }
        newvalues = { "$set": { cans[vote]: int(res[vote])+1 } }
        mycol1.update_one(myquery,newvalues)
        print(vote)
        print("hi")
        return redirect(url_for("dashboard"))

    return render_template("vote.html",cans=cans,cansp=cansp,x =len(cans))     

@app.route("/signin", methods=["POST","GET"])
def signin():
    return render_template("signin.html")

if __name__ == '__main__':
    app.run(debug=True)
    
