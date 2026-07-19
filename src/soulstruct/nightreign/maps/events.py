"""Nightreign MSB events (Smithbox MSB-NR)."""
from __future__ import annotations

import typing as tp
from dataclasses import dataclass

from soulstruct.base.maps.msb.msb_entry import MSBBinaryStruct
from soulstruct.eldenring.maps.events import *  # noqa: F403
from soulstruct.eldenring.maps.events import MSBEvent

from .enums import MSBEventSubtype


class EmptyEventDataStruct(MSBBinaryStruct):
    pass


def _empty_event(name: str, subtype: MSBEventSubtype):
    @dataclass(slots=True, eq=False, repr=False)
    class _Event(MSBEvent):
        SUBTYPE_ENUM: tp.ClassVar[MSBEventSubtype] = subtype
        STRUCTS = MSBEvent.STRUCTS | {"subtype_data": EmptyEventDataStruct}

    _Event.__name__ = name
    _Event.__qualname__ = name
    return _Event


MSBMapOffsetEvent = _empty_event("MSBMapOffsetEvent", MSBEventSubtype.MapOffset)
MSBPatrolInfoEvent = _empty_event("MSBPatrolInfoEvent", MSBEventSubtype.PatrolInfo)
MSBAutoDrawGroupEvent = _empty_event("MSBAutoDrawGroupEvent", MSBEventSubtype.AutoDrawGroup)
MSBBirdRouteEvent = _empty_event("MSBBirdRouteEvent", MSBEventSubtype.BirdRoute)
MSBTalkInfoEvent = _empty_event("MSBTalkInfoEvent", MSBEventSubtype.TalkInfo)
MSBTeamFightEvent = _empty_event("MSBTeamFightEvent", MSBEventSubtype.TeamFight)

MSBPseudoMultiplayerEvent = MSBNPCInvasionEvent
MSBPlatoonInfoEvent = MSBPlatoonEvent
MSBRidingEvent = MSBMountEvent
MSBSignPuddleEvent = MSBSignPoolEvent

__all__ = [
    "MSBMapOffsetEvent",
    "MSBPatrolInfoEvent",
    "MSBAutoDrawGroupEvent",
    "MSBBirdRouteEvent",
    "MSBTalkInfoEvent",
    "MSBTeamFightEvent",
    "MSBPseudoMultiplayerEvent",
    "MSBPlatoonInfoEvent",
    "MSBRidingEvent",
    "MSBSignPuddleEvent",
]
