Packaging and installing the Kodi addon

- Build the zip: run `python3 scripts/package_addon.py` from the repository root.
- The script reads `src/addon.xml` to determine the addon id and version and writes the zip to `dist/`.
- Install in Kodi: Settings → Add-ons → Install from zip file → select the zip in `dist/`.

Notes
- The repository keeps working sources in `src/`. The produced zip contains a top-level folder named by the addon id (e.g. `plugin.video.einthusan`).
