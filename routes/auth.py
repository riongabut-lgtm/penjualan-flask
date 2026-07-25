from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required

from models import User
from extensions import db

auth = Blueprint(
    "auth",
    __name__
    )
@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(
            username=username
        ).first()

        if user and user.check_password(password):

            login_user(user)

            flash("Login berhasil. Selamat datang!", "success")

            return redirect(
                url_for("dashboard")
            )

        flash("Username atau password salah!", "danger")

    return render_template("login.html")


@auth.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(
        url_for("auth.login")
    )