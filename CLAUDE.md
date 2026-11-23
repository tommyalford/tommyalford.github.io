# CLAUDE.md

Personal academic website for Tommy Alford (PhD student in physics/cosmology at the University of Chicago, applying for postdocs). Plain HTML and CSS served directly by GitHub Pages from `main` at the repo root. There is no build step at deploy time.

Use "Tommy Alford" for the name everywhere on the site, never "Thomas". (The bib file header says "Thomas Alford"; that is internal only.)

## Structure

```
index.html  research.html  publications.html  cv.html  contact.html
assets/
  style.css                 all styling, light and dark
  favicon.svg
  headshot-400.jpg, -800.jpg   resized copies of content/headshot.jpg
build.py                    regenerates content-driven page regions (stdlib Python 3.8+)
content/                    SOURCE OF TRUTH: edit these, not the generated HTML
  publications.bib          -> publications.html
  bio.txt                   -> index.html
  profile.txt               -> index.html (intro, links) and contact.html
  research-summary.txt      -> research.html
  cv.pdf                    embedded and linked directly by cv.html
  headshot.jpg              original photo
.nojekyll
```

`build.py` rewrites the text between `<!-- BEGIN:name -->` and `<!-- END:name -->` markers in the HTML pages (`intro`, `bio`, `links` in index; `research`; `pubs`; `contact`). Never hand-edit between markers, because the next build overwrites it. Layout, nav and footer outside the markers are hand-written HTML, and `cv.html` has no markers at all.

After changing anything in `content/` except `cv.pdf` and `headshot.jpg`, run `python3 build.py` and commit the regenerated HTML together with the content change. Re-running it with no content changes must produce no diff.

## Design rules (keep these)

- Monospace font stack starting with Menlo, left-aligned, one column about 72ch wide.
- Dark mode via `prefers-color-scheme` only (CSS variables in `:root`). No toggle.
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
4. Run `python3 build.py`, open `publications.html`, and check the new entry (author bolding, venue line, links).
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

Replace `content/cv.pdf` with the new PDF, keeping the same filename. No build is needed. `cv.html` embeds it and offers a download button, and both point at `content/cv.pdf`. Browsers cache PDFs, so hard-refresh when checking. If the CV lists publications that are not yet in `publications.bib`, mention that to the user.

## Other content

- **Bio** (`content/bio.txt`): paragraphs separated by blank lines. `[text](https://url)`, `**bold**` and `*italic*` work. Currently still "lorem ipsum".
- **Contact and links** (`content/profile.txt`): `key: value` lines (`title`, `affiliation`, `advisor`, `email`, `address`) and `link.<Label>: <url>` lines. An empty value renders as a visible yellow `[TODO: ...]` marker on the page, and `build.py` lists what is still missing. For a multi-line address, separate lines with `|`.
- **Research page** (`content/research-summary.txt`): `## Heading` lines, blank-line-separated paragraphs, and single line breaks preserved. It currently contains placeholder Seuss-style verse that the user plans to replace.
- **Headshot:** replace `content/headshot.jpg`, then regenerate the two resized copies:
  `sips --resampleWidth 400 -s formatOptions 80 content/headshot.jpg --out assets/headshot-400.jpg`
  `sips --resampleWidth 800 -s formatOptions 80 content/headshot.jpg --out assets/headshot-800.jpg`
  The photo is shown at its natural aspect ratio (no cropping). If the new ratio differs from about 3:4, update `width`/`height` on the `<img>` in `index.html` to the resized dimensions.

## Preview and deploy

- Preview: `python3 -m http.server` in the repo root, then open http://localhost:8000.
- Deploy: push to `main`. GitHub Pages republishes within about a minute.
- Do not commit or push unless the user asks.
