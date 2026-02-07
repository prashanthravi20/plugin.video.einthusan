#!/usr/bin/env python3
"""Build a Kodi repository package from top-level addon folders.

Creates in `dist/`:
- `addons.xml` (combined addon entries)
- `addons.xml.md5`
- `repository.einthusan-1.0.0.zip` (contains addons.xml, md5, and addon folders)

Usage: python3 scripts/build_repo.py
"""
from pathlib import Path
import hashlib
import zipfile
import os

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
DIST.mkdir(exist_ok=True)

# find top-level addon folders (contain addon.xml)
addons = []
for p in ROOT.iterdir():
    if p.is_dir():
        if (p / "addon.xml").exists():
            addons.append(p)

if not addons:
    raise SystemExit("No addon folders with addon.xml found at repository root")

def read_addon_xml(folder: Path) -> str:
    data = (folder / "addon.xml").read_text(encoding="utf-8")
    # strip XML declaration if present
    if data.lstrip().startswith("<?xml"):
        idx = data.find("?>")
        if idx != -1:
            data = data[idx+2:]
    return data.strip()

parts = []
for a in sorted(addons):
    parts.append(read_addon_xml(a))

addons_xml = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<addons>\n" + "\n".join(parts) + "\n</addons>\n"

addons_xml_path = DIST / "addons.xml"
addons_xml_path.write_text(addons_xml, encoding="utf-8")

# md5
md5 = hashlib.md5(addons_xml.encode("utf-8")).hexdigest()
(DIST / "addons.xml.md5").write_text(md5, encoding="utf-8")

repo_name = "repository.einthusan-1.0.0.zip"
repo_path = DIST / repo_name

with zipfile.ZipFile(repo_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
    # include the addons.xml and its md5 at repo root
    z.write(addons_xml_path, "addons.xml")
    z.write(DIST / "addons.xml.md5", "addons.xml.md5")
    # include each addon folder (recursively)
    for a in sorted(addons):
        for p in a.rglob("*"):
            if p.is_file():
                # arcname should be the folder name + relative path
                rel = p.relative_to(ROOT)
                arc = str(rel).replace(os.path.sep, "/")
                z.write(p, arc)

print(f"Built repository files in {DIST} and created {repo_path}")
