from pprint import pprint

from django.db import transaction
from rest_framework import serializers

from . import service, models


def update_types():
    """ Update sportmonks types & positions. """
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

                if type_["model_type"] == "position":
                    models.Position.objects.update_or_create(
                        remote_id=type_["id"],
                        defaults={
                            "name": type_["name"],
                            "code": type_["code"],
                        }
                    )
                else:
                    models.SportMonksType.objects.update_or_create(
                        remote_id=type_["id"],
                        defaults={
                            "name": type_["name"],
                            "code": type_["code"],
                            "model_type": type_["model_type"],
                            "developer_name": type_["developer_name"],
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
                home_score = None
                away_score = None

                for p in fixture["participants"]:
                    if p["meta"]["location"] == "home":
                        home_club = models.Club.objects.get(remote_id=p["id"])
                    elif p["meta"]["location"] == "away":
                        away_club = models.Club.objects.get(remote_id=p["id"])

                for score in fixture["scores"]:
                    if score["description"] == "CURRENT":
                        if score["participant_id"] == home_club.remote_id:
                            home_score = score["score"]["goals"]
                        elif score["participant_id"] == away_club.remote_id:
                            away_score = score["score"]["goals"]

                fixture_obj, _ = models.Fixture.objects.update_or_create(
                    remote_id=fixture["id"],
                    defaults={
                        "season": models.Season.objects.get(remote_id=fixture["season_id"]),
                        "round": models.Round.objects.get(remote_id=fixture["round_id"]),
                        "home_club": home_club,
                        "away_club": away_club,
                        "home_club_score": home_score,
                        "away_club_score": away_score,
                        "title": fixture["name"],
                        "venue_id": fixture["venue_id"],
                        "state": models.FixtureState.objects.get(remote_id=fixture["state_id"]),
                        "result_info": fixture["result_info"],
                        "match_date": fixture["starting_at"],
                        "length": fixture["length"],
                    }
                )

                for event in fixture["events"]:
                    if event["sub_type_id"]:
                        sub_type = models.SportMonksType.objects.get(remote_id=event["sub_type_id"])
                    else:
                        sub_type = None

                    try:
                        models.FixtureEvent.objects.update_or_create(
                            remote_id=event["id"],
                            defaults={
                                "fixture": fixture_obj,
                                "type": models.SportMonksType.objects.get(remote_id=event["type_id"]),
                                "sub_type": sub_type,
                                "club": models.Club.objects.get(remote_id=event["participant_id"]),
                                "player": models.Player.objects.get(remote_id=event["player_id"]),
                                "related_player": models.Player.objects.get(remote_id=event["related_player_id"]),
                                "minute": event["minute"],
                                "extra_minute": event["extra_minute"],
                                "injured": event["injured"],
                                "on_bench": event["on_bench"],
                                "result": event["result"],
                                "info": event["info"],
                            }
                        )
                    except (models.Player.DoesNotExist,):
                        continue

                for stat in fixture["statistics"]:
                    models.FixtureStatistic.objects.update_or_create(
                        remote_id=stat["id"],
                        defaults={
                            "fixture": fixture_obj,
                            "type": models.SportMonksType.objects.get(remote_id=stat["type_id"]),
                            "club": models.Club.objects.get(remote_id=stat["participant_id"]),
                            "value": stat["data"]["value"],
                            "data": stat["data"],
                            "location": stat["location"],
                        }
                    )
                try:
                    for lineup in fixture["lineups"]:
                        models.Lineup.objects.update_or_create(
                            remote_id=lineup["id"],
                            defaults={
                                "fixture": fixture_obj,
                                "type": models.SportMonksType.objects.get(remote_id=lineup["type_id"]),
                                "club": models.Club.objects.get(remote_id=lineup["team_id"]),
                                "player": models.Player.objects.get(remote_id=lineup["player_id"]),
                            }
                        )
                except models.Player.DoesNotExist:
                    print("=" * 200)
                    continue
        has_more = resp_data["pagination"]["has_more"]
        page += 1


def update_fixture_by_id(fixture_id):
    success, resp_data = service.SportMonksAPIClient().fetch_fixture_by_id(
        fixture_id=fixture_id
    )

    if not success:
        return

    try:
        fixture = resp_data["data"]
    except KeyError:
        return

    with transaction.atomic():

        home_club = None
        away_club = None
        home_score = None
        away_score = None

        for p in fixture["participants"]:
            if p["meta"]["location"] == "home":
                home_club = models.Club.objects.get(remote_id=p["id"])
            elif p["meta"]["location"] == "away":
                away_club = models.Club.objects.get(remote_id=p["id"])

        for score in fixture["scores"]:
            if score["description"] == "CURRENT":
                if score["participant_id"] == home_club.remote_id:
                    home_score = score["score"]["goals"]
                elif score["participant_id"] == away_club.remote_id:
                    away_score = score["score"]["goals"]

        fixture_obj, _ = models.Fixture.objects.update_or_create(
            remote_id=fixture["id"],
            defaults={
                "season": models.Season.objects.get(remote_id=fixture["season_id"]),
                "round": models.Round.objects.get(remote_id=fixture["round_id"]),
                "home_club": home_club,
                "away_club": away_club,
                "home_club_score": home_score,
                "away_club_score": away_score,
                "title": fixture["name"],
                "venue_id": fixture["venue_id"],
                "state": models.FixtureState.objects.get(remote_id=fixture["state_id"]),
                "result_info": fixture["result_info"],
                "match_date": fixture["starting_at"],
                "length": fixture["length"],
            }
        )

        for event in fixture["events"]:
            if event["sub_type_id"]:
                sub_type = models.SportMonksType.objects.get(remote_id=event["sub_type_id"])
            else:
                sub_type = None

            try:
                models.FixtureEvent.objects.update_or_create(
                    remote_id=event["id"],
                    defaults={
                        "fixture": fixture_obj,
                        "type": models.SportMonksType.objects.get(remote_id=event["type_id"]),
                        "sub_type": sub_type,
                        "club": models.Club.objects.get(remote_id=event["participant_id"]),
                        "player": models.Player.objects.get(
                            remote_id=event["player_id"]
                        ) if event["player_id"] else None,
                        "related_player": models.Player.objects.get(
                            remote_id=event["related_player_id"]
                        ) if event["related_player_id"] else None,
                        "minute": event["minute"],
                        "extra_minute": event["extra_minute"],
                        "injured": event["injured"],
                        "on_bench": event["on_bench"],
                        "result": event["result"],
                        "info": event["info"],
                    }
                )
            except (models.Player.DoesNotExist,):
                continue

        for stat in fixture["statistics"]:
            models.FixtureStatistic.objects.update_or_create(
                remote_id=stat["id"],
                defaults={
                    "fixture": fixture_obj,
                    "type": models.SportMonksType.objects.get(remote_id=stat["type_id"]),
                    "club": models.Club.objects.get(remote_id=stat["participant_id"]),
                    "value": stat["data"]["value"],
                    "data": stat["data"],
                    "location": stat["location"],
                }
            )

        for lineup in fixture["lineups"]:
            try:
                models.Lineup.objects.update_or_create(
                    remote_id=lineup["id"],
                    defaults={
                        "fixture": fixture_obj,
                        "type": models.SportMonksType.objects.get(remote_id=lineup["type_id"]),
                        "club": models.Club.objects.get(
                            remote_id=lineup["team_id"]
                        ) if lineup["team_id"] else None,
                        "player": models.Player.objects.get(
                            remote_id=lineup["player_id"]
                        ) if lineup["player_id"] else None,
                    }
                )
            except (models.Player.DoesNotExist, models.Club.DoesNotExist, models.SportMonksType.DoesNotExist):
                continue


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

                try:
                    plyer = models.Player.objects.get(remote_id=player["player_id"])
                except models.Player.DoesNotExist:
                    continue

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
                plyer.jersey_number = player["jersey_number"]
                plyer.club_contract_until = player["end"]
                plyer.save(update_fields=["club", "club_contract_until", "jersey_number"])


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
            plyer.jersey_number = player["jersey_number"]
            plyer.save(update_fields=["club", "club_contract_until", "jersey_number"])


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


@transaction.atomic
def update_premierleague_status_by_players():
    success, resp_data = service.PremierLeagueAPIClient().fetch_statistics()

    try:
        players_data = resp_data['elements']
    except Exception as e:
        raise serializers.ValidationError(
            {"API": "Invalid  data", "message": "Problem with API response"}
        )

    count = 0
    for player in players_data:
        count = count + 1

        models.PremierLeagueStatusByPlayer.objects.update_or_create(
            remote_id=player["id"],
            # code=player["code"],
            defaults={
                "code": player["code"],
                "dreamteam_count": player["dreamteam_count"],
                "in_dreamteam": player["in_dreamteam"],
                "element_type": player["element_type"],
                "ep_next": player["ep_next"],
                "ep_this": player["ep_this"],
                "form": player["form"],
                "value_form": player["value_form"],
                "selected_by_percent": player["selected_by_percent"],
                "points_per_game": player["points_per_game"],
                "now_cost": player["now_cost"],
                "web_name": player["web_name"],
                "first_name": player["first_name"],
                "second_name": player["second_name"],
                "special": player["special"],
                "squad_number": player["squad_number"],
                "status": player["status"],
                "photo": player["photo"],
                "photo_url": f"https://resources.premierleague.com/premierleague/photos/players/250x250/p{player['code']}.png",
                "event_points": player["event_points"],
                "team": player["team"],
                "team_code": player["team_code"],
                "total_points": player["total_points"],
                "transfers_in": player["transfers_in"],
                "transfers_out": player["transfers_out"],
                "goals_scored": player["goals_scored"],
                "clean_sheets": player["clean_sheets"],
                "goals_conceded": player["goals_conceded"],
                "own_goals": player["own_goals"],
                "penalties_saved": player["penalties_saved"],
                "penalties_missed": player["penalties_missed"],
                "yellow_cards": player["yellow_cards"],
                "red_cards": player["red_cards"],
                "saves": player["saves"],
                "bonus": player["bonus"],
                "bps": player["bps"],
                "influence_rank": player["influence_rank"],
                "creativity_rank": player["creativity_rank"],
                "threat_rank": player["threat_rank"],
                "ict_index_rank": player["ict_index_rank"],
                "now_cost_rank": player["now_cost_rank"],
                "form_rank": player["form_rank"],
                "selected_rank": player["selected_rank"],
                "direct_freekicks_order": player["direct_freekicks_order"],
                "penalties_order": player["penalties_order"],
                "influence": player["influence"],
                "threat": player["threat"],
                "ict_index": player["ict_index"],
                "expected_goals": player["expected_goals"],
            }
        )
    return count
