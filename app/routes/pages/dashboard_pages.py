"""
Dashboard Page Routes
Serves HTML pages for dashboard views
"""
from flask import Blueprint, render_template

dashboard_pages_bp = Blueprint("dashboard_pages", __name__)


@dashboard_pages_bp.route("/dashboard", methods=["GET"])
def dashboard():
    """Render dashboard page"""
    return render_template("dashboard.html")

