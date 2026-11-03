"""Load a decrypted Nightreign mapbnd and assert FLVER entries exist."""
from __future__ import annotations

import unittest

from soulstruct.containers import Binder

from tests.nightreign._paths import find_mapbnd, is_encrypted

MAPBND_PATH = find_mapbnd()


def _mapbnd_available() -> bool:
    return MAPBND_PATH is not None and MAPBND_PATH.is_file() and not is_encrypted(MAPBND_PATH)


class NightreignMapbndTest(unittest.TestCase):

    @unittest.skipUnless(_mapbnd_available(), "decrypted NR mapbnd missing — run NrUnpackCli with ReadFileOrThrow")
    def test_binder_contains_flver(self):
        self.assertFalse(is_encrypted(MAPBND_PATH), f"{MAPBND_PATH} is still AES ciphertext")
        magic = MAPBND_PATH.read_bytes()[:4]
        self.assertIn(magic, {b"DCX\0", b"BND4"}, f"unexpected magic {magic!r} in {MAPBND_PATH}")
        binder = Binder.from_path(MAPBND_PATH)
        flver_entries = binder.find_entries_matching_name(r".*\.flver(\.dcx)?")
        self.assertGreater(len(flver_entries), 0, f"no FLVER entries in {MAPBND_PATH.name}")
        data = flver_entries[0].get_uncompressed_data()
        self.assertGreater(len(data), 4)
        self.assertIn(data[:4], {b"FLVER", b"DCX\0", b"FLVE"})


if __name__ == "__main__":
    unittest.main()
