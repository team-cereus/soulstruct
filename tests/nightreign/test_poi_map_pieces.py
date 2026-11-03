"""POI helpers against a real decrypted Nightreign MSB."""
from __future__ import annotations

import unittest

from soulstruct.nightreign.maps import MSB
from soulstruct.nightreign.maps import poi_map_pieces

from tests.nightreign._paths import find_msb, is_encrypted, unpack_root_for_poi

MSB_PATH = find_msb("m46_51_00_00", "m30_30_00_00")
UNPACK_ROOT = unpack_root_for_poi()


def _msb_available() -> bool:
    return MSB_PATH is not None and MSB_PATH.is_file() and not is_encrypted(MSB_PATH)


class NightreignPoiMapPiecesTest(unittest.TestCase):

    def test_resolve_msb_stem(self):
        self.assertEqual(poi_map_pieces.resolve_msb_stem("m46_51"), "m46_51_00_00")
        self.assertEqual(poi_map_pieces.resolve_msb_stem("m30_30"), "m30_30_00_00")
        self.assertEqual(poi_map_pieces.resolve_msb_stem("m30_30_00_00"), "m30_30_00_00")

    @unittest.skipUnless(UNPACK_ROOT is not None, "decrypted mapstudio root missing")
    def test_find_msb_path(self):
        path = poi_map_pieces.find_msb_path(UNPACK_ROOT, "m46_51")
        if path is None:
            path = poi_map_pieces.find_msb_path(UNPACK_ROOT, "m30_30")
        self.assertIsNotNone(path)
        assert path is not None
        self.assertFalse(is_encrypted(path), f"{path} is still AES ciphertext")

    @unittest.skipUnless(_msb_available(), "decrypted NR MSB missing — run NrUnpackCli with ReadFileOrThrow")
    def test_iter_map_piece_instances(self):
        msb = MSB.from_path(MSB_PATH)
        pieces = poi_map_pieces.iter_map_piece_instances(msb)
        self.assertGreater(len(pieces), 0, f"no map pieces in {MSB_PATH.name}")
        named = [name for name, _t, _r, _s in pieces if name]
        self.assertGreater(len(named), 0, "map pieces have no model names")
        for name in named[:8]:
            self.assertTrue(name.startswith("m") or name.startswith("AEG") or name.startswith("aeg"), name)
        aeg_names = poi_map_pieces.unique_aeg_model_names(msb)
        if aeg_names:
            self.assertTrue(aeg_names[0].upper().startswith("AEG"), aeg_names[0])


if __name__ == "__main__":
    unittest.main()
