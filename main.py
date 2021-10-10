import time


def api(request):
    import visits
    import publish

    start = time.process_time()
    page_name = request.path.split("/visits/")[-1]

    result = ("Sorry, are you lost?", 404)
    if request.method == "POST":
        result = publish.post_visits(page_name)
    elif request.method == "GET":
        result = visits.get_visits(page_name)

    delta = time.process_time() - start
    print("api", delta, page_name, request.method)
    return result


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
    elif request.path.startswith("/config"):
        return config(request)
    else:
        return static(request)


def inc_visits(event, context):
    import base64
    import visits

    start = time.process_time()

    page_name = base64.b64decode(event["data"]).decode("utf-8")
    visits.inc_visits(page_name)

    delta = time.process_time() - start
    print("inc_visits", delta, page_name)


def config(request):
    import visits

    visits.init_visits(int(request.args["shards"]))
    return "Ok"
