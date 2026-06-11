from flask import Flask, render_template, redirect,url_for,request,session

from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,IntegerField,PasswordField,EmailField
from wtforms.validators import DataRequired,Email
import smtplib
from dotenv  import load_dotenv
import os
from flask_bootstrap import Bootstrap4


load_dotenv()


app = Flask(__name__)


app.config['SECRET_KEY'] = '24313413413'

boostrap=Bootstrap4(app)

class Myform(FlaskForm):
    
    name=StringField("what is your name",validators=[DataRequired() ])
    email=EmailField( "what is your email",validators=[DataRequired(),Email()])
   
    submit=SubmitField("submit")
    pasword=PasswordField("what is you password only numbers")
    


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/name/redirect")
def redirectx():
    name=session.get("name")
    epost=session.get("epost")
    return render_template("redirect.html",name=name,epost=epost)


@app.route("/name",methods=["POST","GET"])
def name():
    name=None
    epost=None
    password=None
    form=Myform()
    
    
    if form.validate_on_submit():
        name=form.name.data
        session["name"]=name
        epost=form.email.data
        session["epost"]=epost
        password=form.pasword.data
        session["password"]=password
        with open("static/data.txt","a") as selim:
            selim.write(f"name:{name} eposta:{epost} password:{password}\n")
            
        # creates SMTP session
        s = smtplib.SMTP('smtp.gmail.com', 587)
        # start TLS for security
        s.starttls()
        # Authentication
        s.login(os.getenv("email"),os.getenv("password") )
        # message to be sent
        message = f"selamın aleyküm {name}, your password is {password} do not share with anybody"
        # sending the mail
        s.sendmail(os.getenv("email"),epost,message.encode("utf-8"))
        # terminating the session
        s.quit()
        

            
        return redirect(url_for("redirectx",form=form))
    return render_template("login.html",form=form)


if __name__=="__main__":
    app.run(debug=True)


    