from django.db import models
from django.utils.translation import gettext_lazy as _


class SportMonksTypeModelTypeChoices(models.TextChoices):
    EVENT = "event", _("Event")
    HIGHLIGHT = "highlight", _("Highlight")
    INJURY_SUSPENSION = "injury_suspension", _("Injury Suspension")
    LINEUP = "lineup", _("Lineup")
    METADATA = "metadata", _("Metadata")
    PERIOD = "period", _("Period")
    PREDICTION = "prediction", _("Prediction")
    REFEREE = "referee", _("Referee")
    STAGE_TYPE = "stage_type", _("Stage Type")
    STANDING_CORRECTION = "standing_correction", _("Standing Correction")
    STANDING_RULE = "standing_rule", _("Standing Rule")
    STANDINGS = "standings", _("Standings")
    STATISTIC = "statistic", _("Statistic")
    SUB_EVENT = "sub_event", _("Sub Event")
    TIE_BREAKER_RULE = "tie_breaker_rule", _("Tie Breaker Rule")
    TIMELINE = "timeline", _("Timeline")
    TRANSFER = "transfer", _("Transfer")
