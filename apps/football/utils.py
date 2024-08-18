from django.db import transaction

from . import service, models


def update_leagues():
    page = 1
    has_more = True

    while has_more:
        success, resp_data = service.SportMonksAPIClient().fetch_leagues(page=page, per_page=100)

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
