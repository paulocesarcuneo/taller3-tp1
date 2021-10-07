def api(request):
    import visits
    import publish

    page_name = request.path.split("/visits/")[-1]
    if request.method == "POST":
        return publish.post_visits(page_name)
    elif request.method == "GET":
        return visits.get_visits(page_name)
    else:
        return ("Sorry, are you lost?", 404)


def static(request):
    from flask import send_from_directory
    import os

    if request.path and request.path != "/":
        page_name = request.path[1:]
        return send_from_directory(os.path.abspath("public"), page_name)
    return ("", 301, {"Location": "/home.html"})


def site(request):
    if request.path.startswith("/api/visits"):
        return api(request)
    else:
        return static(request)


def inc_visits(event, context):
    import base64
    import visits

    page_name = base64.b64decode(event["data"]).decode("utf-8")
    visits.inc_visits(page_name)
