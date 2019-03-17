""" Main Module Exports, please note that the order of imports IS IMPORTANT
    In this case: custom User must come first, afterwards import TrackableModel. """

# Structural models
# from backend.models.user import User
from backend.models.trackable_model import TrackableModel
from backend.models.user import User
from django.contrib.auth.models import Group

# Other models
from backend.models.multilang_field import MultilangField, MultilangFieldEntry
from backend.models.structure import Structure
from backend.models.project import (
    Project,
    KnowledgeArea,
    Participation,
    ParticipationRole,
)
from backend.models.collaboration import Collaboration
from backend.models.keyword import Keyword
