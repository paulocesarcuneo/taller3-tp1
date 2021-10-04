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
    page_name = (
        request.path[1:] if request.path and request.path != "/" else "home.html"
    )
    return send_from_directory(os.path.abspath("public"), page_name)


def site(request):
    if request.path.startswith("/api/visits"):
        return handle_api(request)
    else:
        return handle_html(request)
