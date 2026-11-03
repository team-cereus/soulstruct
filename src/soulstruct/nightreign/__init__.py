"""Elden Ring: Nightreign — reuses Elden Ring soulstruct modules where formats match.

Do not star-import ``soulstruct.eldenring``: that binds ``maps`` to the Elden Ring MSB
(version 73) and shadows ``soulstruct.nightreign.maps`` (version 78).
"""

from soulstruct.eldenring import events, game_types, params, text  # noqa: F401
from . import constants  # noqa: F401
from . import maps  # noqa: F401
from . import models  # noqa: F401
