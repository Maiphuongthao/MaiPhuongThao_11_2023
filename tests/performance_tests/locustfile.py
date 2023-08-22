from locust import HttpUser, task

class ProjectPerfTest(HttpUser):
    @task
    def home(self):
        self.client.get("")
    
    @task
    def points(self):
        self.client.get("points")

    @task
    def showSummary(self):
        with self.client.post("showSummary", {"email":"kate@shelifts.co.uk"}, catch_response=True) as response:
            if b"Welcome, kate@shelifts.co.uk" not in response.content:
                response.failure("Got wrong email")
            elif response.elapsed.total_seconds() > 5:
                response.failure("Request took too long")

    @task
    def purchasePlaces(self):
        club = "She Lifts"
        competition = "Spring Festival"
        with self.client.post("purchasePlaces", {"competition":competition, "club":club, "places":1}, catch_response=True) as response:
            if response.elapsed.total_seconds() > 2:
                response.failure("Request took too long")


    @task
    def logout(self):
        self.client.get("logout")