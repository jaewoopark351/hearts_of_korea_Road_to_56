#!/usr/bin/env python3
"""Materialize the reviewed HOK base plus the selected Korean update.

Gameplay inputs use immutable Git objects. The separately reviewed artwork
uses an explicit hash-pinned working-tree snapshot; neither source is modified.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from functools import lru_cache
from pathlib import Path

# [2026-09-22]_kpopmodder: Pin the old donor and selected Korean commits separately.
REPO_ROOT = Path(__file__).resolve().parents[1]
DONOR_ROOT = Path(r"C:\hoi\hearts_of_korea")
LOCK_PATH = Path(__file__).with_name("hok_source_lock.json")
HOK_ROOT = REPO_ROOT / ".local-artifacts/sources/hok-887930f-korea-118d7b5"
BASE_COMMIT = "887930f6e88c80568d62dab9cfbe1ba8a498a252"
CONTENT_COMMIT = "da815305e3ce00186a487b3a378bf8536ff59146"
UPDATE_COMMIT = "118d7b53dfdbc120fcfe4b9d6792e66b2b519be7"
AI_PATH = "common/ai_strategy_plans/KOR_historical_strategy_plan.txt"

# [2026-09-22]_kpopmodder: Keep uncommitted artwork provenance separate from the immutable gameplay base.
ICON_LOCK_PATH = Path(__file__).with_name("hok_icon_lock.json")
ICON_ROOT = REPO_ROOT / ".local-artifacts/sources/hok-icons-20260922"
ICON_MANIFEST = "docs/data/HOK_KOREAN_FOCUS_ICON_MANIFEST.json"


@lru_cache(maxsize=1)
def icon_lock() -> dict:
    lock = json.loads(ICON_LOCK_PATH.read_text(encoding="utf-8"))
    if (lock["format"], lock["source_kind"], lock["base_commit"]) != (
        1, "uncommitted-working-tree", "698b6eb160efbaa04a4d43846330ba002f5e8cc7"
    ):
        raise ValueError("unreviewed artwork source-lock revision")
    if len(lock["runtime_assets"]) != 92 or len(lock["reference_inputs"]) != 4:
        raise ValueError("expected 89 textures, three registries and four reference inputs")
    for relative in icon_records(lock):
        path = Path(relative)
        if path.is_absolute() or ".." in path.parts or "\\" in relative:
            raise ValueError(f"unsafe artwork source path: {relative}")
    return lock


def icon_records(lock: dict | None = None) -> dict:
    lock = icon_lock() if lock is None else lock
    return {relative: record for group in ("runtime_assets", "reference_inputs", "documentation")
            for relative, record in lock[group].items()}


def read_icon_source(relative: str | Path) -> bytes:
    relative = Path(relative).as_posix()
    record = icon_records()[relative]
    data = (ICON_ROOT / relative).read_bytes()
    if len(data) != record["size"] or sha256(data) != record["sha256"]:
        raise ValueError(f"artwork source drift: {relative}")
    return data


def ensure_icon_snapshot(check_only: bool = False) -> int:
    records = icon_records()
    existing = {path.relative_to(ICON_ROOT).as_posix() for path in ICON_ROOT.rglob("*") if path.is_file()}
    if existing - set(records):
        raise ValueError(f"unexpected artwork cache files: {sorted(existing - set(records))}")
    pending = {}
    for relative, record in records.items():
        target = ICON_ROOT / relative
        if target.exists():
            read_icon_source(relative)
            continue
        if check_only:
            raise ValueError(f"artwork cache missing: {relative}; run source_snapshot.py --import-icons")
        data = (DONOR_ROOT / relative).read_bytes()
        if len(data) != record["size"] or sha256(data) != record["sha256"]:
            raise ValueError(f"donor artwork differs from reviewed snapshot: {relative}")
        pending[relative] = data
    # Preflight every source before materializing any new cache file.
    for relative, data in pending.items():
        target = ICON_ROOT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as handle:
            handle.write(data)
    return len(pending)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


@lru_cache(maxsize=1)
def source_lock() -> dict:
    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    if (lock["format"], lock["base_commit"], lock["content_commit"], lock["update_commit"]) != (
        1, BASE_COMMIT, CONTENT_COMMIT, UPDATE_COMMIT
    ):
        raise ValueError("unreviewed donor source-lock revision")
    if len(lock["base"]) != 1014 or len(lock["overlay"]) != 20:
        raise ValueError("unexpected donor source-lock inventory")
    for relative in set(lock["base"]) | set(lock["overlay"]):
        path = Path(relative)
        if path.is_absolute() or ".." in path.parts or "\\" in relative:
            raise ValueError(f"unsafe source path: {relative}")
    return lock


FOCUS_UPDATE_PATHS = tuple(source_lock()["overlay"])


def source_record(relative: str | Path, *, updated: bool = True) -> dict:
    relative = Path(relative).as_posix()
    lock = source_lock()
    if updated and relative in lock["overlay"]:
        return {**lock["overlay"][relative], "commit": UPDATE_COMMIT if relative == AI_PATH else CONTENT_COMMIT}
    return {**lock["base"][relative], "commit": BASE_COMMIT}


def checkout_bytes(payload: bytes, record: dict) -> bytes:
    mode = record["checkout"]
    if mode == "raw":
        result = payload
    elif mode == "lf":
        result = payload.replace(b"\r\n", b"\n")
    elif mode == "crlf":
        result = payload.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
    elif mode == "crlf_except":
        lf_lines = set(record["lf_lines"])
        lines = payload.replace(b"\r\n", b"\n").splitlines(keepends=True)
        result = b"".join(line if index in lf_lines else line.replace(b"\n", b"\r\n") for index, line in enumerate(lines))
    else:
        raise ValueError(f"unknown checkout mode: {mode}")
    if sha256(result) != record["sha256"]:
        raise ValueError(f"source checkout hash mismatch: {record['blob']}")
    return result


def git_command() -> list[str]:
    return ["git", "-c", f"safe.directory={DONOR_ROOT.as_posix()}", "-C", str(DONOR_ROOT)]


@lru_cache(maxsize=1)
def verify_provenance() -> None:
    # [2026-09-22]_kpopmodder: Verify each claimed commit/path against its immutable Git blob.
    trees = {}
    for commit in (BASE_COMMIT, CONTENT_COMMIT, UPDATE_COMMIT):
        rows = subprocess.check_output(git_command() + ["ls-tree", "-rz", "--full-tree", commit])
        tree = {}
        for row in rows.split(b"\0"):
            if not row:
                continue
            meta, relative = row.split(b"\t", 1)
            mode, kind, blob = meta.decode().split()
            if kind == "blob" and mode in ("100644", "100755"):
                tree[relative.decode("utf-8")] = blob
        trees[commit] = tree
    lock = source_lock()
    for updated, records in ((False, lock["base"]), (True, lock["overlay"])):
        for relative in records:
            record = source_record(relative, updated=updated)
            if trees[record["commit"]].get(relative) != record["blob"]:
                raise ValueError(f"source provenance mismatch: {record['commit']}:{relative}")


def read_source_file(relative: str | Path, updated: bool = False) -> bytes:
    verify_provenance()
    record = source_record(relative, updated=updated)
    payload = subprocess.check_output(git_command() + ["cat-file", "blob", record["blob"]])
    return checkout_bytes(payload, record)


def ensure_source_snapshot(check_only: bool = False) -> int:
    verify_provenance()
    lock = source_lock()
    paths = sorted(set(lock["base"]) | set(lock["overlay"]))
    if len(paths) != 1031:
        raise ValueError("effective donor inventory must contain 1031 files")
    existing = {path.relative_to(HOK_ROOT).as_posix() for path in HOK_ROOT.rglob("*") if path.is_file()}
    unexpected = existing - set(paths)
    if unexpected:
        raise ValueError(f"unexpected source cache files: {sorted(unexpected)}")
    changed = 0
    for relative in paths:
        destination = HOK_ROOT / relative
        record = source_record(relative)
        if destination.is_file():
            if sha256(destination.read_bytes()) != record["sha256"]:
                raise ValueError(f"modified source cache; refusing overwrite: {relative}")
            continue
        if check_only:
            raise ValueError(f"source cache missing: {relative}; run tools/source_snapshot.py")
        data = read_source_file(relative, updated=True)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
        changed += 1
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--import-icons", action="store_true", help="materialize the reviewed artwork bytes without changing donor files")
    args = parser.parse_args()
    changed = ensure_source_snapshot(check_only=args.check)
    print(f"HOK source snapshot: 1014 base + 20 selected overlay = 1031 files; created {changed}")
    icon_changes = ensure_icon_snapshot(check_only=not args.import_icons or args.check)
    print(f"HOK artwork snapshot: 92 assets + 4 reference inputs + documentation; created {icon_changes}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
