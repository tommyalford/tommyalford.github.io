# CLAUDE.md

Personal academic website for Tommy Alford (PhD student in physics/cosmology at the University of Chicago, applying for postdocs). It is a single page of plain HTML and CSS, served directly by GitHub Pages from `main` at the repo root. There is no build step at deploy time.

Use "Tommy Alford" for the name everywhere on the site, never "Thomas". (The bib file header says "Thomas Alford"; that is internal only.)

## Structure

```
index.html              the whole site: intro + photo, Research, Publications
assets/
  style.css             all styling, light and dark
  favicon.svg
  headshot-400.jpg, -800.jpg   resized copies of content/headshot.jpg
build_pubs.py           regenerates the publication list in index.html (stdlib Python 3.8+)
content/
  publications.bib      SOURCE OF TRUTH for the publication list
  cv.pdf                linked from the "CV" link in index.html
  headshot.jpg          original photo
.nojekyll
```

Everything except the publication list is hand-written HTML in `index.html`: the affiliation and advisor lines, the bio paragraph, the links row (email, CV, GitHub), and the Research section. Edit those directly.

The publication list sits between `<!-- BEGIN:pubs -->` and `<!-- END:pubs -->` in `index.html`. `build_pubs.py` overwrites that region from `content/publications.bib`, so never hand-edit between the markers. Re-running it with no bib changes must produce no diff.

Layout follows a friend's site, https://gingerschultheis.github.io/: one page, no navigation menu, sections stacked down the page. Don't split it back into multiple pages unless asked.

## Design rules (keep these)

- Monospace font stack starting with Menlo, left-aligned. The intro puts the text on the left and the photo (natural aspect ratio) on the right; on phones the photo moves above the text.
- Page title "Tommy Alford" in the `<h1>` at 20pt. No divider lines between sections.
- Light mode only. Dark mode is deliberately disabled for now. To bring it back, add a `@media (prefers-color-scheme: dark)` block that overrides the CSS variables in `:root`, set `color-scheme: light dark` in `:root` and in the `<meta name="color-scheme">` tag in `index.html`, and restore the dark variant in `assets/favicon.svg` (all three are in git history, commit `e953d48`). No toggle.
- No JavaScript, no frameworks, no web fonts, no external requests.
- Keep it fast and readable on a phone.

## Add a publication

1. Open `content/publications.bib` and add an entry inside the right block (newest first is tidy, though the build sorts by year anyway). Put a TODO comment line directly above it, as every other entry has:
   `% TODO: add  doi = {10.xxxx/xxxxx},  and/or  url = {https://.../paper.pdf},  to the entry below (optional)`
2. Fields the site reads:
   - `author`, `title` (wrap in double braces `{{...}}` to protect capitalization), `year`
   - `journal`, `volume`, `pages` for `@article`; `booktitle`, `volume` for `@inproceedings`; use `@misc` for preprints
   - `eprint` (arXiv ID, which gives arXiv and PDF links), `doi`, `url` (a PDF link)
   - `note`: for `@misc`, shown as the venue (e.g. `Submitted to Applied Optics`)
   - `category`: exactly one of `selected`, `collaboration`, `undergraduate`. An entry with a missing or unknown category is skipped with a warning.
   - `contribution`: one sentence on Tommy's role. Shown under `selected` entries; leave it out for the others.
3. Author convention:
   - Write authors as `Last, F.` separated by ` and `.
   - If Tommy is in the list, include `Alford, T.` and he is bolded automatically.
   - For long collaboration lists where he is not individually named, use `Lead, A. and others` plus `note = {Including T. Alford}`. This renders as "A. Lead et al. (including **T. Alford**)".
   - `and others` renders as "et al."
4. Run `python3 build_pubs.py`, open `index.html`, and check the new entry (author bolding, venue line, links).
5. Never invent a DOI, URL, volume, page number, or arXiv ID. If it isn't in the material you were given, leave the field out and tell the user what is missing.

Example:

```bibtex
% TODO: add  doi = {10.xxxx/xxxxx},  and/or  url = {https://.../paper.pdf},  to the entry below (optional)
@article{smith2027example,
  author       = {Smith, J. and Alford, T. and others},
  title        = {{The Simons Observatory: An Example Paper}},
  journal      = {JCAP},
  year         = {2027},
  eprint       = {2701.00001},
  archivePrefix = {arXiv},
  category     = {selected},
  contribution = {Led the beam analysis.}
}
```

## Update the CV

Replace `content/cv.pdf` with the new PDF, keeping the same filename. No build is needed. The "CV" link in `index.html` opens it directly in the browser. Browsers cache PDFs, so hard-refresh when checking. If the CV lists publications that are not yet in `publications.bib`, mention that to the user.

## Other content (edit `index.html` directly)

- **Affiliation, advisor, bio:** the `<p class="affil">` lines and the paragraph below them in the `.intro` block. The bio is still "lorem ipsum".
- **Links row:** the `<ul class="links">` list. To add a link (INSPIRE, Google Scholar, ORCID, arXiv...), add `<li><a href="URL">Label</a></li>`. Don't add a link with an empty or made-up URL.
- **Research section:** `<section id="research">`. It currently contains placeholder Seuss-style verse (an HTML comment above it says so) that the user plans to replace. Use `<h3>` for subheadings and `<p>` for paragraphs.
- **Headshot:** replace `content/headshot.jpg`, then regenerate the two resized copies:
  `sips --resampleWidth 400 -s formatOptions 80 content/headshot.jpg --out assets/headshot-400.jpg`
  `sips --resampleWidth 800 -s formatOptions 80 content/headshot.jpg --out assets/headshot-800.jpg`
  The photo is shown at its natural aspect ratio (no cropping). If the new ratio differs from about 3:4, update `width`/`height` on the `<img>` in `index.html` to the resized dimensions.

## Preview and deploy

- Preview: `python3 -m http.server` in the repo root, then open http://localhost:8000.
- Deploy: push to `main`. GitHub Pages republishes within about a minute.
- Do not commit or push unless the user asks.
