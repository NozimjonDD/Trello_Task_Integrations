from django.db import transaction

from . import service, models


def update_leagues():
    page = 1
    has_more = True

    while has_more:
        success, resp_data = service.SportMonksAPIClient().fetch_leagues(page=page, per_page=50)

        if not success:
            break

        leagues_data = resp_data["data"]

        with transaction.atomic():

            for league in leagues_data:
                models.League.objects.update_or_create(
                    remote_id=league["id"],
                    defaults={
                        "name": league["name"],
                        "short_code": league["short_code"],
                        "image_path": league["image_path"],
                        "type": league["type"],
                        "sub_type": league["sub_type"],
                        "category_id": league["category"],
                        "has_jerseys": league["has_jerseys"],
                        "is_active": league["active"],
                    }
                )

        has_more = resp_data["pagination"]["has_more"]
        page += 1


def update_seasons():
    page = 1
    has_more = True

    while has_more:
        success, resp_data = service.SportMonksAPIClient().fetch_seasons(page=page, per_page=50)

        if not success:
            break

        seasons_data = resp_data["data"]

        with transaction.atomic():

            for season in seasons_data:
                models.Season.objects.update_or_create(
                    remote_id=season["id"],
                    defaults={
                        "league": models.League.objects.get(remote_id=season["league_id"]),
                        "name": season["name"],
                        "is_finished": season["finished"],
                        "pending": season["pending"],
                        "is_current": season["is_current"],
                        "starting_at": season["starting_at"],
                        "ending_at": season["ending_at"],
                        "games_in_current_week": season["games_in_current_week"],
                    }
                )

        has_more = resp_data["pagination"]["has_more"]
        page += 1


def update_players():
    page = 1
    has_more = True

    while has_more:
        success, resp_data = service.SportMonksAPIClient().fetch_players(page=page, per_page=50)

        if not success:
            break

        players_data = resp_data["data"]

        with transaction.atomic():

            for player in players_data:
                models.Player.objects.update_or_create(
                    remote_id=player["id"],
                    defaults={
                        "country_id": player["country_id"],
                        "nationality_id": player["nationality_id"],
                        "profile_picture_path": player["image_path"],
                        "first_name": player["firstname"],
                        "last_name": player["lastname"],
                        "full_name": player["name"],
                        "common_name": player["common_name"],
                        "date_of_birth": player["date_of_birth"],
                        "gender": player["gender"],
                        "height": player["height"],
                        "weight": player["weight"],
                    }
                )

        has_more = resp_data["pagination"]["has_more"]
        page += 1
