from flask import Blueprint, render_template, request, flash, redirect, url_for
from forms import AddUser
from functions import dbfunctions

bp = Blueprint("users", __name__, url_prefix="/users")

@bp.route("", methods=["GET"])
def index():
    users = dbfunctions.get_users()
    return render_template("users/index.html", users=users)

@bp.route("/add", methods=["GET", "POST"])
def add_user():
    form = AddUser()
    if request.method == "POST":
        if form.validate_on_submit():
            user = dbfunctions.add_user(form.username.data, form.password.data)
            if user:
                flash("User {} was created.".format(user.username))
            return redirect(url_for("users.index"))

    return render_template("users/add_user.html", form=form)

@bp.route("/<int:id>/delete", methods=["DELETE"])
def delete_user(id):
    user = dbfunctions.delete_user(id)
    if not user:
        flash("User {} was not found or deleted.".format(id))
    flash("User {} was successfully deleted.")
    
    return redirect(url_for("users.index"))