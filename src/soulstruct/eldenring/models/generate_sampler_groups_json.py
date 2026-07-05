from __future__ import annotations

import argparse
import logging
from pathlib import Path

from soulstruct.base.models.matbin import MATBIN, MATBINBND
from soulstruct.config import Config
from soulstruct.containers import Binder, BinderEntry, EntryNotFoundError
from soulstruct.utilities.binary import BinaryReader
from soulstruct.utilities.files import SOULSTRUCT_PATH, read_json, write_json

_LOGGER = logging.getLogger(__name__)

RESOURCES_DIR = SOULSTRUCT_PATH("eldenring/models/resources")
ER_SHADER_SAMPLER_GROUPS_PATH = RESOURCES_DIR / "er_shader_sampler_groups.json"
NR_SHADER_SAMPLER_GROUPS_PATH = RESOURCES_DIR / "nr_shader_sampler_groups.json"


def load_shaderbdle_binder(game_root: Path) -> Binder:
    """Load and merge base + DLC shaderbdle binders from a game install."""
    shaderbdle_paths = [
        game_root / "shader/shaderbdle.shaderbdlebnd.dcx",
        game_root / "shader/shaderbdle_dlc01.shaderbdlebnd.dcx",
        game_root / "shader/shaderbdle_dlc02.shaderbdlebnd.dcx",
    ]
    existing_paths = [path for path in shaderbdle_paths if path.is_file()]
    if not existing_paths:
        raise FileNotFoundError(f"No shaderbdle binders found under {game_root / 'shader'}")

    shaderbdlebnd = Binder.from_path(existing_paths[0])
    entries_by_name = shaderbdlebnd.get_entries_by_name()
    for path in existing_paths[1:]:
        for entry in Binder.from_path(path).entries:
            if entry.name in entries_by_name:
                shaderbdlebnd.remove_entry_name(entry.name)
            shaderbdlebnd.entries.append(entry)
            entries_by_name[entry.name] = entry
    return shaderbdlebnd


def load_game_matbinbnds(game_root: Path) -> list[MATBINBND]:
    """Load MATBINBND binders from a game install's material directory."""
    matbinbnd_paths = [
        game_root / "material/allmaterial.matbinbnd.dcx",
        game_root / "material/allmaterial_dlc01.matbinbnd.dcx",
    ]
    matbinbnds = []
    for path in matbinbnd_paths:
        if path.is_file():
            matbinbnds.append(MATBINBND.from_path(path))
    if not matbinbnds:
        raise FileNotFoundError(f"No MATBINBND files found under {game_root / 'material'}")
    return matbinbnds


def iter_matbins(matbinbnds: list[MATBINBND]):
    """Yield unique MATBIN entries by shader stem across multiple MATBINBND binders."""
    seen_shader_stems: set[str] = set()
    for matbinbnd in matbinbnds:
        for matbin_entry in matbinbnd.entries:
            matbin = MATBIN.from_binder_entry(matbin_entry)
            shader_stem = matbin.shader_stem
            if shader_stem in seen_shader_stems:
                continue
            seen_shader_stems.add(shader_stem)
            yield matbin


def collect_shader_sampler_groups(
    matbinbnd: MATBINBND | list[MATBINBND],
    shaderbdlebnd: Binder,
) -> tuple[dict[str, dict[str, list[tuple[str, str]]]], dict[str, dict[str, list[str]]]]:
    """Collect sampler groups and summaries for all shaders referenced by MATBIN entries."""
    if isinstance(matbinbnd, list):
        matbins = list(iter_matbins(matbinbnd))
    else:
        matbins = [MATBIN.from_binder_entry(entry) for entry in matbinbnd.entries]

    all_shader_sampler_groups: dict[str, dict[str, list[tuple[str, str]]]] = {}
    shader_group_summaries: dict[str, dict[str, list[str]]] = {}

    for matbin in matbins:
        shader_stem = matbin.shader_stem
        if shader_stem in all_shader_sampler_groups:
            continue

        print(f"Finding metaparam for shader {shader_stem}...")
        try:
            shaderbdle_entry = shaderbdlebnd.find_entry_by_name(f"{shader_stem}.shaderbdle")
        except EntryNotFoundError:
            print(f"  No shaderbdle entry found for {shader_stem}.")
            continue

        shaderbdle = Binder.from_binder_entry(shaderbdle_entry)
        metaparam_entry = shaderbdle.find_entry_by_name(f"{shader_stem}.metaparam")
        try:
            shader_sampler_groups = read_metaparam(metaparam_entry)
        except (ValueError, EntryNotFoundError) as ex:
            print(f"  Failed to read metaparam for {shader_stem}: {ex}")
            continue
        if not shader_sampler_groups:
            continue

        shader_sampler_groups = {
            group_name: shader_sampler_groups[group_name]
            for group_name in sorted(
                shader_sampler_groups,
                key=lambda x: int(x.removeprefix("group_")) if x else 1E9,
            )
        }
        all_shader_sampler_groups[shader_stem] = shader_sampler_groups

        shader_group_summaries[shader_stem] = {}
        shader_prefix = shader_stem.replace("][", "_").replace("[", "_").replace("]", "_")
        for group_name, samplers in shader_sampler_groups.items():
            short_sampler_names = []
            for sampler_name, default_texture_name in samplers:
                short_name = sampler_name.removeprefix(shader_prefix)
                short_name = short_name.removeprefix("_snp_Texture2D_")
                if default_texture_name and "SYSTEX" not in default_texture_name:
                    short_name += f" == {default_texture_name}"
                short_sampler_names.append(short_name)
            shader_group_summaries[shader_stem][group_name] = short_sampler_names

    all_shader_sampler_groups = dict(sorted(all_shader_sampler_groups.items()))
    shader_group_summaries = dict(sorted(shader_group_summaries.items()))
    return all_shader_sampler_groups, shader_group_summaries


def generate_metaparam(game_root: Path):
    """Regenerate the full ER shader sampler groups JSON from bundled ER MATBINBND + game shaderbdle."""
    matbinbnd = MATBINBND.from_bundled("ELDEN_RING")
    shaderbdlebnd = load_shaderbdle_binder(game_root)
    all_shader_sampler_groups, shader_group_summaries = collect_shader_sampler_groups(matbinbnd, shaderbdlebnd)

    write_json(ER_SHADER_SAMPLER_GROUPS_PATH, all_shader_sampler_groups, indent=4)
    write_json(RESOURCES_DIR / "er_shader_sampler_groups_summary.json", shader_group_summaries, indent=4)


def generate_nr_overlay(game_root: Path):
    """Generate NR-only shader sampler groups not already present in the ER JSON."""
    er_shader_sampler_groups = read_json(ER_SHADER_SAMPLER_GROUPS_PATH)
    matbinbnds = load_game_matbinbnds(game_root)
    shaderbdlebnd = load_shaderbdle_binder(game_root)
    all_shader_sampler_groups, shader_group_summaries = collect_shader_sampler_groups(matbinbnds, shaderbdlebnd)

    scanned = len(all_shader_sampler_groups)
    nr_shader_sampler_groups = {
        shader_stem: sampler_groups
        for shader_stem, sampler_groups in all_shader_sampler_groups.items()
        if shader_stem not in er_shader_sampler_groups
    }
    skipped_existing = scanned - len(nr_shader_sampler_groups)

    nr_shader_group_summaries = {
        shader_stem: shader_group_summaries[shader_stem]
        for shader_stem in nr_shader_sampler_groups
    }

    write_json(NR_SHADER_SAMPLER_GROUPS_PATH, nr_shader_sampler_groups, indent=4)
    write_json(RESOURCES_DIR / "nr_shader_sampler_groups_summary.json", nr_shader_group_summaries, indent=4)

    print(
        f"NR overlay: scanned {scanned} unique shaders, "
        f"added {len(nr_shader_sampler_groups)} new entries, "
        f"skipped {skipped_existing} already in ER JSON."
    )


def read_metaparam(metaparam_entry: BinderEntry) -> dict[str, list[tuple[str, str]]]:
    """Read metaparam data as a dictionary mapping sampler group names to lists of sampler names with their default
    texture paths ('SYSTEX' stuff usually).

    Note that an empty group name key may exist.
    """
    metaparam = BinaryReader(metaparam_entry.get_uncompressed_data())

    shader_dict = {}
    metaparam.seek(0xC)
    sampler_count = metaparam.unpack_value("i")
    for i in range(sampler_count):
        metaparam.seek(0x98 + (0x30 * i))
        sampler_name_offset = metaparam.unpack_value("q")
        metaparam.seek(8, 1)
        default_texture_path_offset = metaparam.unpack_value("q")
        sampler_group_name_offset = metaparam.unpack_value("q")

        sampler_name = metaparam.unpack_string(offset=sampler_name_offset, encoding="utf-16-le")
        default_texture_path = metaparam.unpack_string(offset=default_texture_path_offset, encoding="utf-16-le")
        group_name = metaparam.unpack_string(offset=sampler_group_name_offset, encoding="utf-16-le")  # could be empty

        shader_dict.setdefault(group_name, []).append((sampler_name, default_texture_path))

    return shader_dict


def main():
    parser = argparse.ArgumentParser(description="Generate Elden Ring / Nightreign shader sampler group JSON.")
    parser.add_argument(
        "--game-root",
        type=Path,
        default=Config.ER_PATH,
        help="Path to the game 'Game' directory containing shader/ and material/ folders.",
    )
    parser.add_argument(
        "--nr-overlay",
        action="store_true",
        help="Write NR-only shader entries to nr_shader_sampler_groups.json (does not modify ER JSON).",
    )
    args = parser.parse_args()

    if args.nr_overlay:
        generate_nr_overlay(args.game_root)
    else:
        generate_metaparam(args.game_root)


if __name__ == "__main__":
    main()
