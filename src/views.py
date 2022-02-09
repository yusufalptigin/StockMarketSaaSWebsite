from forms import RegisterForm, LoginForm
from flask import render_template, current_app, flash, request, url_for, redirect, g
from flask_login import login_user, logout_user, current_user, login_required
from database import Database
from user import get
from passlib.hash import pbkdf2_sha256 as hasher

def home_page():
    return render_template("welcome.html")

def info_page():
    return render_template("index.html")

def about_page():
    return render_template("about.html")

def adviceToUser_page():
    return render_template("adviceToUser.html")

def advice_page():
    return render_template("advice.html")

def contact_page():
    return render_template("contact.html")

def post_page():
    return render_template("post.html")


def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.data["username"]
        password = hasher.hash(form.data["password"])
        db = current_app.config["db"]
        u = db.register(username,password)
        if u is None:
            flash("Username is currently in use, please choose another")
            return redirect(url_for('register_page'))
        next_page = request.args.get("next", url_for("login_page"))
        return redirect(next_page)
    return render_template("register.html", form=form)

def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.data["username"]
        user = get(username)
        if user is not None:
            password = form.data["password"]
            print("user.password:")
            #print(user.password)
            if hasher.verify(password, user.password):
                login_user(user)
                flash("You have logged in.")
                next_page = request.args.get("next", url_for("info_page"))
                return redirect(next_page)
        flash("Invalid credentials.")
    return render_template("login.html", form=form)