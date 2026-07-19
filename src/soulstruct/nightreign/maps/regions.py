"""Nightreign MSB regions: ER-compatible types plus NR-only passthrough subtypes."""
from __future__ import annotations

import typing as tp
from dataclasses import dataclass

from soulstruct.utilities.binary import *

from soulstruct.eldenring.maps.regions import *  # noqa: F403
from soulstruct.eldenring.maps.regions import MSBRegion, MSBBinaryStruct

from .enums import MSBRegionSubtype

class Int32PairRegionDataStruct(MSBBinaryStruct):
    unk_t00: int
    unk_t04: int


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


def _empty_region(name: str, subtype: MSBRegionSubtype):
    class _EmptyData(MSBBinaryStruct):
        pass

    @dataclass(slots=True, eq=False, repr=False)
    class _Region(MSBRegion):
        SUBTYPE_ENUM: tp.ClassVar[MSBRegionSubtype] = subtype
        STRUCTS = MSBRegion.STRUCTS | {"subtype_data": _EmptyData}

    _Region.__name__ = name
    _Region.__qualname__ = name
    return _Region


# Aliases: same layout as Elden Ring classes, NR enum names.
MSBEntryPointRegion = MSBInvasionPointRegion
MSBReturnPointRegion = MSBSpawnPointRegion

# NR-only or renamed subtypes (minimal type data).
MSBRespawnPointRegion = _pair_region("MSBRespawnPointRegion", MSBRegionSubtype.RespawnPoint)
MSBStaticWaypointRegion = _empty_region("MSBStaticWaypointRegion", MSBRegionSubtype.StaticWaypoint)
MSBMapGridLayerConnectionRegion = _pair_region("MSBMapGridLayerConnectionRegion", MSBRegionSubtype.MapGridLayerConnection)
MSBEnemySpawnPointRegion = _pair_region("MSBEnemySpawnPointRegion", MSBRegionSubtype.EnemySpawnPoint)
MSBRollingObjectOverrideRegion = _pair_region("MSBRollingObjectOverrideRegion", MSBRegionSubtype.RollingObjectOverride)
MSBSoundStateRegion = _pair_region("MSBSoundStateRegion", MSBRegionSubtype.SoundState)
MSBMapInfoOverrideRegion = MSBWeatherOverrideRegion
MSBMassPlacementRegion = MSBGroupDefeatRewardRegion
MSBMapVisibilityOverrideRegion = _pair_region("MSBMapVisibilityOverrideRegion", MSBRegionSubtype.MapVisibilityOverride)
MSBOpenCharacterActivateLimitRegion = _pair_region(
    "MSBOpenCharacterActivateLimitRegion", MSBRegionSubtype.OpenCharacterActivateLimit
)
MSBSmallBaseAttachRegion = _pair_region("MSBSmallBaseAttachRegion", MSBRegionSubtype.SmallBaseAttach)
MSBBirdRouteRegion = _pair_region("MSBBirdRouteRegion", MSBRegionSubtype.BirdRoute)
MSBClearInfoRegion = _pair_region("MSBClearInfoRegion", MSBRegionSubtype.ClearInfo)
MSBRespawnOverrideRegion = _pair_region("MSBRespawnOverrideRegion", MSBRegionSubtype.RespawnOverride)
MSBUserEdgeRemovalInnerRegion = _pair_region("MSBUserEdgeRemovalInnerRegion", MSBRegionSubtype.UserEdgeRemovalInner)
MSBUserEdgeRemovalOuterRegion = _pair_region("MSBUserEdgeRemovalOuterRegion", MSBRegionSubtype.UserEdgeRemovalOuter)
MSBBigJumpSealableRegion = _pair_region("MSBBigJumpSealableRegion", MSBRegionSubtype.BigJumpSealable)

# Smithbox renames at same subtype id as ER.
MSBSourceWaypointRegion = MSBPatrolRoute22Region
MSBFastTravelOverrideRegion = MSBFastTravelRestrictionRegion
MSBWeatherAssetGenerationRegion = MSBWeatherCreateAssetPointRegion
MSBMidRangeEnvMapOutputRegion = MSBEnvironmentMapOutputRegion
MSBBigJumpRegion = MSBMountJumpRegion
MSBSoundDummyRegion = MSBDummyRegion
MSBFallPreventionOverrideRegion = MSBFallPreventionRemovalRegion
MSBBigJumpExitRegion = MSBMountJumpFallRegion
MSBMountOverrideRegion = MSBHorseRideOverrideRegion
MSBHitSettingRegion = MSBHitsetRegion
MSBPatrolPointRegion = MSBPatrolRouteRegion
MSBEnvMapPointRegion = MSBEnvironmentMapPointRegion
MSBEnvMapEffectBoxRegion = MSBEnvironmentMapEffectBoxRegion
MSBWindPlacementRegion = MSBWindAreaRegion
MSBMapConnectionRegion = MSBConnectionRegion
MSBSFXRegion = MSBVFXRegion
MSBWindSFXRegion = MSBWindVFXRegion
MSBAutoDrawGroupSampleRegion = MSBAutoDrawGroupPointRegion
