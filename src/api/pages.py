from flask import Blueprint, render_template

bp = Blueprint("pages", __name__)


@bp.get("/")
def index():
    return render_template("index.html")


@bp.get("/login")
def login():
    return render_template("login.html")


@bp.get("/musicians")
def musicians_page():
    return render_template("musicians.html")


@bp.get("/concerts")
def concerts_page():
    return render_template("concerts.html")


@bp.get("/performances")
def performances_page():
    return render_template("performances.html")


@bp.get("/instruments")
def instruments_page():
    return render_template("instruments.html")
