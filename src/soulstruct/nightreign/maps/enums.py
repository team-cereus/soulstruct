from __future__ import annotations

__all__ = [
    "MSBSupertype",
    "MSBModelSubtype",
    "MSBEventSubtype",
    "MSBRegionSubtype",
    "MSBPartSubtype",
    "MSBRouteSubtype",
    "CollisionHitFilter",
]

from soulstruct.eldenring.maps.enums import (
    MSBSupertype,
    MSBModelSubtype,
    MSBPartSubtype,
    MSBRouteSubtype,
    CollisionHitFilter,
    BaseMSBEventSubtype,
    BaseMSBRegionSubtype,
)


class MSBEventSubtype(BaseMSBEventSubtype):
    Treasure = 4
    Generator = 5
    ObjAct = 7
    MapOffset = 9
    PseudoMultiplayer = 12
    PatrolInfo = 14
    PlatoonInfo = 15
    PatrolRouteEvent = 20
    Riding = 21
    AutoDrawGroup = 22
    SignPuddle = 23
    RetryPoint = 24
    BirdRoute = 25
    TalkInfo = 26
    TeamFight = 27
    OtherEvent = -1

    @classmethod
    def get_plural_supertype_name(cls):
        return "Events"


class MSBRegionSubtype(BaseMSBRegionSubtype):
    """Nightreign MSB region (point) subtypes (Smithbox MSB-NR)."""

    EntryPoint = 1
    EnvironmentMapPoint = 2
    RespawnPoint = 3
    Sound = 4
    VFX = 5
    WindVFX = 6
    ReturnPoint = 8
    Message = 9
    EnvironmentMapEffectBox = 17
    WindArea = 18
    Connection = 21
    SourceWaypoint = 22
    StaticWaypoint = 23
    MapGridLayerConnection = 24
    EnemySpawnPoint = 25
    BuddySummonPoint = 26
    RollingObjectOverride = 27
    MufflingBox = 28
    MufflingPortal = 29
    OtherSound = 30
    MufflingPlane = 31
    PatrolRoute = 32
    MapPoint = 33
    SoundState = 34
    MapInfoOverride = 35
    AutoDrawGroupPoint = 36
    MassPlacement = 37
    MapPointDiscoveryOverride = 38
    MapPointParticipationOverride = 39
    Hitset = 40
    FastTravelRestriction = 41
    WeatherCreateAssetPoint = 42
    PlayArea = 43
    EnvironmentMapOutput = 44
    MapVisibilityOverride = 45
    MountJump = 46
    OpenCharacterActivateLimit = 47
    Dummy = 48
    FallPreventionRemoval = 49
    NavmeshCutting = 50
    MapNameOverride = 51
    MountJumpFall = 52
    HorseRideOverride = 53
    SmallBaseAttach = 54
    BirdRoute = 55
    ClearInfo = 56
    RespawnOverride = 57
    UserEdgeRemovalInner = 58
    UserEdgeRemovalOuter = 59
    BigJumpSealable = 60
    OtherRegion = -1

    @classmethod
    def get_plural_supertype_name(cls):
        return "Regions"
