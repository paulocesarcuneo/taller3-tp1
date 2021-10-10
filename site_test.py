from locust import HttpUser, between, task, LoadTestShape
from locust.clients import HttpSession
from pyquery import PyQuery
import time
import os
import math


def retry(times: int, op):
    result = None
    while times > 0:
        result = op()
        if result:
            return result
        times = times - 1
    return result


SITE_PATH = "/site"


class Browser:
    api_request_timeout = 32
    assets_request_timeout = 32
    cache = {}
    cache_enabled = os.getenv("CACHE_ENABLED", "False") == "True"
    retry_post = 1
    retry_get = 1
    user_reading_time = 3
    client: HttpSession

    def download_page(self, page_name):
        if self.cache_enabled and self.cache[page_name]:
            return
        html_response = self.client.get(f"{SITE_PATH}/{page_name}.html")
        html = html_response.content

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
            self.client.get(
                f"{SITE_PATH}/" + asset, timeout=self.assets_request_timeout
            )

        self.cache[page_name] = True

    def post_visit(self, page_name):
        def do_post_visit():
            response = self.client.post(
                f"/api/visits/{page_name}", timeout=self.api_request_timeout
            )
            return 200 <= response.status_code < 300

        retry(self.retry_post, do_post_visit)

    def get_visits(self, page_name):
        def do_get_visits():
            response = self.client.get(
                f"/api/visits/{page_name}", timeout=self.api_request_timeout
            )
            return 200 <= response.status_code < 300

        retry(self.retry_get, do_get_visits)


class SiteTest(HttpUser, Browser):
    wait_time = between(5, 15)
    host = os.getenv("TARGET_HOST", "http://localhost:8080")

    def enter_page(self, page_name):
        self.download_page(page_name)
        self.post_visit(page_name)
        self.get_visits(page_name)
        time.sleep(self.user_reading_time)

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


class LoadShape:
    class RampUpRampDownShape(LoadTestShape):
        rampup_end = 10
        rampdown_start = 20
        rampdown_end = 30
        spawn = 5
        slope = 1

        def tick(self):
            run_time = self.get_run_time()
            print(run_time)

            if run_time < self.rampup_end:
                return (round(self.slope * run_time), self.spawn)
            elif run_time < self.rampdown_start:
                return (self.slope * self.rampdown_start, self.spawn)
            elif run_time < self.rampdown_end:
                return (
                    round(self.slope * (self.rampdown_start - run_time)),
                    self.spawn,
                )
            return None

    class StepLoadShape(LoadTestShape):
        step_time = 30
        step_load = 10
        spawn_rate = 10
        time_limit = 600

        def tick(self):
            run_time = self.get_run_time()

            if run_time > self.time_limit:
                return None

            current_step = math.floor(run_time / self.step_time) + 1
            return (current_step * self.step_load, self.spawn_rate)


class StepLoadShape(LoadTestShape):
    step_time = 30
    step_load = 10
    spawn_rate = 10
    time_limit = 10000

    def tick(self):
        run_time = self.get_run_time()

        if run_time > self.time_limit:
            return None

        current_step = math.floor(run_time / self.step_time) + 1
        return (current_step * self.step_load, self.spawn_rate)
