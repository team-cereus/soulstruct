"""Locate AES-decrypted Nightreign unpack files for tests."""
from __future__ import annotations

from pathlib import Path

DECRYPTED_ROOT = Path(r"S:/_modding/tools/soulstruct-blender/_tmp/nr-full-unpack-decrypted")
STAGING_ROOT = Path(r"S:/_modding/tools/soulstruct-blender/_tmp/nr-full-unpack")
POC_MSB = Path(r"S:/_modding/tools/soulstruct-blender/_tmp/msb-test-out/m46_51_00_00.msb")
POC_MAPBND = Path(r"S:/_modding/tools/soulstruct-blender/_tmp/msb-test-out/m10_00_00_00_100000.mapbnd")

# AES ciphertext of DCX\0 — not a codec. Tests must not treat these as loadable.
_ENCRYPTED_MAGICS = {b"UFdk", b"\xaf\xb9\x8a\x0b"}


def is_encrypted(path: Path) -> bool:
    if not path.is_file():
        return False
    return path.read_bytes()[:4] in _ENCRYPTED_MAGICS


def _usable(path: Path | None) -> Path | None:
    if path is None or not path.is_file():
        return None
    if is_encrypted(path):
        return None
    return path


def find_msb(*stems: str) -> Path | None:
    """Return first decrypted MSB for any of the given stems (``m46_51_00_00``)."""
    if not stems:
        stems = ("m46_51_00_00", "m30_30_00_00")
    for stem in stems:
        for root in (DECRYPTED_ROOT, STAGING_ROOT):
            found = _usable(root / "map" / "mapstudio" / f"{stem}.msb.dcx")
            if found is None:
                found = _usable(root / "map" / "mapstudio" / f"{stem}.msb")
            if found is not None:
                return found
    return _usable(POC_MSB)


def find_mapbnd() -> Path | None:
    """Return a decrypted mapbnd (prefer m34, then any under map/)."""
    for root in (DECRYPTED_ROOT, STAGING_ROOT):
        map_root = root / "map"
        if not map_root.is_dir():
            continue
        preferred = sorted(map_root.glob("m34/**/*.mapbnd*"))
        others = sorted(map_root.glob("**/*.mapbnd*"))
        for path in preferred + others:
            if _usable(path) is not None:
                return path
    return _usable(POC_MAPBND)


def unpack_root_for_poi() -> Path | None:
    """Root that has a decrypted mapstudio MSB (for find_msb_path)."""
    for root in (DECRYPTED_ROOT, STAGING_ROOT):
        if find_msb("m46_51_00_00", "m30_30_00_00") and (
            (root / "map" / "mapstudio").is_dir()
        ):
            # Prefer the root that actually contains the decrypted file.
            for stem in ("m46_51_00_00", "m30_30_00_00"):
                if _usable(root / "map" / "mapstudio" / f"{stem}.msb.dcx") is not None:
                    return root
                if _usable(root / "map" / "mapstudio" / f"{stem}.msb") is not None:
                    return root
    return None
