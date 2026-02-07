Packaging and installing the Kodi addon

- Build the zip: run `python3 scripts/package_addon.py` from the repository root.
- The script reads `src/addon.xml` to determine the addon id and version and writes the zip to `dist/`.
- Install in Kodi: Settings → Add-ons → Install from zip file → select the zip in `dist/`.

Notes
- The repository keeps working sources in `src/`. The produced zip contains a top-level folder named by the addon id (e.g. `plugin.video.einthusan`).

Creating a Kodi repository (so Kodi auto-detects updates)

- Build repository files: run `python3 scripts/build_repo.py`. This creates `dist/addons.xml`, `dist/addons.xml.md5`, and `dist/repository.einthusan-1.0.0.zip`.
- Publish the `dist/` contents on GitHub. Recommended approaches:
	- GitHub Pages: push the `dist/` folder to the `gh-pages` branch and enable GitHub Pages. Then the raw URL to `addons.xml` will be https://<user>.github.io/<repo>/addons.xml
	- Raw GitHub: use raw.githubusercontent.com URLs for the `addons.xml` file, but GitHub raw can be rate-limited.
- In Kodi: Add source → enter URL pointing to the hosted `dist/` folder (the URL where `addons.xml` is reachable). Then Add-ons → Install from zip file → Add-on browser → install `repository.einthusan-1.0.0.zip` from that source.

How updates work

- When you push a new release or update `addons.xml` on GitHub Pages, Kodi periodically checks the repository URL for changes in `addons.xml`. When it sees a new version number for an installed add-on, it offers an update.

Notes and tips

- Ensure `addons.xml` and `addons.xml.md5` are at the root of the hosted URL. Kodi expects those filenames.
- Keep the repository zip named like `repository.<name>-<version>.zip` and include the add-on folders inside the zip (not nested under another folder).
- You can automate running `scripts/build_repo.py` in CI (GitHub Actions) to update `dist/` on each push.

If you want, I can:
- Add a small GitHub Actions workflow to build `dist/` and publish it to `gh-pages` automatically.
- Change the repository package name or versioning scheme.
