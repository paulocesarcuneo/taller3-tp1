from flask import send_from_directory
from visits import get_visits, post_visits
import os


def handle_api(request):
    if request.method == "POST":
        return post_visits(request)
    elif request.method == "GET":
        return get_visits(request)
    else:
        return ("Sorry, are you lost?", 404)


def handle_html(request):
    if request.path and request.path != "/":
        page_name = request.path[1:]
        return send_from_directory(os.path.abspath("public"), page_name)
    return ("", 301, {"Location": "/home.html"})


def site(request):
    if request.path.startswith("/api/visits"):
        return handle_api(request)
    else:
        return handle_html(request)
