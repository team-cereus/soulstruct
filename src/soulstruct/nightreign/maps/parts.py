from __future__ import annotations

"""Nightreign MSB parts: ER layouts plus UnkA8 header offset (Smithbox MSB-NR)."""

__all__ = [
    "MSBPart",
    "MSBMapPiece",
    "MSBAsset",
    "MSBCharacter",
    "MSBPlayerStart",
    "MSBCollision",
    "MSBDummyAsset",
    "MSBDummyCharacter",
    "MSBConnectCollision",
]

import typing as tp
from dataclasses import dataclass, field

from soulstruct.base.maps.msb.msb_entry import MSBHeaderStruct, MSBBinaryStruct, MSBEntry, EntryRef
from soulstruct.utilities.binary import *
from soulstruct.utilities.maths import EulerDeg, Vector3

from soulstruct.eldenring.maps.parts import *  # noqa: F403
from soulstruct.eldenring.maps.parts import (
    PartHeaderStruct as _ERPartHeaderStruct,
    MSBMapPiece as _ERMapPiece,
    MSBAsset as _ERAsset,
    MSBCharacter as _ERCharacter,
    MSBPlayerStart as _ERPlayerStart,
    MSBCollision as _ERCollision,
    MSBDummyAsset as _ERDummyAsset,
    MSBDummyCharacter as _ERDummyCharacter,
    MSBConnectCollision as _ERConnectCollision,
    MSBPart as _ERPart,
)

if tp.TYPE_CHECKING:
    from soulstruct.utilities.misc import IDList


class NRPartHeaderStruct(MSBHeaderStruct):
    """ER part header, but the trailing 24 bytes are UnkA8 offset + UnkB0 + UnkB8 (not zero pad)."""

    name_offset: long
    model_instance_id: int
    _subtype_int: int
    subtype_index: int
    _model_index: int = field(**EntryRef("MODEL_PARAM_ST"))
    sib_path_offset: long
    translate: Vector3
    rotate: EulerDeg
    scale: Vector3
    part_unkh_44: int
    event_layer: int
    _zero: int = binary(asserted=0, init=False)
    draw_info_1_data_offset: long
    draw_info_2_data_offset: long
    supertype_data_offset: long
    subtype_data_offset: long
    gparam_data_offset: long
    scene_gparam_data_offset: long
    grass_config_data_offset: long
    unk8_data_offset: long
    unk9_data_offset: long
    tile_load_config_data_offset: long
    unk11_data_offset: long
    unk_a8_data_offset: long
    _unk_b0: long = binary(asserted=0, init=False)
    _unk_b8: long = binary(asserted=0, init=False)

    @classmethod
    def reader_to_entry_kwargs(
        cls,
        reader: BinaryReader,
        entry_type: type[MSBEntry],
        entry_offset: int,
    ) -> dict[str, tp.Any]:
        kwargs = super(NRPartHeaderStruct, cls).reader_to_entry_kwargs(reader, entry_type, entry_offset)
        kwargs["sib_path"] = reader.unpack_string(
            offset=entry_offset + kwargs.pop("sib_path_offset"), encoding=entry_type.NAME_ENCODING
        )
        consumed = {f"{name}_offset" for name in entry_type.STRUCTS}
        for key in list(kwargs):
            if key.endswith("_offset") and key not in consumed:
                kwargs.pop(key)
        return kwargs

    @classmethod
    def preprocess_write_kwargs(
        cls,
        entry: MSBEntry,
        entry_lists: dict[str, IDList[MSBEntry]],
        kwargs: dict[str, tp.Any],
    ) -> None:
        super(NRPartHeaderStruct, cls).preprocess_write_kwargs(entry, entry_lists, kwargs)
        if "model_instance_id" not in kwargs:
            kwargs["model_instance_id"] = getattr(entry, "model_instance_id", 0)
        kwargs["sib_path_offset"] = RESERVED
        kwargs.pop("supertype_index")
        used = {f"{name}_offset" for name in getattr(entry, "STRUCTS", {})}
        for field_name in cls.get_binary_field_names():
            if field_name.endswith("_offset") and field_name not in used and field_name not in (
                "name_offset",
                "sib_path_offset",
            ):
                kwargs.setdefault(field_name, 0)

    @classmethod
    def post_write(
        cls,
        entry: _ERPart,
        writer: BinaryWriter,
        entry_offset: int,
        entry_lists: [dict[str, IDList[MSBEntry]]],
    ):
        _ERPartHeaderStruct.post_write(entry, writer, entry_offset, entry_lists)


class UnkA8Struct(MSBBinaryStruct):
    """16-byte UnkA8 blob on NR Enemy and Asset parts (Smithbox MSB-NR)."""

    unk_a8_00: short = -1
    unk_a8_02: short = -1
    unk_a8_04: short = -1
    unk_a8_06: short = 0
    unk_a8_08: int = 0
    unk_a8_0c: int = 0


class NRCharacterDataStruct(MSBBinaryStruct):
    """NR enemy type data (Smithbox EnemyBase). Same size as ER, fewer zero-asserts."""

    char_unk_00: int = -1
    char_unk_04: int = -1
    ai_id: int
    character_id: int
    talk_id: int
    char_unk_14: byte = 0
    char_unk_15: byte = 0
    platoon_id: short
    player_id: int
    _draw_parent_index: int = field(**EntryRef("PARTS_PARAM_ST"))
    _patrol_route_event_index: short = field(**EntryRef("patrol_route_events"))
    scenario_placement_param_id: short = -1
    char_unk_24: int
    char_unk_28: int
    char_activate_condition_param_id: int
    char_unk_30: int = 0
    char_unk_34: int
    backup_event_animation_id: int
    char_unk_3c: sbyte = -1
    char_unk_3d: byte = 0
    char_unk_3e: short = -1
    special_effect_set_param_id: list[int] = binary_array(4)
    char_unk_50: int = 0
    char_unk_54: int = 0
    char_unk_58: int = 0
    char_unk_5c: int = 0
    char_unk_60: int = 0
    char_unk_64: int = 0
    char_unk_68: int = 0
    char_unk_6c: int = 0
    _offset70: long = binary(asserted=0, init=False)
    _offset78: long = binary(asserted=0x80, init=False)
    char_unk78_00: int = 0
    char_unk_84: float
    unk78_tail: list[int] = binary_array(14)


class NRPartReadMixin:
    """Relative offset 0 means absent; leftover NR UnkA8 offsets are ignored when unused."""

    @classmethod
    def reader_to_entry_kwargs(cls, reader, entry_offset: int):
        kwargs = cls.HEADER_STRUCT.reader_to_entry_kwargs(reader, cls, entry_offset)
        for struct_name, struct_type in cls.STRUCTS.items():
            rel = kwargs.pop(f"{struct_name}_offset", 0)
            if struct_type is None or not rel:
                continue
            reader.seek(entry_offset + rel)
            kwargs |= struct_type.reader_to_entry_kwargs(reader, cls, entry_offset)
        return kwargs


def _with_header(er_cls, unk_a8):
    """Clone an ER part class with the NR header and optional UnkA8 struct."""

    extra_fields = {}
    if unk_a8 is UnkA8Struct:
        extra_fields = {
            "unk_a8_00": -1,
            "unk_a8_02": -1,
            "unk_a8_04": -1,
            "unk_a8_06": 0,
            "unk_a8_08": 0,
            "unk_a8_0c": 0,
        }

    ns = {
        "HEADER_STRUCT": NRPartHeaderStruct,
        "STRUCTS": {**er_cls.STRUCTS, "unk_a8_data": unk_a8},
        **{k: v for k, v in extra_fields.items()},
    }
    return type(er_cls.__name__, (NRPartReadMixin, er_cls), ns)


# MapPiece / PlayerStart / Collision / DummyAsset / ConnectCollision: UnkA8 offset is 0.
MSBMapPiece = _with_header(_ERMapPiece, None)
MSBPlayerStart = _with_header(_ERPlayerStart, None)
MSBCollision = _with_header(_ERCollision, None)
MSBDummyAsset = _with_header(_ERDummyAsset, None)
MSBConnectCollision = _with_header(_ERConnectCollision, None)
class NRDrawInfo2(MSBBinaryStruct):
    """NR DisplayGroup / DrawInfo2: same 72-byte size as ER DrawInfo2, no zero-pad assert."""

    condition_2: int
    display_groups_2: list[int] = binary_array(8, uint)
    unk2_24: short
    unk2_26: short
    unk2_28: int = 0
    unk2_2c: int = 0
    unk2_30: int = 0
    unk2_34: int = 0
    unk2_38: int = 0
    unk2_3c: int = 0
    unk2_40: int = 0
    unk2_44: int = 0


class NRAssetDataStruct(MSBBinaryStruct):
    """NR asset type data: ER-sized prefix without zero-pad asserts, then 256-byte inner blob."""

    asset_unk_00: byte = 0
    asset_unk_01: byte = 0
    asset_unk_02: short = 0
    asset_unk_04: int = 0
    asset_unk_08: int = 0
    asset_unk_0c: int = 0
    asset_unk_10: byte = 0
    asset_unk_11: byte = 0
    asset_unk_12: sbyte = 0
    asset_unk_13: byte = 0
    asset_unk_14: int = 0
    asset_unk_18: int = 0
    asset_sfx_param_relative_id: short = 0
    asset_unk_1e: short = 0
    asset_unk_20: int = 0
    asset_unk_24: int = 0
    asset_unk_28: int = 0
    asset_unk_2c: int = 0
    asset_unk_30: int = 0
    asset_unk_34: int = 0
    _unk_parts_indices: list[int] = field(**EntryRef("PARTS_PARAM_ST", array_size=6))
    asset_unk_50: int = 0
    asset_unk_54: int = 0
    asset_unk_58: int = 0
    asset_unk_5c: int = 0
    asset_unk_60: int = 0
    asset_unk_64: int = 0
    _asset_unk1_offset: long = binary(asserted=0x88, init=False)
    _asset_unk2_offset: long = binary(asserted=0xC8, init=False)
    _asset_unk3_offset: long = binary(asserted=0x108, init=False)
    _asset_unk4_offset: long = binary(asserted=0x148, init=False)
    asset_inner: list[int] = binary_array(64)


@dataclass(slots=True, eq=False, repr=False)
class MSBAsset(NRPartReadMixin, _ERAsset):
    HEADER_STRUCT = NRPartHeaderStruct
    STRUCTS = {
        **_ERAsset.STRUCTS,
        "draw_info_2_data": NRDrawInfo2,
        "subtype_data": NRAssetDataStruct,
        "unk_a8_data": UnkA8Struct,
    }
    unk2_28: int = 0
    unk2_2c: int = 0
    unk2_30: int = 0
    unk2_34: int = 0
    unk2_38: int = 0
    unk2_3c: int = 0
    unk2_40: int = 0
    unk2_44: int = 0
    asset_unk_00: int = 0
    asset_unk_01: int = 0
    asset_unk_04: int = 0
    asset_unk_08: int = 0
    asset_unk_0c: int = 0
    asset_unk_13: int = 0
    asset_unk_14: int = 0
    asset_unk_18: int = 0
    asset_unk_20: int = 0
    asset_unk_2c: int = 0
    asset_inner: list[int] = field(default_factory=lambda: [0] * 64)
    unk_a8_00: int = -1
    unk_a8_02: int = -1
    unk_a8_04: int = -1
    unk_a8_06: int = 0
    unk_a8_08: int = 0
    unk_a8_0c: int = 0



@dataclass(slots=True, eq=False, repr=False)
class MSBCharacter(NRPartReadMixin, _ERCharacter):
    HEADER_STRUCT = NRPartHeaderStruct
    STRUCTS = {
        **_ERCharacter.STRUCTS,
        "subtype_data": NRCharacterDataStruct,
        "unk_a8_data": UnkA8Struct,
    }

    char_unk_00: int = -1
    char_unk_04: int = -1
    char_unk_14: int = 0
    scenario_placement_param_id: int = -1
    char_unk_30: int = 0
    char_unk_3d: int = 0
    char_unk_3e: int = -1
    char_unk_50: int = 0
    char_unk_54: int = 0
    char_unk_58: int = 0
    char_unk_5c: int = 0
    char_unk_60: int = 0
    char_unk_64: int = 0
    char_unk_68: int = 0
    char_unk_6c: int = 0
    char_unk78_00: int = 0
    unk78_tail: list[int] = field(default_factory=lambda: [-1, -1, 0xA0000FF, 0] * 3 + [0] * 2)
    unk_a8_00: int = -1
    unk_a8_02: int = -1
    unk_a8_04: int = -1
    unk_a8_06: int = 0
    unk_a8_08: int = 0
    unk_a8_0c: int = 0


@dataclass(slots=True, eq=False, repr=False)
class MSBDummyCharacter(MSBCharacter):
    """NR dummy enemies have no UnkA8 blob (Smithbox DummyEnemy.HasUnkA8Data = false)."""

    SUBTYPE_ENUM: tp.ClassVar = _ERDummyCharacter.SUBTYPE_ENUM
    STRUCTS = {
        **MSBCharacter.STRUCTS,
        "unk_a8_data": None,
    }


# Keep MSBPart name for msb.py type hints (header is per-subtype).
MSBPart = _ERPart
