"""Load a real Nightreign MSB after BHD5 AES decrypt (not UFdk ciphertext)."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from soulstruct.dcx import DCXType
from soulstruct.nightreign.maps import MSB
from soulstruct.nightreign.maps import poi_map_pieces

from tests.nightreign._paths import find_msb, is_encrypted

MSB_PATH = find_msb("m46_51_00_00", "m30_30_00_00")


def _msb_available() -> bool:
    return MSB_PATH is not None and MSB_PATH.is_file() and not is_encrypted(MSB_PATH)


class NightreignMSBTest(unittest.TestCase):

    def test_resolve_msb_stem(self):
        self.assertEqual(poi_map_pieces.resolve_msb_stem("m46_51"), "m46_51_00_00")
        self.assertEqual(poi_map_pieces.resolve_msb_stem("m46_51_00_00"), "m46_51_00_00")

    def test_empty_roundtrip(self):
        msb = MSB()
        msb.dcx_type = DCXType.Null
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "empty.msb"
            msb.write(path)
            reloaded = MSB.from_path(path)
            self.assertEqual(len(reloaded.map_pieces), 0)
            for subtype in MSB.get_subtype_list_names():
                self.assertEqual(len(msb[subtype]), len(reloaded[subtype]))

    @unittest.skipUnless(_msb_available(), "decrypted NR MSB missing — run NrUnpackCli with ReadFileOrThrow")
    def test_load_staging_msb(self):
        self.assertFalse(is_encrypted(MSB_PATH), f"{MSB_PATH} is still AES ciphertext (UFdk)")
        magic = MSB_PATH.read_bytes()[:4]
        self.assertIn(magic, {b"DCX\0", b"MSB "}, f"unexpected magic {magic!r} in {MSB_PATH}")
        msb = MSB.from_path(MSB_PATH)
        self.assertTrue(
            len(msb.map_pieces) > 0 or len(msb.map_piece_models) > 0
            or len(msb.assets) > 0 or len(msb.asset_models) > 0,
            f"no map pieces or assets in {MSB_PATH}",
        )

    @unittest.skipUnless(_msb_available(), "decrypted NR MSB missing — run NrUnpackCli with ReadFileOrThrow")
    def test_staging_roundtrip(self):
        msb = MSB.from_path(MSB_PATH)
        msb.dcx_type = DCXType.Null
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "roundtrip.msb"
            msb.write(path)
            reloaded = MSB.from_path(path)
            for subtype in MSB.get_subtype_list_names():
                self.assertEqual(len(msb[subtype]), len(reloaded[subtype]))

    @unittest.skipUnless(_msb_available(), "decrypted NR MSB missing — run NrUnpackCli with ReadFileOrThrow")
    def test_small_base_attach_if_present(self):
        msb = MSB.from_path(MSB_PATH)
        if not msb.small_base_attachs:
            self.skipTest("no SmallBaseAttach regions in this map")
        region = msb.small_base_attachs[0]
        self.assertEqual(region.SUBTYPE_ENUM.value, 54)


if __name__ == "__main__":
    unittest.main()
