Packaging and installing the Kodi addon
```markdown
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

GitHub Actions and hosting example

- A workflow has been added at `.github/workflows/publish-gh-pages.yml` which:
	- Runs on pushes to `main`/`master`.
	- Builds the addon zip and `addons.xml` (`scripts/package_addon.py` and `scripts/build_repo.py`).
	- Publishes the `dist/` directory to the `gh-pages` branch using `peaceiris/actions-gh-pages`.

Example URLs (replace placeholders)

- GitHub Pages (recommended):
	- addons.xml: https://<your-github-username>.github.io/<repo-name>/addons.xml
	- repository zip: https://<your-github-username>.github.io/<repo-name>/repository.einthusan-1.0.0.zip

- Raw GitHub (alternative):
	- addons.xml: https://raw.githubusercontent.com/<your-github-username>/<repo-name>/gh-pages/addons.xml

How to add the repo to Kodi

- In Kodi: Add source → enter the base URL where `addons.xml` is hosted (e.g. `https://<username>.github.io/<repo-name>/`).
- Then Add-ons → Install from zip file → browse to that source and install `repository.einthusan-1.0.0.zip`.

Notes

- Enable GitHub Pages for the repository and set the source to the `gh-pages` branch (Repository → Settings → Pages).
- The workflow uses the provided `GITHUB_TOKEN` so no extra secrets are required.
- If you want, I can add a CI workflow that only publishes on tag or release events instead of every push.

``` 
