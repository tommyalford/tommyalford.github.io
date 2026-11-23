# tommyalford.github.io

Tommy Alford's personal academic website. A single page of plain HTML and CSS, hosted on GitHub Pages, with no frameworks and no JavaScript.

Almost everything is written directly in `index.html`. The one exception is the publication list, which a small script, `build_pubs.py`, generates from `content/publications.bib`.

## Repo layout

```
index.html              the whole site: intro and photo, Research, Publications
assets/style.css        styling (light + dark mode)
build_pubs.py           fills the publication list in index.html from the .bib file
content/
  publications.bib      publication list
  cv.pdf                CV (linked from the "CV" link)
  headshot.jpg          photo
```

## Updating the website

You need Python 3.8 or newer, which is already on a Mac. There is nothing to install.

### Add a publication

1. Open `content/publications.bib` and add an entry, copying an existing one as a template. Set `category` to `selected`, `collaboration` or `undergraduate`.
2. Write authors as `Last, F. and Last, F.`. Include `Alford, T.` to have the name bolded. For big collaboration papers where he isn't listed individually, use `Lead, A. and others` and add `note = {Including T. Alford}`.
3. Add `eprint = {...}` for an arXiv ID, which gives the arXiv and PDF links. Add `doi = {...}` or `url = {...}` if you have them. The comment line above each entry shows where those go.
4. Run `python3 build_pubs.py`. It rewrites the publication list inside `index.html`.

### Update the CV

Replace `content/cv.pdf` with the new file, keeping the name `cv.pdf`. No build step is needed. If you still see the old version, hard-refresh the browser.

### Change the bio, links, or research text

Open `index.html` and edit the text directly. No build step is needed.

- **Affiliation, advisor and bio:** the lines at the top, next to the photo.
- **Links (email, CV, GitHub):** the list under the bio. To add one, copy an existing `<li>` line and change the URL and label.
- **Research:** the `Research` section. It currently holds placeholder verse. Replace it with real text, using `<h3>` for subheadings and `<p>` for paragraphs.
- Don't edit between `<!-- BEGIN:pubs -->` and `<!-- END:pubs -->`. The script overwrites that part.

### Change the photo

Replace `content/headshot.jpg`, then make the two smaller copies the site uses:

```
sips --resampleWidth 400 -s formatOptions 80 content/headshot.jpg --out assets/headshot-400.jpg
sips --resampleWidth 800 -s formatOptions 80 content/headshot.jpg --out assets/headshot-800.jpg
```

### Preview locally

```
python3 -m http.server
```

Then open http://localhost:8000.

### Publish

```
git add -A
git commit -m "Describe your change"
git push
```

GitHub Pages updates the live site within about a minute.

## One-time GitHub Pages setup

In the repository on GitHub, go to Settings → Pages, set the source to "Deploy from a branch", and choose branch `main` and folder `/ (root)`. The site is then served at https://tommyalford.github.io/.

## Working with Claude Code

`CLAUDE.md` describes the site's conventions, so you can ask Claude Code things like "add this new paper" or "update the CV" and it will follow the steps above.
