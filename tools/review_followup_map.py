"""Apply the reviewed one-row inland floating-harbor placement correction."""

from __future__ import annotations

from pathlib import PurePath


MAP_PATH = "map/buildings.txt"
RAW_OLD_ROW = b"1153;floating_harbor;4725.00;9.50;1289.00;-4.47;10065"
ROW_COUNT_DELTA = -1


#20261109_kpopmodder: Remove only the exact inherited harbor marker whose linked province is inland in the approved HOK map.
def apply_map(relative: str | PurePath, data: bytes) -> bytes:
    """Remove the current invalid row; the caller owns hashes and idempotence."""
    if str(relative).replace("\\", "/") != MAP_PATH:
        return data

    if data.count(b"1153;floating_harbor;") != 1:
        raise ValueError("expected one unambiguous inland floating-harbor marker")
    rows = data.splitlines(keepends=True)
    candidates = [
        index
        for index, row in enumerate(rows)
        if row.split(b";", 2)[:2] == [b"1153", b"floating_harbor"]
    ]
    if len(candidates) != 1:
        raise ValueError("expected exactly one reviewed inland floating-harbor row")
    index = candidates[0]
    if rows[index] != RAW_OLD_ROW + b"\r\n":
        raise ValueError("unreviewed inland floating-harbor placement bytes")
    return b"".join(rows[:index] + rows[index + 1:])
