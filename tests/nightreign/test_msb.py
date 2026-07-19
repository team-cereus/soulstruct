import os
import tempfile
import unittest
from pathlib import Path

from soulstruct.dcx import DCXType
from soulstruct.nightreign.maps import MSB
from soulstruct.nightreign.maps import poi_map_pieces

STAGING_MSB = Path(r"S:/_modding/tools/soulstruct-blender/_tmp/nr-full-unpack/map/mapstudio/m46_51_00_00.msb.dcx")


def _staging_available() -> bool:
    return STAGING_MSB.is_file()


def _is_ufdk_compressed(path: Path) -> bool:
    return path.read_bytes()[:4] == b"UFdk"


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

    @unittest.skipUnless(_staging_available(), "staging MSB missing")
    def test_load_staging_msb(self):
        if _is_ufdk_compressed(STAGING_MSB):
            self.skipTest("staging file uses UFdk compression (not yet supported by soulstruct.dcx)")
        msb = MSB.from_path(STAGING_MSB)
        self.assertTrue(len(msb.map_pieces) > 0 or len(msb.map_piece_models) > 0)

    @unittest.skipUnless(_staging_available(), "staging MSB missing")
    def test_staging_roundtrip(self):
        if _is_ufdk_compressed(STAGING_MSB):
            self.skipTest("staging file uses UFdk compression (not yet supported by soulstruct.dcx)")
        msb = MSB.from_path(STAGING_MSB)
        msb.dcx_type = DCXType.Null
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "roundtrip.msb"
            msb.write(path)
            reloaded = MSB.from_path(path)
            for subtype in MSB.get_subtype_list_names():
                self.assertEqual(len(msb[subtype]), len(reloaded[subtype]))

    @unittest.skipUnless(_staging_available(), "staging MSB missing")
    def test_small_base_attach_if_present(self):
        if _is_ufdk_compressed(STAGING_MSB):
            self.skipTest("staging file uses UFdk compression (not yet supported by soulstruct.dcx)")
        msb = MSB.from_path(STAGING_MSB)
        if not msb.small_base_attachs:
            self.skipTest("no SmallBaseAttach regions in this map")
        region = msb.small_base_attachs[0]
        self.assertEqual(region.SUBTYPE_ENUM.value, 54)


if __name__ == "__main__":
    unittest.main()
