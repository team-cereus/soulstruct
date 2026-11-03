"""AEG GEOMBND path resolution and FLVER extract from decrypted Nightreign unpack."""
from __future__ import annotations

import unittest

from soulstruct.containers import Binder
from soulstruct.eldenring.models.geombnd import (
    aeg_geombnd_relative_path,
    aeg_model_stem,
    find_aeg_geombnd,
)
from soulstruct.nightreign.maps import MSB
from soulstruct.nightreign.maps import poi_map_pieces

from tests.nightreign._paths import DECRYPTED_ROOT, is_encrypted

AEG_MODEL = "AEG001_290"
EXPECTED_GEOMBND = DECRYPTED_ROOT / "asset" / "aeg" / "aeg001" / "aeg001_290.geombnd.dcx"
MSB_PATH = DECRYPTED_ROOT / "map" / "mapstudio" / "m30_30_00_00.msb.dcx"


class NightreignAegGeombndTest(unittest.TestCase):

    def test_aeg_geombnd_relative_path(self):
        self.assertEqual(aeg_model_stem("AEG001_290"), "aeg001_290")
        self.assertEqual(
            aeg_geombnd_relative_path("AEG001_290").as_posix(),
            "asset/aeg/aeg001/aeg001_290.geombnd.dcx",
        )
        self.assertEqual(
            aeg_geombnd_relative_path("aeg001_290.geombnd.dcx").as_posix(),
            "asset/aeg/aeg001/aeg001_290.geombnd.dcx",
        )

    def test_aeg001_290_geombnd_yields_flver(self):
        path = find_aeg_geombnd(DECRYPTED_ROOT, AEG_MODEL)
        self.assertIsNotNone(
            path,
            f"missing AEG geombnd: {EXPECTED_GEOMBND}",
        )
        assert path is not None
        self.assertFalse(is_encrypted(path), f"{path} is still AES ciphertext")
        magic = path.read_bytes()[:4]
        self.assertIn(magic, {b"DCX\0", b"BND4"}, f"unexpected magic {magic!r} in {path}")
        binder = Binder.from_path(path)
        flver_entries = binder.find_entries_matching_name(r".*\.flver(\.dcx)?")
        self.assertGreater(len(flver_entries), 0, f"no FLVER entries in {path}")
        from soulstruct.flver import FLVER

        flver = flver_entries[0].to_binary_file(FLVER)
        self.assertTrue(
            len(flver.meshes) > 0 or len(flver.bones) > 0,
            f"FLVER from {path.name} has no meshes or bones",
        )

    def test_m30_30_msb_lists_aeg001_290(self):
        self.assertTrue(MSB_PATH.is_file(), f"missing MSB: {MSB_PATH}")
        self.assertFalse(is_encrypted(MSB_PATH), f"{MSB_PATH} is still AES ciphertext")
        msb = MSB.from_path(MSB_PATH)
        names = poi_map_pieces.unique_aeg_model_names(msb)
        self.assertIn(AEG_MODEL, names, f"{AEG_MODEL} not in {MSB_PATH.name} unique AEG models")
        self.assertGreaterEqual(len(names), 1)


if __name__ == "__main__":
    unittest.main()
