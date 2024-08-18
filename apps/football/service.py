import requests
from django.conf import settings

SPORTMONKS_APIKEY = settings.SPORTMONKS_APIKEY

SPORT = "football"
API_VERSION = "v3"


class SportMonksAPIClient:
    def __init__(self):
        self.BASE_URL = f"https://api.sportmonks.com/{API_VERSION}"

    def fetch_base(self, endpoint) -> (bool, dict):
        url = self.BASE_URL + endpoint
        headers = {
            "Authorization": "{}".format(SPORTMONKS_APIKEY)
        }

        try:
            resp = requests.get(url=url, headers=headers, timeout=7)
        except (requests.ConnectionError, requests.Timeout) as e:
            return False, {"error": e}
        try:
            data = resp.json()
        except requests.JSONDecodeError as e:
            return False, {"error": e}
        return True, data

    def fetch_leagues(self, page=1, per_page=50):
        endpoint = f"/{SPORT}/leagues?page={page}&per_page={per_page}"
        return self.fetch_base(endpoint)

    def fetch_seasons(self, page=1, per_page=50):
        endpoint = f"/{SPORT}/seasons?page={page}&per_page={per_page}"
        return self.fetch_base(endpoint)

    def fetch_players(self, page=1, per_page=50):
        endpoint = f"/{SPORT}/players?page={page}&per_page={per_page}"
        endpoint += "&include=sport;country;nationality;city;position;metadata;transfers;teams"
        return self.fetch_base(endpoint)
