"""Nightreign MSB regions: ER-compatible types plus NR-only subtypes (Smithbox MSB-NR)."""
from __future__ import annotations

import typing as tp
from dataclasses import dataclass

from soulstruct.utilities.binary import *

from soulstruct.eldenring.maps.msb.regions import *  # noqa: F403
from soulstruct.eldenring.maps.msb.regions import MSBRegion, MSBBinaryStruct, RegionHeaderStruct

from .enums import MSBRegionSubtype


class Int32PairRegionDataStruct(MSBBinaryStruct):
    unk_t00: int
    unk_t04: int


class Int32RegionDataStruct(MSBBinaryStruct):
    unk_t00: int


class BigJumpSealableRegionDataStruct(MSBBinaryStruct):
    unk_t00: float
    unk_t04: int
    unk_t08: int
    unk_t0c: int
    unk_t10: int
    unk_t14: int


def _no_type_data_region(name: str, subtype: MSBRegionSubtype):
    """HasTypeData is false in Smithbox: subtype_data offset must stay 0."""

    @dataclass(slots=True, eq=False, repr=False)
    class _Region(MSBRegion):
        SUBTYPE_ENUM: tp.ClassVar[MSBRegionSubtype] = subtype

    _Region.__name__ = name
    _Region.__qualname__ = name
    return _Region


def _pair_region(name: str, subtype: MSBRegionSubtype):
    @dataclass(slots=True, eq=False, repr=False)
    class _Region(MSBRegion):
        SUBTYPE_ENUM: tp.ClassVar[MSBRegionSubtype] = subtype
        STRUCTS = MSBRegion.STRUCTS | {"subtype_data": Int32PairRegionDataStruct}
        unk_t00: int = 0
        unk_t04: int = 0

    _Region.__name__ = name
    _Region.__qualname__ = name
    return _Region


# Aliases: same layout as Elden Ring classes, NR enum names.
MSBEntryPointRegion = MSBInvasionPointRegion
MSBReturnPointRegion = MSBSpawnPointRegion
MSBMapInfoOverrideRegion = MSBWeatherOverrideRegion
MSBMassPlacementRegion = MSBGroupDefeatRewardRegion
MSBEnvMapPointRegion = MSBEnvironmentMapPointRegion
MSBEnvMapEffectBoxRegion = MSBEnvironmentMapEffectBoxRegion
MSBWindPlacementRegion = MSBWindAreaRegion
MSBMapConnectionRegion = MSBConnectionRegion
MSBSFXRegion = MSBVFXRegion
MSBWindSFXRegion = MSBWindVFXRegion
MSBAutoDrawGroupSampleRegion = MSBAutoDrawGroupPointRegion
MSBHitSettingRegion = MSBHitsetRegion
MSBPatrolPointRegion = MSBPatrolRouteRegion
MSBWeatherAssetGenerationRegion = MSBWeatherCreateAssetPointRegion
MSBBigJumpRegion = MSBMountJumpRegion
MSBSoundDummyRegion = MSBDummyRegion
MSBFallPreventionOverrideRegion = MSBFallPreventionRemovalRegion
MSBBigJumpExitRegion = MSBMountJumpFallRegion
MSBMidRangeEnvMapOutputRegion = MSBEnvironmentMapOutputRegion  # ER class has no subtype_data

# NR HasTypeData == false (do not reuse ER classes that expect subtype_data).
MSBStaticWaypointRegion = _no_type_data_region("MSBStaticWaypointRegion", MSBRegionSubtype.StaticWaypoint)
MSBMapGridLayerConnectionRegion = _no_type_data_region(
    "MSBMapGridLayerConnectionRegion", MSBRegionSubtype.MapGridLayerConnection
)
MSBEnemySpawnPointRegion = _no_type_data_region("MSBEnemySpawnPointRegion", MSBRegionSubtype.EnemySpawnPoint)
MSBRollingObjectOverrideRegion = _no_type_data_region(
    "MSBRollingObjectOverrideRegion", MSBRegionSubtype.RollingObjectOverride
)
MSBSoundStateRegion = _no_type_data_region("MSBSoundStateRegion", MSBRegionSubtype.SoundState)
MSBMapVisibilityOverrideRegion = _no_type_data_region(
    "MSBMapVisibilityOverrideRegion", MSBRegionSubtype.MapVisibilityOverride
)
MSBOpenCharacterActivateLimitRegion = _no_type_data_region(
    "MSBOpenCharacterActivateLimitRegion", MSBRegionSubtype.OpenCharacterActivateLimit
)
MSBClearInfoRegion = _no_type_data_region("MSBClearInfoRegion", MSBRegionSubtype.ClearInfo)
MSBSourceWaypointRegion = _no_type_data_region("MSBSourceWaypointRegion", MSBRegionSubtype.SourceWaypoint)
MSBFastTravelOverrideRegion = _no_type_data_region(
    "MSBFastTravelOverrideRegion", MSBRegionSubtype.FastTravelRestriction
)
MSBPlayAreaRegion = _no_type_data_region("MSBPlayAreaRegion", MSBRegionSubtype.PlayArea)
MSBMountOverrideRegion = _no_type_data_region("MSBMountOverrideRegion", MSBRegionSubtype.HorseRideOverride)
MSBBuddySummonPointRegion = _no_type_data_region("MSBBuddySummonPointRegion", MSBRegionSubtype.BuddySummonPoint)

# NR HasTypeData == true.
MSBRespawnPointRegion = _pair_region("MSBRespawnPointRegion", MSBRegionSubtype.RespawnPoint)
MSBSmallBaseAttachRegion = _pair_region("MSBSmallBaseAttachRegion", MSBRegionSubtype.SmallBaseAttach)
MSBBirdRouteRegion = _pair_region("MSBBirdRouteRegion", MSBRegionSubtype.BirdRoute)
MSBUserEdgeRemovalInnerRegion = _pair_region(
    "MSBUserEdgeRemovalInnerRegion", MSBRegionSubtype.UserEdgeRemovalInner
)
MSBUserEdgeRemovalOuterRegion = _pair_region(
    "MSBUserEdgeRemovalOuterRegion", MSBRegionSubtype.UserEdgeRemovalOuter
)


@dataclass(slots=True, eq=False, repr=False)
class MSBRespawnOverrideRegion(MSBRegion):
    SUBTYPE_ENUM: tp.ClassVar[MSBRegionSubtype] = MSBRegionSubtype.RespawnOverride
    STRUCTS = MSBRegion.STRUCTS | {"subtype_data": Int32RegionDataStruct}
    unk_t00: int = 0


@dataclass(slots=True, eq=False, repr=False)
class MSBBigJumpSealableRegion(MSBRegion):
    SUBTYPE_ENUM: tp.ClassVar[MSBRegionSubtype] = MSBRegionSubtype.BigJumpSealable
    STRUCTS = MSBRegion.STRUCTS | {"subtype_data": BigJumpSealableRegionDataStruct}
    unk_t00: float = 0.0
    unk_t04: int = 0
    unk_t08: int = 0
    unk_t0c: int = 0
    unk_t10: int = 0
    unk_t14: int = 0


class NRRegionExtraData(MSBBinaryStruct):
    """NR region extra blob: Unk10 is used (often -1); ER treated it as zero pad."""

    map_id: int
    region_unkx_04: int
    _pad1: int = binary_pad(4, init=False)
    region_unkx_0c: int
    _unkx_10: int = 0
    _pad2: bytes = binary_pad(12, init=False)


class NRRegionHeaderStruct(RegionHeaderStruct):
    @classmethod
    def reader_to_entry_kwargs(cls, reader, entry_type, entry_offset):
        kwargs = super(RegionHeaderStruct, cls).reader_to_entry_kwargs(reader, entry_type, entry_offset)

        reader.seek(entry_offset + kwargs.pop("unk_shorts_a_offset"))
        unk_shorts_a_len = reader["h"]
        kwargs["unk_shorts_a"] = list(reader.unpack(f"{unk_shorts_a_len}h"))

        reader.seek(entry_offset + kwargs.pop("unk_shorts_b_offset"))
        unk_shorts_b_len = reader["h"]
        kwargs["unk_shorts_b"] = list(reader.unpack(f"{unk_shorts_b_len}h"))

        reader.seek(entry_offset + kwargs.pop("extra_data_offset"))
        extra_data = NRRegionExtraData.from_bytes(reader)
        kwargs |= extra_data.to_dict(ignore_underscore_prefix=True)

        shape_type_int = kwargs.pop("shape_type_int")
        try:
            shape_class = entry_type.SHAPE_CLASSES[shape_type_int]
        except KeyError:
            if shape_type_int == 6:
                raise ValueError("Composite Region shape type (6) is not supported in older games.")
            raise ValueError(f"Invalid MSB region shape type value: {shape_type_int}")
        reader.seek(entry_offset + kwargs.pop("shape_data_offset"))
        kwargs["shape"] = shape_class.from_msb_reader(reader)
        # NR Other (and similar) may have a leftover subtype offset even when unused.
        if getattr(entry_type, "STRUCTS", {}).get("subtype_data") is None:
            kwargs["subtype_data_offset"] = 0
        return kwargs


class NRRegionReadMixin:
    """Treat relative offset 0 as absent; ignore leftover NR subtype offsets."""

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


def _with_nr_region_header(cls):
    if NRRegionReadMixin in getattr(cls, "__mro__", ()):
        return cls
    return type(cls.__name__, (NRRegionReadMixin, cls), {"HEADER_STRUCT": NRRegionHeaderStruct})


for _name, _cls in list(globals().items()):
    if (
        isinstance(_cls, type)
        and _name.startswith("MSB")
        and "Region" in _name
        and hasattr(_cls, "HEADER_STRUCT")
    ):
        globals()[_name] = _with_nr_region_header(_cls)
