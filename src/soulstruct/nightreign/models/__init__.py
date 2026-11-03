"""Nightreign shares Elden Ring's model binder formats. Mirrors `soulstruct.eldenring.models` so game-submodule lookups
(e.g. `NIGHTREIGN.from_game_submodule_import("models.chrbnd", "CHRBND")`) resolve.
"""
from soulstruct.eldenring.models import *  # noqa: F403
