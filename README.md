# tommyalford.github.io

Tommy Alford's personal academic website. Plain HTML and CSS, hosted on GitHub Pages, with no frameworks and no JavaScript.

All the text lives in `content/`. A small script, `build.py`, copies it into the HTML pages. You never edit the generated parts of the HTML by hand.

## Repo layout

```
index.html research.html publications.html cv.html contact.html   the pages
assets/style.css                                                  styling (light + dark mode)
build.py                                                          fills pages from content/
content/
  publications.bib      publication list
  bio.txt               bio on the home page
  profile.txt           title, advisor, email, address, profile links
  research-summary.txt  Research page text
  cv.pdf                CV
  headshot.jpg          photo
```

## Updating the website

You need Python 3.8 or newer, which is already on a Mac. There is nothing to install. The routine is always the same: edit a file in `content/`, run `python3 build.py`, preview, then commit and push.

### Add a publication

1. Open `content/publications.bib` and add an entry, copying an existing one as a template. Set `category` to `selected`, `collaboration` or `undergraduate`.
2. Write authors as `Last, F. and Last, F.`. Include `Alford, T.` to have the name bolded. For big collaboration papers where he isn't listed individually, use `Lead, A. and others` and add `note = {Including T. Alford}`.
3. Add `eprint = {...}` for an arXiv ID, which gives the arXiv and PDF links. Add `doi = {...}` or `url = {...}` if you have them. The comment line above each entry shows where those go.
4. Run `python3 build.py`.

### Update the CV

Replace `content/cv.pdf` with the new file, keeping the name `cv.pdf`. No build step is needed. If you still see the old version, hard-refresh the browser.

### Change the bio, contact details, or links

- Bio: edit `content/bio.txt`. Separate paragraphs with a blank line.
- Email, advisor, address, and links to INSPIRE, Google Scholar, ORCID, arXiv and GitHub: edit `content/profile.txt`. Anything left empty shows up on the site as a yellow `[TODO]` marker, so you can spot what is missing.
- Then run `python3 build.py`.

### Replace the research text

Edit `content/research-summary.txt`. It currently holds placeholder verse. Start a section with `## Heading`, and separate paragraphs with a blank line. Then run `python3 build.py`.

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
