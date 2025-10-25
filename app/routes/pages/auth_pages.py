"""
Authentication Page Routes
Serves HTML pages for login and signup
"""
from flask import Blueprint, render_template

auth_pages_bp = Blueprint("auth_pages", __name__)


@auth_pages_bp.route("/", methods=["GET"])
def login_page():
    """Render login page"""
    return render_template("login.html")


@auth_pages_bp.route("/signup", methods=["GET"])
def signup_page():
    """Render signup page"""
    return render_template("signup.html")

