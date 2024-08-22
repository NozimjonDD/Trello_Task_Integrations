from rest_framework import views
from rest_framework.response import Response

from apps.football.utils import update_premierleague_status_by_players


class UpgadePremierLeagueStat(views.APIView):
    def post(self, request, *args, **kwargs):
        count = update_premierleague_status_by_players()

        return Response({"message": "class A", "count": count})
