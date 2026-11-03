"""Nightreign MSB events (Smithbox MSB-NR)."""
from __future__ import annotations

import typing as tp
from dataclasses import dataclass, field, make_dataclass

from soulstruct.base.maps.msb.msb_entry import MSBBinaryStruct, EntryRef
from soulstruct.eldenring.maps.events import *  # noqa: F403
from soulstruct.eldenring.maps.events import (
    MSBEvent,
    EventDataStruct as _EREventDataStruct,
    EventExtraDataStruct as _EREventExtraDataStruct,
    MSBTreasureEvent as _ERTreasure,
    MSBSpawnerEvent as _ERSpawner,
    MSBObjActEvent as _ERObjAct,
    MSBPatrolRouteEvent as _ERPatrolRoute,
    MSBRetryPointEvent as _ERRetry,
    MSBOtherEvent as _EROther,
    MSBNPCInvasionEvent,
    MSBPlatoonEvent,
    MSBMountEvent,
    MSBSignPoolEvent,
)
from soulstruct.utilities.binary import *

from .enums import MSBEventSubtype


class NREventDataStruct(MSBBinaryStruct):
    _attached_part_index: int = field(**EntryRef("PARTS_PARAM_ST"))
    _attached_region_index: int = field(**EntryRef("POINT_PARAM_ST"))
    entity_id: int
    event_unkd_0c: sbyte = 0
    event_unkd_0d: byte = 0
    event_unkd_0e: short = 0


class NREventExtraDataStruct(MSBBinaryStruct):
    map_id: int
    unk_04: int
    unk_08: int
    unk_0c: int
    unk_10: int = 0
    unk_14: int = 0
    unk_18: int = 0
    unk_1c: int = 0


class EmptyEventDataStruct(MSBBinaryStruct):
    """Placeholder for NR events whose type blob is empty or not yet modeled.
    Constrata forbids zero-field structs, so read/write are no-ops."""

    _dummy: int = 0  # never packed; overrides skip from_bytes

    @classmethod
    def reader_to_entry_kwargs(cls, reader, entry_type, entry_offset):
        return {}

    @classmethod
    def kwargs_to_msb_writer(cls, entry, writer, entry_offset, entry_lists, **kwargs):
        return


class NRTreasureEventDataStruct(MSBBinaryStruct):
    treasure_unk_00: int = 0
    treasure_unk_04: int = 0
    _treasure_part_index: int = field(**EntryRef("PARTS_PARAM_ST"))
    treasure_unk_0c: int = 0
    item_lot: int
    treasure_unk_14: int = 0
    treasure_unk_18: int = 0
    treasure_unk_1c: int = 0
    treasure_unk_20: int = 0
    treasure_unk_24: int = 0
    treasure_unk_28: int = 0
    treasure_unk_2c: int = 0
    treasure_unk_30: int = 0
    treasure_unk_34: int = 0
    action_button_id: int = 0
    pickup_animation_id: int = 0
    is_in_chest: byte = 0
    starts_disabled: byte = 0
    treasure_unk_42: byte = 0
    treasure_unk_43: byte = 0
    treasure_unk_44: int = 0
    treasure_unk_48: short = 0
    treasure_unk_4a: short = 0
    treasure_unk_4c: int = 0


_NR_COMMON_STRUCTS = {
    "supertype_data": NREventDataStruct,
    "extra_data": NREventExtraDataStruct,
}

_NR_EXTRA_FIELDS = [
    ("event_unkd_0d", int, field(default=0)),
    ("event_unkd_0e", int, field(default=0)),
    ("unk_10", int, field(default=0)),
    ("unk_14", int, field(default=0)),
    ("unk_18", int, field(default=0)),
    ("unk_1c", int, field(default=0)),
]


def _nr_event(er_cls, name: str | None = None, subtype_struct=None, extra_fields=()):
    structs = {**er_cls.STRUCTS, **_NR_COMMON_STRUCTS}
    if subtype_struct is not None:
        structs["subtype_data"] = subtype_struct
    cls = make_dataclass(
        name or er_cls.__name__,
        list(_NR_EXTRA_FIELDS) + list(extra_fields),
        bases=(er_cls,),
        namespace={"STRUCTS": structs},
        slots=True,
        eq=False,
        repr=False,
    )
    return cls


def _empty_event(name: str, subtype: MSBEventSubtype):
    @dataclass(slots=True, eq=False, repr=False)
    class _Event(MSBEvent):
        SUBTYPE_ENUM: tp.ClassVar[MSBEventSubtype] = subtype
        STRUCTS = {**MSBEvent.STRUCTS, **_NR_COMMON_STRUCTS, "subtype_data": EmptyEventDataStruct}
        event_unkd_0d: int = 0
        event_unkd_0e: int = 0
        unk_10: int = 0
        unk_14: int = 0
        unk_18: int = 0
        unk_1c: int = 0

    _Event.__name__ = name
    _Event.__qualname__ = name
    return _Event



class NRObjActEventDataStruct(MSBBinaryStruct):
    obj_act_entity_id: int
    _obj_act_part_index: int = field(**EntryRef("PARTS_PARAM_ST"))
    obj_act_param_id: int
    obj_act_state: byte
    obj_act_unk_0d: byte = 0
    obj_act_unk_0e: short = 0
    obj_act_flag: int
    obj_act_unk_14: int = 0
    obj_act_unk_18: int = 0
    obj_act_unk_1c: int = 0


class NRSpawnerEventDataStruct(MSBBinaryStruct):
    max_count: byte
    spawner_type: sbyte
    limit_count: short
    min_spawner_count: short
    max_spawner_count: short
    min_interval: float
    max_interval: float
    initial_spawn_count: sbyte
    spawner_unk_11: byte = 0
    spawner_unk_12: short = 0
    spawner_unk_14: float
    spawner_unk_18: float
    spawner_unk_1c: int = 0
    spawner_unk_20: int = 0
    spawner_unk_24: int = 0
    spawner_unk_28: int = 0
    spawner_unk_2c: int = 0
    _spawn_regions_indices: list[int] = field(**EntryRef("POINT_PARAM_ST", array_size=8))
    spawner_unk_50: int = 0
    spawner_unk_54: int = 0
    spawner_unk_58: int = 0
    spawner_unk_5c: int = 0
    _spawn_parts_indices: list[int] = field(**EntryRef("PARTS_PARAM_ST", array_size=32))
    spawner_unk_e0: list[int] = binary_array(8)


MSBTreasureEvent = _nr_event(
    _ERTreasure,
    extra_fields=[
        ("treasure_unk_00", int, field(default=0)),
        ("treasure_unk_04", int, field(default=0)),
        ("treasure_unk_0c", int, field(default=0)),
        ("treasure_unk_14", int, field(default=0)),
        ("treasure_unk_18", int, field(default=0)),
        ("treasure_unk_1c", int, field(default=0)),
        ("treasure_unk_20", int, field(default=0)),
        ("treasure_unk_24", int, field(default=0)),
        ("treasure_unk_28", int, field(default=0)),
        ("treasure_unk_2c", int, field(default=0)),
        ("treasure_unk_30", int, field(default=0)),
        ("treasure_unk_34", int, field(default=0)),
        ("treasure_unk_42", int, field(default=0)),
        ("treasure_unk_43", int, field(default=0)),
        ("treasure_unk_44", int, field(default=0)),
        ("treasure_unk_48", int, field(default=0)),
        ("treasure_unk_4a", int, field(default=0)),
        ("treasure_unk_4c", int, field(default=0)),
    ],
)
# make_dataclass doesn't take subtype_struct via extra; set after
MSBTreasureEvent.STRUCTS = {**MSBTreasureEvent.STRUCTS, "subtype_data": NRTreasureEventDataStruct}

MSBSpawnerEvent = _nr_event(
    _ERSpawner,
    subtype_struct=NRSpawnerEventDataStruct,
    extra_fields=[
        ("spawner_unk_11", int, field(default=0)),
        ("spawner_unk_12", int, field(default=0)),
        ("spawner_unk_1c", int, field(default=0)),
        ("spawner_unk_20", int, field(default=0)),
        ("spawner_unk_24", int, field(default=0)),
        ("spawner_unk_28", int, field(default=0)),
        ("spawner_unk_2c", int, field(default=0)),
        ("spawner_unk_50", int, field(default=0)),
        ("spawner_unk_54", int, field(default=0)),
        ("spawner_unk_58", int, field(default=0)),
        ("spawner_unk_5c", int, field(default=0)),
        ("spawner_unk_e0", list, field(default_factory=lambda: [0] * 8)),
    ],
)
MSBObjActEvent = _nr_event(
    _ERObjAct,
    subtype_struct=NRObjActEventDataStruct,
    extra_fields=[
        ("obj_act_unk_0d", int, field(default=0)),
        ("obj_act_unk_0e", int, field(default=0)),
        ("obj_act_unk_14", int, field(default=0)),
        ("obj_act_unk_18", int, field(default=0)),
        ("obj_act_unk_1c", int, field(default=0)),
    ],
)
MSBPatrolRouteEvent = _nr_event(_ERPatrolRoute)
MSBRetryPointEvent = _nr_event(_ERRetry)
MSBOtherEvent = _nr_event(_EROther)

MSBMapOffsetEvent = _empty_event("MSBMapOffsetEvent", MSBEventSubtype.MapOffset)
MSBPatrolInfoEvent = _empty_event("MSBPatrolInfoEvent", MSBEventSubtype.PatrolInfo)
MSBAutoDrawGroupEvent = _empty_event("MSBAutoDrawGroupEvent", MSBEventSubtype.AutoDrawGroup)
MSBBirdRouteEvent = _empty_event("MSBBirdRouteEvent", MSBEventSubtype.BirdRoute)
MSBTalkInfoEvent = _empty_event("MSBTalkInfoEvent", MSBEventSubtype.TalkInfo)
MSBTeamFightEvent = _empty_event("MSBTeamFightEvent", MSBEventSubtype.TeamFight)

MSBPseudoMultiplayerEvent = _nr_event(MSBNPCInvasionEvent, name="MSBPseudoMultiplayerEvent")
MSBPlatoonInfoEvent = _nr_event(MSBPlatoonEvent, name="MSBPlatoonInfoEvent")
MSBRidingEvent = _nr_event(MSBMountEvent, name="MSBRidingEvent")
MSBSignPuddleEvent = _nr_event(MSBSignPoolEvent, name="MSBSignPuddleEvent")

__all__ = [
    "MSBTreasureEvent",
    "MSBSpawnerEvent",
    "MSBObjActEvent",
    "MSBPatrolRouteEvent",
    "MSBRetryPointEvent",
    "MSBOtherEvent",
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
