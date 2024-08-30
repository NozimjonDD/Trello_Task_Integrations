import requests
from django.conf import settings

SPORTMONKS_APIKEY = settings.SPORTMONKS_APIKEY

SPORT = "football"
API_VERSION = "v3"
TIMEZONE = settings.TIME_ZONE


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

    def fetch_types(self, page=1, per_page=50):
        endpoint = f"/core/types?page={page}&per_page={per_page}&timezone={TIMEZONE}"
        return self.fetch_base(endpoint)

    def fetch_leagues(self, page=1, per_page=50):
        endpoint = f"/{SPORT}/leagues?page={page}&per_page={per_page}&timezone={TIMEZONE}"
        return self.fetch_base(endpoint)

    def fetch_seasons_by_league(self, league_id, page=1, per_page=50):
        endpoint = f"/{SPORT}/seasons?page={page}&per_page={per_page}&filter=seasonLeagues:{league_id}"
        endpoint += f"&timezone={TIMEZONE}"
        return self.fetch_base(endpoint)

    def fetch_rounds_by_season(self, season_id):
        endpoint = f"/{SPORT}/rounds/seasons/{season_id}?timezone={TIMEZONE}"
        return self.fetch_base(endpoint)

    def fetch_clubs_by_season(self, season_id):
        endpoint = f"/{SPORT}/teams/seasons/{season_id}"
        endpoint += f"?include=players&timezone={TIMEZONE}"
        return self.fetch_base(endpoint)

    def fetch_fixtures_by_season(self, season_id, page=1, per_page=50):
        endpoint = f"/{SPORT}/fixtures?page={page}&per_page={per_page}"
        endpoint += f"&include=participants;state;aggregate;scores;events;statistics;lineups"
        endpoint += f"&filter=fixtureSeasons:{season_id}&timezone={TIMEZONE}"
        return self.fetch_base(endpoint)

    def fetch_fixture_by_id(self, fixture_id):
        endpoint = f"/{SPORT}/fixtures/{fixture_id}"
        endpoint += "?include=participants;state;aggregate;scores;events;statistics;lineups"
        endpoint += f"&timezone={TIMEZONE}"
        return self.fetch_base(endpoint)

    def fetch_club_by_id(self, club_id):
        endpoint = f"/{SPORT}/teams/{club_id}"
        endpoint += f"?include=sport;country;venue;upcoming;latest;players.position&timezone={TIMEZONE}"
        return self.fetch_base(endpoint)

    def fetch_players(self, page=1, per_page=50):
        endpoint = f"/{SPORT}/players?page={page}&per_page={per_page}"
        endpoint += f"&include=sport;country;nationality;city;position;metadata;transfers;teams&timezone={TIMEZONE}"
        return self.fetch_base(endpoint)

    def fetch_fixture_states(self, page=1, per_page=50):
        endpoint = f"/{SPORT}/states?page={page}&per_page={per_page}&timezone={TIMEZONE}"
        return self.fetch_base(endpoint)


class PremierLeagueAPIClient:
    def __init__(self):
        self.BASE_URL = f"https://fantasy.premierleague.com/api"

    def fetch_base(self, endpoint) -> (bool, dict):
        url = self.BASE_URL + endpoint

        try:
            resp = requests.get(url=url, timeout=20)
        except (requests.ConnectionError, requests.Timeout) as e:
            return False, {"error": e}
        try:
            data = resp.json()
        except requests.JSONDecodeError as e:
            return False, {"error": e}
        return True, data

    def fetch_statistics(self):
        endpoint = f"/bootstrap-static/"
        return self.fetch_base(endpoint)
