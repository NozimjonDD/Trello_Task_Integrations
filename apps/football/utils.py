from django.db import transaction

from . import service, models


def update_positions():
    page = 1
    has_more = True

    while has_more:
        success, resp_data = service.SportMonksAPIClient().fetch_types(page=page, per_page=50)

        if not success:
            break

        try:
            types_data = resp_data["data"]
        except KeyError:
            break

        with transaction.atomic():

            for type_ in types_data:

                if not type_["model_type"] == "position":
                    continue

                models.Position.objects.update_or_create(
                    remote_id=type_["id"],
                    defaults={
                        "name": type_["name"],
                        "code": type_["code"],
                    }
                )

        has_more = resp_data["pagination"]["has_more"]
        page += 1


def update_fixture_states():
    page = 1
    has_more = True

    while has_more:
        success, resp_data = service.SportMonksAPIClient().fetch_fixture_states(page=page, per_page=50)

        if not success:
            break

        try:
            states_data = resp_data["data"]
        except KeyError:
            break

        with transaction.atomic():

            for state in states_data:
                models.FixtureState.objects.update_or_create(
                    remote_id=state["id"],
                    defaults={
                        "state": state["state"],
                        "title": state["name"],
                        "short_title": state["short_name"],
                    }
                )

        has_more = resp_data["pagination"]["has_more"]
        page += 1


def update_leagues():
    page = 1
    has_more = True

    while has_more:
        success, resp_data = service.SportMonksAPIClient().fetch_leagues(page=page, per_page=50)

        if not success:
            break

        try:
            leagues_data = resp_data["data"]
        except KeyError:
            break

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


def update_seasons_by_league(league_id):
    page = 1
    has_more = True

    while has_more:
        success, resp_data = service.SportMonksAPIClient().fetch_seasons_by_league(
            league_id=league_id,
            page=page,
            per_page=50
        )

        if not success:
            break

        try:
            seasons_data = resp_data["data"]
        except KeyError:
            break

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


def update_rounds_by_season(season_id):
    success, resp_data = service.SportMonksAPIClient().fetch_rounds_by_season(
        season_id=season_id
    )

    if not success:
        return

    try:
        rounds_data = resp_data["data"]
    except KeyError:
        return

    with transaction.atomic():

        for rnd in rounds_data:
            models.Round.objects.update_or_create(
                remote_id=rnd["id"],
                defaults={
                    "league": models.League.objects.get(remote_id=rnd["league_id"]),
                    "season": models.Season.objects.get(remote_id=rnd["season_id"]),
                    "name": rnd["name"],
                    "is_finished": rnd["finished"],
                    "is_current": rnd["is_current"],
                    "starting_at": rnd["starting_at"],
                    "ending_at": rnd["ending_at"],
                    "games_in_current_week": rnd["games_in_current_week"],
                }
            )


def update_fixtures_by_season(season_id):
    page = 1
    has_more = True

    while has_more:
        success, resp_data = service.SportMonksAPIClient().fetch_fixtures_by_season(
            season_id=season_id,
            page=page,
            per_page=50
        )

        if not success:
            break

        try:
            fixtures_data = resp_data["data"]
        except KeyError:
            break

        with transaction.atomic():

            for fixture in fixtures_data:
                home_club = None
                away_club = None

                for p in fixture["participants"]:
                    if p["meta"]["location"] == "home":
                        home_club = models.Club.objects.get(remote_id=p["id"])
                    elif p["meta"]["location"] == "away":
                        away_club = models.Club.objects.get(remote_id=p["id"])

                models.Fixture.objects.update_or_create(
                    remote_id=fixture["id"],
                    defaults={
                        "season": models.Season.objects.get(remote_id=fixture["season_id"]),
                        "round": models.Round.objects.get(remote_id=fixture["round_id"]),
                        "home_club": home_club,
                        "away_club": away_club,
                        "title": fixture["name"],
                        "venue_id": fixture["venue_id"],
                        "state": models.FixtureState.objects.get(remote_id=fixture["state_id"]),
                        "result_info": fixture["result_info"],
                        "match_date": fixture["starting_at"],
                        "length": fixture["length"],
                    }
                )
        has_more = resp_data["pagination"]["has_more"]
        page += 1


def update_clubs_by_season(season_id):
    success, resp_data = service.SportMonksAPIClient().fetch_clubs_by_season(
        season_id=season_id
    )

    if not success:
        return

    try:
        clubs_data = resp_data["data"]
    except KeyError:
        return

    with transaction.atomic():

        for club in clubs_data:
            players_data = club["players"]

            club, _ = models.Club.objects.update_or_create(
                remote_id=club["id"],
                defaults={
                    "name": club["name"],
                    "league": models.Season.objects.get(remote_id=season_id).league,
                    "short_name": club["short_code"],
                    "logo_path": club["image_path"],
                    "founded_year": club["founded"],
                    "country_id": club["country_id"],
                    "venue_id": club["venue_id"],
                    "type": club["type"],
                })

            for player in players_data:
                plyer = models.Player.objects.get(remote_id=player["player_id"])
                models.ClubPlayer.objects.update_or_create(
                    remote_id=player["id"],
                    defaults={
                        "club": club,
                        "player": plyer,
                        "position": models.Position.objects.get(remote_id=player["position_id"]) if player[
                            "position_id"] else None,

                        "transfer_id": player["transfer_id"],
                        "start_date": player["start"],
                        "end_date": player["end"],
                        "is_captain": player["captain"],
                        "kit_number": player["jersey_number"],
                        "is_current_club": True,
                    }
                )

                plyer.club = club
                plyer.club_contract_until = player["end"]
                plyer.save(update_fields=["club", "club_contract_until"])


def update_club_details(club_id):
    success, resp_data = service.SportMonksAPIClient().fetch_club_by_id(
        club_id=club_id
    )

    if not success:
        return

    try:
        club_data = resp_data["data"]
    except KeyError:
        return

    with transaction.atomic():

        club = models.Club.objects.update_or_create(
            remote_id=club_data["id"],
            defaults={
                "name": club_data["name"],
                "short_name": club_data["short_code"],
                "logo_path": club_data["image_path"],
                "founded_year": club_data["founded"],
                "country_id": club_data["country_id"],
                "venue_id": club_data["venue_id"],
                "type": club_data["type"],
            })[0]

        for player in club_data["players"]:
            plyer = models.Player.objects.get(remote_id=player["player_id"])
            models.ClubPlayer.objects.update_or_create(
                remote_id=player["id"],
                defaults={
                    "club": club,
                    "player": plyer,
                    "position": models.Position.objects.get(remote_id=player["position_id"]) if player[
                        "position_id"] else None,

                    "transfer_id": player["transfer_id"],
                    "start_date": player["start"],
                    "end_date": player["end"],
                    "is_captain": player["captain"],
                    "kit_number": player["jersey_number"],
                    "is_current_club": True,
                }
            )

            plyer.club = club
            plyer.club_contract_until = player["end"]
            plyer.save(update_fields=["club", "club_contract_until"])


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
                        "position": models.Position.objects.get(remote_id=player["position_id"]) if player[
                            "position_id"] else None,
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
