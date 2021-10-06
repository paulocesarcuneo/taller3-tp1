from locust import HttpUser, between, task
from pyquery import PyQuery
import time


def retry(times: int, op):
    result = None
    while times > 0:
        result = op()
        if result:
            return result
        times = times - 1
    return result


class SiteTest(HttpUser):
    wait_time = between(5, 15)
    host = "http://localhost:8080"

    retry_post = 3
    retry_get = 3
    read_time = 3

    def download_assets(self, html):
        def assets(html):
            pq = PyQuery(html)
            result = [
                link.attrib["href"] for link in pq("link") if "href" in link.attrib
            ]
            for img in pq("img"):
                if "src" in img.attrib:
                    result.append(img.attrib["src"])
            for js in pq("script"):
                if "src" in js.attrib:
                    result.append(js.attrib["src"])
            return result

        for asset in assets(html):
            self.client.get("/" + asset)

    def post_visit(self, page_name):
        def do_post_visit():
            return (
                200
                <= self.client.post(
                    "/api/visits", json={"page_name": page_name}
                ).status_code
                < 300
            )

        retry(self.retry_post, do_post_visit)

    def get_visits(self, page_name):
        def do_get_visits():
            return (
                200
                <= self.client.get(f"/api/visits?page_name={page_name}").status_code
                < 300
            )

        retry(self.retry_get, do_get_visits)

    def enter_page(self, page_name):
        html_response = self.client.get(f"/{page_name}.html")
        self.download_assets(html_response.content)
        self.post_visit(page_name)
        time.sleep(self.read_time)

    @task(1)
    def stray_user(self):
        self.enter_page("home")
        self.enter_page("about")

    @task(10)
    def jobs_seeker(self):
        self.enter_page("home")
        self.enter_page("jobs")
        self.enter_page("about")
        self.enter_page("offices")
        self.enter_page("about")
        self.enter_page("home")

    @task(10)
    def usual_user(self):
        self.enter_page("home")
        self.enter_page("about")
        self.enter_page("legals")
        self.enter_page("about")
        self.enter_page("home")
