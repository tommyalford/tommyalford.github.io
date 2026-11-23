#!/usr/bin/env python3
"""Regenerate the content-driven parts of the site from content/.

    python3 build.py

Fills the regions between <!-- BEGIN:name --> and <!-- END:name --> markers:
    index.html         intro, bio, links     <- content/profile.txt, content/bio.txt
    research.html      research              <- content/research-summary.txt
    publications.html  pubs                  <- content/publications.bib
    contact.html       contact               <- content/profile.txt

Everything else in the HTML files is hand-written and left alone.
Standard library only (Python 3.8+).
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
HIGHLIGHT_LAST_NAMES = {"alford"}          # surnames to bold in author lists
HIGHLIGHT_NOTE_RE = re.compile(r"\bT\. Alford\b")
TODOS = []

GROUPS = [
    ("selected", "Selected publications",
     "Papers with major contributions. The contribution is noted under each entry."),
    ("collaboration", "Collaboration publications",
     "Papers from ACT and the Simons Observatory. For the ACT papers, contributions were "
     "detector passband calibration and uncertainty characterization supporting mapmaking, "
     "component separation, foreground modeling, and cosmological analysis."),
    ("undergraduate", "Undergraduate research", ""),
]


# ---------------------------------------------------------------- text helpers

def esc(s):
    return html.escape(s, quote=True)


def inline(s):
    """Escape, then apply **bold**, *italic*, and [text](url)."""
    s = esc(s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+|mailto:[^)\s]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", s)
    return s


def read_text(name):
    """Read a content file, dropping '# comment' lines (but not '## heading' lines)."""
    path = CONTENT / name
    lines = path.read_text(encoding="utf-8").splitlines()
    return [ln for ln in lines if not re.match(r"#(\s|$)", ln)]


def text_to_html(lines):
    """Paragraphs separated by blank lines; '## ' starts a heading; single newlines become <br>."""
    out, para = [], []

    def flush():
        if para:
            out.append("<p>" + "<br>\n".join(inline(p) for p in para) + "</p>")
            para.clear()

    for ln in lines:
        if ln.startswith("## "):
            flush()
            out.append("<h2>" + inline(ln[3:].strip()) + "</h2>")
        elif not ln.strip():
            flush()
        else:
            para.append(ln.strip())
    flush()
    return "\n".join(out)


def todo(label):
    TODOS.append(label)
    return '<span class="todo">[TODO: %s]</span>' % esc(label)


# --------------------------------------------------------------------- profile

def read_profile():
    prof, links = {}, []
    for ln in read_text("profile.txt"):
        if ":" not in ln or not ln.strip():
            continue
        key, _, val = ln.partition(":")
        key, val = key.strip(), val.strip()
        if key.startswith("link."):
            links.append((key[5:].strip(), val))
        else:
            prof[key] = val
    return prof, links


def link_html(label, url):
    return '<a href="%s">%s</a>' % (esc(url), esc(label)) if url else todo("%s link" % label)


def build_intro(prof):
    parts = [prof.get("title") or None, prof.get("affiliation") or None]
    line = ", ".join(esc(p) for p in parts if p)
    if not line:
        line = todo("title / affiliation")
    out = ['<p class="affil">%s</p>' % line]
    if prof.get("advisor"):
        out.append('<p class="affil">Advisor: %s</p>' % inline(prof["advisor"]))
    return "\n".join(out)


def build_bio():
    return text_to_html(read_text("bio.txt"))


def build_links(prof, links):
    items = []
    email = prof.get("email")
    items.append('<a href="mailto:%s">email</a>' % esc(email) if email else todo("email"))
    items.append('<a href="cv.html">CV</a>')
    items += [link_html(label, url) for label, url in links]
    return '<ul class="links">\n' + "\n".join("  <li>%s</li>" % i for i in items) + "\n</ul>"


def build_contact(prof, links):
    rows = []
    email = prof.get("email")
    rows.append(("email", '<a href="mailto:%s">%s</a>' % (esc(email), esc(email)) if email else todo("email")))
    if prof.get("affiliation"):
        rows.append(("affiliation", esc(prof["affiliation"])))
    rows.append(("address", "<br>".join(esc(p.strip()) for p in prof["address"].split("|"))
                 if prof.get("address") else todo("address")))
    for label, url in links:
        rows.append((label.lower(), link_html(label, url) if not url else
                     '<a href="%s">%s</a>' % (esc(url), esc(re.sub(r"^https?://(www\.)?", "", url).rstrip("/")))))
    return '<dl class="kv">\n' + "\n".join("  <dt>%s</dt>\n  <dd>%s</dd>" % (esc(k), v) for k, v in rows) + "\n</dl>"


# ---------------------------------------------------------------------- BibTeX

def _read_braced(s, i):
    """s[i] == '{': return (contents, index after the matching '}')."""
    depth, start = 0, i
    while i < len(s):
        c = s[i]
        if c == "\\":
            i += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return s[start + 1:i], i + 1
        i += 1
    raise ValueError("unbalanced braces in .bib file")


def parse_bib(text):
    text = "\n".join(ln for ln in text.splitlines() if not ln.lstrip().startswith("%"))
    entries, pos = [], 0
    for m in re.finditer(r"@(\w+)\s*\{", text):
        if m.start() < pos:
            continue
        kind = m.group(1).lower()
        body, pos = _read_braced(text, m.end() - 1)
        if kind in ("comment", "string", "preamble"):
            continue
        key, _, rest = body.partition(",")
        fields, i = {}, 0
        while i < len(rest):
            fm = re.compile(r"\s*,?\s*([A-Za-z][\w-]*)\s*=\s*").match(rest, i)
            if not fm:
                break
            i = fm.end()
            if rest[i] == "{":
                val, i = _read_braced(rest, i)
            elif rest[i] == '"':
                j = rest.index('"', i + 1)
                val, i = rest[i + 1:j], j + 1
            else:
                vm = re.compile(r"[^,\s]+").match(rest, i)
                val, i = vm.group(0), vm.end()
            fields[fm.group(1).lower()] = val.strip()
        entries.append({"type": kind, "key": key.strip(), **fields})
    return entries


GREEK = {"Lambda": "Λ", "lambda": "λ", "Omega": "Ω", "omega": "ω", "alpha": "α", "beta": "β",
         "gamma": "γ", "mu": "μ", "nu": "ν", "sigma": "σ", "tau": "τ", "Delta": "Δ"}


def tex_to_text(s):
    s = re.sub(r"\$([^$]*)\$", lambda m: re.sub(r"\\([A-Za-z]+)\s*", lambda g: GREEK.get(g.group(1), g.group(0)), m.group(1)), s)
    s = s.replace("---", "—").replace("--", "–")
    s = s.replace("\\&", "&").replace("\\%", "%").replace("\\_", "_")
    s = re.sub(r"(?<!\\)[{}]", "", s)
    return re.sub(r"\s+", " ", s).strip()


def format_authors(entry):
    raw = entry.get("author", "")
    names, others = [], False
    for a in re.split(r"\s+and\s+", raw.strip()):
        a = tex_to_text(a)
        if a.lower() == "others":
            others = True
            continue
        last, _, first = a.partition(",")
        disp = ("%s %s" % (first.strip(), last.strip())).strip()
        bold = last.strip().lower() in HIGHLIGHT_LAST_NAMES
        names.append("<strong>%s</strong>" % esc(disp) if bold else esc(disp))
    out = ", ".join(names)
    if others:
        out += (", et al." if len(names) > 1 else " et al.")
    note = entry.get("note", "")
    if note.lower().startswith("including"):
        who = esc(tex_to_text(note[len("including"):].strip()))
        who = HIGHLIGHT_NOTE_RE.sub(lambda m: "<strong>%s</strong>" % m.group(0), who)
        if "<strong>" not in out:
            out += " (including %s)" % who
    return out


def format_venue(entry):
    year = entry.get("year", "")
    note = entry.get("note", "")
    note = "" if note.lower().startswith("including") else tex_to_text(note)
    kind = entry["type"]
    if kind == "article":
        v = tex_to_text(entry.get("journal", ""))
        if entry.get("volume"):
            v += " " + entry["volume"]
        if entry.get("pages"):
            v += ", " + entry["pages"]
    elif kind == "inproceedings":
        v = tex_to_text(entry.get("booktitle", ""))
        if entry.get("volume"):
            v += " " + entry["volume"]
    else:
        v = note or "Preprint"
        note = ""
    if year:
        v += " (%s)" % year
    if note:
        v += ". " + note
    return esc(v)


def format_links(entry):
    links = []
    if entry.get("doi"):
        links.append(("DOI", "https://doi.org/" + entry["doi"]))
    if entry.get("eprint"):
        links.append(("arXiv", "https://arxiv.org/abs/" + entry["eprint"]))
    if entry.get("url"):
        links.append(("PDF", entry["url"]))
    elif entry.get("eprint"):
        links.append(("PDF", "https://arxiv.org/pdf/" + entry["eprint"]))
    return " ".join('[<a href="%s">%s</a>]' % (esc(u), esc(l)) for l, u in links)


def format_entry(entry):
    parts = ['    <li id="%s">' % esc(entry["key"]),
             '      <span class="pub-title">%s</span>' % esc(tex_to_text(entry.get("title", ""))),
             '      <span class="pub-authors">%s</span>' % format_authors(entry),
             '      <span class="pub-venue">%s</span>' % format_venue(entry)]
    links = format_links(entry)
    if links:
        parts.append('      <span class="pub-links">%s</span>' % links)
    if entry.get("contribution"):
        parts.append('      <span class="pub-contrib">%s</span>' % esc(tex_to_text(entry["contribution"])))
    parts.append("    </li>")
    return "\n".join(parts)


def build_pubs():
    entries = parse_bib((CONTENT / "publications.bib").read_text(encoding="utf-8"))
    out, seen = [], set()
    for cat, heading, blurb in GROUPS:
        group = [e for e in entries if e.get("category", "").lower() == cat]
        group.sort(key=lambda e: -int(re.sub(r"\D", "", e.get("year", "0")) or 0))   # stable: keeps file order within a year
        seen.update(e["key"] for e in group)
        if not group:
            continue
        out.append("<section>\n  <h2>%s</h2>" % esc(heading))
        if blurb:
            out.append('  <p class="blurb">%s</p>' % esc(blurb))
        out.append('  <ul class="pubs">\n' + "\n".join(format_entry(e) for e in group) + "\n  </ul>\n</section>")
    for e in entries:
        if e["key"] not in seen:
            print("warning: %s has no recognised category and was skipped" % e["key"], file=sys.stderr)
    out.append('<p class="blurb">Source: <a href="content/publications.bib">publications.bib</a></p>')
    return "\n".join(out), len(entries)


# --------------------------------------------------------------------- writing

def fill(page, name, new):
    path = ROOT / page
    src = path.read_text(encoding="utf-8")
    pat = re.compile(r"(<!-- BEGIN:%s -->)(.*?)(<!-- END:%s -->)" % (name, name), re.S)
    if not pat.search(src):
        sys.exit("error: %s is missing <!-- BEGIN:%s --> ... <!-- END:%s -->" % (page, name, name))
    path.write_text(pat.sub(lambda m: "%s\n%s\n%s" % (m.group(1), new, m.group(3)), src, count=1), encoding="utf-8")


def main():
    prof, links = read_profile()
    fill("index.html", "intro", build_intro(prof))
    fill("index.html", "bio", build_bio())
    fill("index.html", "links", build_links(prof, links))
    fill("research.html", "research", text_to_html(read_text("research-summary.txt")))
    fill("contact.html", "contact", build_contact(prof, links))
    pubs, n = build_pubs()
    fill("publications.html", "pubs", pubs)
    print("built 4 pages from content/ (%d publications)" % n)
    if TODOS:
        print("still missing in content/profile.txt: " + ", ".join(sorted(set(TODOS))))


if __name__ == "__main__":
    main()
