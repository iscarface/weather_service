from locust import HttpUser, task

class WeatherLoadTest(HttpUser):
    @task
    def test_weather(self):
        self.client.get("/weather?city=London")
