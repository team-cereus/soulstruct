"""Describes the structure of a GEOMBND Binder."""
from __future__ import annotations

__all__ = [
    "GEOMBND",
    "aeg_model_stem",
    "aeg_geombnd_relative_path",
    "find_aeg_geombnd",
]

import re
import typing as tp
from dataclasses import field
from pathlib import Path

from soulstruct.containers import BinderVersion, BinderVersion4Info
from soulstruct.containers.binder_types import FLVERBinder
from soulstruct.dcx import DCXType
from soulstruct.games import ELDEN_RING

# On-disk AEG stem: aeg001_290 (MSB names are typically AEG001_290).
_AEG_STEM_RE = re.compile(r"^aeg\d{3}_\d{3}$", re.IGNORECASE)
_AEG_STRIP_SUFFIXES = (
    ".flver.dcx",
    ".flver",
    ".geombnd.dcx",
    ".geombnd",
)


class GEOMBND(FLVERBinder):

    DEFAULT_ENTRY_ROOT: tp.ClassVar[str] = f"{ELDEN_RING.interroot_prefix}\\asset\\aeg"
    TPF_ENTRY_ID: tp.ClassVar[int] = -1

    dcx_type: DCXType = ELDEN_RING.default_dcx_type
    version: BinderVersion = BinderVersion.V4
    v4_info: BinderVersion4Info = field(default_factory=BinderVersion4Info.eldenring_default)

    def get_tpf_entry_path(self, model_stem: str) -> str:
        raise TypeError("GEOMBND does not contain TPF files. These are in `asset/aet` TPFs.")

    def get_flver_entry_path(self, model_stem: str) -> str:
        """Note more complicated path for AEG."""
        return f"{self.DEFAULT_ENTRY_ROOT}\\{model_stem[:6]}\\{model_stem}\\sib\\{model_stem}.flver"


def aeg_model_stem(model_name: str) -> str:
    """Normalize an MSB/asset name (``AEG001_290``) to the on-disk stem (``aeg001_290``)."""
    stem = Path(str(model_name).strip()).name
    lowered = stem.lower()
    for suffix in _AEG_STRIP_SUFFIXES:
        if lowered.endswith(suffix):
            stem = stem[: -len(suffix)]
            break
    return stem.lower()


def aeg_geombnd_relative_path(model_name: str) -> Path:
    """Return ``asset/aeg/aeg001/aeg001_290.geombnd.dcx`` for ``AEG001_290``.

    Matches Elden Ring / Nightreign UXM layout and Blender ``ImportAssetFLVER`` /
    ``ImportAssetHKXAnimation`` (``asset/aeg/{category}/{stem}.geombnd``).
    """
    stem = aeg_model_stem(model_name)
    if not _AEG_STEM_RE.match(stem):
        raise ValueError(f"Not an AEG model name: {model_name!r}")
    return Path("asset") / "aeg" / stem[:6] / f"{stem}.geombnd.dcx"


def find_aeg_geombnd(game_root: Path | str, model_name: str) -> Path | None:
    """Locate a GEOMBND for ``model_name`` under ``game_root`` (with or without ``.dcx``)."""
    try:
        relative = aeg_geombnd_relative_path(model_name)
    except ValueError:
        return None
    root = Path(game_root)
    candidates = (
        root / relative,
        root / relative.with_name(relative.name.removesuffix(".dcx")),
    )
    for path in candidates:
        if path.is_file():
            return path
    return None
