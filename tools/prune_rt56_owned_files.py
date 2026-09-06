#!/usr/bin/env python3
"""Remove donor files whose runtime ownership is explicitly assigned to RT56."""

from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

RT56_OWNED = [
    "common/difficulty_settings/00_difficulty.txt",
    "common/on_actions/04_mtg_on_actions.txt",
    "history/units/JAP_1936_naval.txt",
    "gfx/loadingscreens/load_10.dds",
    "gfx/loadingscreens/load_11.dds",
    # The donor registry would duplicate KOR sound/soundeffect IDs.  The HOK
    # WAV payloads are retained and consumed by the generated single-owner
    # sound/r56_vo_Korean.asset instead.
    "sound/voice_korea.asset",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()

    remaining = []
    for relative in RT56_OWNED:
        path = (ROOT / Path(relative)).resolve()
        path.relative_to(ROOT)
        if path.is_dir():
            raise RuntimeError(f"refusing to remove directory: {path}")
        if path.exists():
            remaining.append(relative)
            if args.apply:
                path.unlink()
                print(f"removed {relative}")
            else:
                print(f"present {relative}")
        else:
            print(f"absent  {relative}")
    if args.check and remaining:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
