#!/usr/bin/env python3
"""Package the addon under src/ into a Kodi-installable zip.

Usage: python3 scripts/package_addon.py
Creates: dist/<addon-id>-<version>.zip
Supports an optional `.packageignore` file at the repository root with glob
patterns (one per line) to exclude from the produced zip and from extraction.
"""
import os
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
import fnmatch

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
ADDON_XML = SRC / "addon.xml"
PACKAGE_IGNORE = ROOT / ".packageignore"

if not ADDON_XML.exists():
    raise SystemExit(f"Missing addon.xml at {ADDON_XML}")

def read_packageignore(path: Path):
    if not path.exists():
        return []
    patterns = []
    for line in path.read_text().splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        patterns.append(s)
    return patterns

try:
    tree = ET.parse(ADDON_XML)
    root = tree.getroot()
    addon_id = root.attrib.get("id") or "plugin.video.addon"
    version = root.attrib.get("version") or "0.0.0"
except Exception as e:
    raise SystemExit(f"Failed to parse addon.xml: {e}")

exclude_patterns = read_packageignore(PACKAGE_IGNORE)

def is_excluded(rel_path: Path):
    s = str(rel_path).replace(os.path.sep, "/")
    for pat in exclude_patterns:
        if fnmatch.fnmatch(s, pat) or fnmatch.fnmatch(s, f"*/{pat}"):
            return True
    return False

addon_folder = addon_id
DIST = ROOT / "dist"
DIST.mkdir(exist_ok=True)
zip_name = f"{addon_folder}-{version}.zip"
zip_path = DIST / zip_name

with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
    for p in SRC.rglob("*"):
        if p.is_file():
            rel = p.relative_to(SRC)
            if is_excluded(rel):
                continue
            arcname = Path(addon_folder) / rel
            # Force forward slashes for zip
            z.write(p, str(arcname).replace(os.path.sep, "/"))

print(f"Created {zip_path}")

# Also create an extracted addon folder at repository root for direct copy-install
EXTRACT_TO = ROOT / addon_folder
if EXTRACT_TO.exists():
    # don't remove, but update contents
    pass
else:
    EXTRACT_TO.mkdir()

for p in SRC.rglob("*"):
    rel = p.relative_to(SRC)
    if p.is_dir():
        (EXTRACT_TO / rel).mkdir(parents=True, exist_ok=True)
        continue
    if is_excluded(rel):
        continue
    target = EXTRACT_TO / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    with p.open("rb") as rf, target.open("wb") as wf:
        wf.write(rf.read())

print(f"Extracted addon to {EXTRACT_TO}")
