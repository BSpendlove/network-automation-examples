from flask import Blueprint, render_template
from functions import dbfunctions

bp = Blueprint("index", __name__, url_prefix="/")

@bp.route("", methods=["GET"])
def main():
    total_users = len(dbfunctions.get_users())
    total_devices = len(dbfunctions.get_devices())
    return render_template("main.html", total_users=total_users, total_devices=total_devices)