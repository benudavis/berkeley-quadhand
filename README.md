# Berkeley QUAD Hand project website

Static project page for the manuscript **“A Quasi-Direct-Drive Underactuated Asymmetric Hand for Dexterous and Efficient Grasping and Manipulation.”**

The site uses plain HTML, CSS, and a small JavaScript file for switching viewer tabs. There is no runtime build step, package manager, analytics, or application server.

## Preview locally

From the repository root, run:

```sh
python3 -m http.server 8000
```

Then open <http://localhost:8000>.

## Publish with GitHub Pages

1. Push `main` to GitHub.
2. Open **Settings → Pages** for the repository.
3. Under **Build and deployment**, select **Deploy from a branch**.
4. Select the `main` branch and `/(root)` folder, then save.

The project-page URL is expected to be:

```text
https://benudavis.github.io/berkeley-quadhand/
```

All site assets use relative paths so the page works from that project subdirectory.

## Content updates

- Site-ready copies of manuscript figures live in `assets/images/`. The ignored `manuscript/` directory remains the source of truth for the paper.
- Replace the paper and video status pills in `index.html` with links when those resources become public.
- The demonstration stage is a placeholder for a featured video and optional secondary clips.
- Add official citation text only after the preprint metadata is fixed.

## Prerecorded Viser viewer

The interactive section embeds Viser's generated static browser client and switches among four prerecorded grasp scenes:

```text
viser/
├── client/index.html
├── grasp_cylinder_large.viser
├── grasp_cylinder_small.viser
├── grasp_sphere_large.viser
└── grasp_sphere_small.viser
```

`viewer.js` changes the iframe playback path when a visitor selects a grasp tab. Only the selected recording is loaded.

The checked-in client was generated with Viser 1.1.1:

```sh
viser-build-client --out-dir viser/client
```

Regenerate the client after intentionally upgrading Viser. The recordings and generated client remain fully static and are hosted directly by GitHub Pages. A live Python/WebSocket GUI can be introduced later without changing the surrounding project page.

The recordings intentionally omit Viser grid nodes. After replacing or regenerating a recording, remove its grids with a Python environment containing Viser's `msgspec` and `zstandard` dependencies:

```sh
python scripts/remove_viser_grids.py viser/*.viser
```
