"""Helpers for resolving Nightreign map MSB paths and map piece instances (Blender POI)."""
from __future__ import annotations

import re
from pathlib import Path
import typing as tp

if tp.TYPE_CHECKING:
    from soulstruct.nightreign.maps.msb import MSB

_TILE_RE = re.compile(r"^m(\d{2})_(\d{2})(?:_\d{2}_\d{2})?$")


def resolve_msb_stem(tile_str: str) -> str:
    """Expand a map tile stem like ``m46_51`` to ``m46_51_00_00``."""
    tile_str = tile_str.strip().lower()
    m = _TILE_RE.match(tile_str)
    if not m:
        raise ValueError(f"Not a map tile stem: {tile_str!r}")
    if tile_str.count("_") >= 3:
        return tile_str
    return f"m{m.group(1)}_{m.group(2)}_00_00"


def find_msb_path(game_root: Path, map_stem: str) -> Path | None:
    """Return ``map/mapstudio/<stem>.msb.dcx`` (or MapStudio) if it exists."""
    stem = resolve_msb_stem(map_stem)
    for sub in ("map/mapstudio", "map/MapStudio"):
        for ext in (".msb.dcx", ".msb"):
            path = game_root / sub / f"{stem}{ext}"
            if path.is_file():
                return path
    return None


def iter_map_piece_instances(msb: MSB) -> list[tuple[str, tp.Any, tp.Any, tp.Any]]:
    """Return ``(model_name, translate, rotate, scale)`` for each map piece part."""
    out: list[tuple[str, tp.Any, tp.Any, tp.Any]] = []
    for piece in msb.map_pieces:
        model_name = piece.model.name if piece.model else ""
        out.append((model_name, piece.translate, piece.rotate, piece.scale))
    return out
