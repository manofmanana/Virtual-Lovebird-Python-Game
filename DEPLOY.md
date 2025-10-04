Deployment notes — GitHub Pages and itch.io

This file documents a small, repeatable workflow to publish the pygbag web build
that lives in `web/build/web` and is packaged as `mango_web_build.zip`.

1) Quick local verification
   - Unzip `mango_web_build.zip` to a temporary directory and serve it locally:

       python3 -m http.server 8000 --directory web/build/web

     Then open http://localhost:8000 in a browser and test interactions. Note:
     the browser will require a user gesture to enable audio (click the screen).

2) Publish to GitHub Pages (recommended for demo)
   - Create a branch with the web build (we include the ZIP in commits in this
     repo for convenience):

       git checkout -b gh-pages-web-build
       git add mango_web_build.zip web/build/web
       git commit -m "Add pygbag web build artifacts"
       git push --set-upstream origin gh-pages-web-build

   - In the repository settings on GitHub, configure GitHub Pages to serve from
     the `gh-pages-web-build` branch (or merge the branch into `gh-pages`).

3) Upload to itch.io
   - In the itch.io dashboard, choose "Upload files" -> drag `mango_web_build.zip`.
   - Set the kind of game to "HTML" and make sure the file is the uploaded HTML
     build. Publish and test the page in an incognito window to confirm assets
     and audio behavior.

4) Notes & troubleshooting
   - Browsers block autoplay: the game requires a user click to start music and
     to permit audio playback. Make sure to click the canvas to start audio.
   - If audio is missing or the page shows a black screen, open the browser
     devtools console and look for 404s or module loading errors.
   - If you prefer the packaged paths to be `sounds/`, `sprites/`, and
     `backgrounds/` at the top-level instead of `assets/...`, tell me and I can
     adjust the packaging workflow (it may require small changes to the copy
     script and a re-run of the build).

5) Rebuild steps (if you need to reproduce locally)
   - From repo root:

       /bin/bash scripts/pygbag_build_with_assets.sh

     The script copies assets into `web/`, runs `pygbag` in the background,
     waits for `web/build/web/web.apk`, produces `web/pygbag_build.log` and
     creates `mango_web_build.zip`.

---

If you'd like, I can push the current branch with the artifacts to your
remote repository now (I created branch `build/web-artifacts` locally). If you
prefer a different branch name or want me to open a PR, tell me and I'll do it.
