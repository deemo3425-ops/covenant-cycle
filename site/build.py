#!/usr/bin/env python3
"""Render the book to static HTML for GitHub Pages.

The source Markdown is never modified and never copied into the repo as HTML --
_site/ is build output. Rendering is a view, not an edition.

Why this instead of Jekyll, GitHub Pages' default:
  1. Jekyll only converts files that carry YAML front matter. Adding front
     matter to anakainosis.md would edit a byte-protected file.
  2. Jekyll's kramdown applies typographic replacement by default, turning
     "..." into an ellipsis character. That would silently destroy the
     Protected Ledger's two straight ellipses, which exist precisely to read
     differently from the ten curly ones.
python-markdown does neither. verify.py proves the marks survive the render.
"""
import html
import re
import shutil
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_site"
BASE = "https://deemo3425-ops.github.io/covenant-cycle"

DESC = ("Five tellings of one future. Four AI models wrote in relay, none reading "
        "another's draft — then the man who carried the stories between them wrote the fifth.")

# source -> (output path, <title>)
PAGES = {
    "README.md":                          ("index.html",  "The Covenant Cycle"),
    "tellings/01-introduction.md":        ("tellings/01-introduction.html",        "Introduction"),
    "tellings/02-the-book-of-renewals.md":("tellings/02-the-book-of-renewals.html","I. The Book of Renewals"),
    "tellings/03-aubade-for-the-makers.md":("tellings/03-aubade-for-the-makers.html","II. Aubade for the Makers"),
    "tellings/04-the-relief.md":          ("tellings/04-the-relief.html",          "III. The Relief"),
    "tellings/05-the-fourth-telling.md":  ("tellings/05-the-fourth-telling.html",  "IV. The Fourth Telling"),
    "tellings/06-afterword.md":           ("tellings/06-afterword.html",           "Afterword"),
    "anakainosis.md":                     ("anakainosis.html",                     "V. anakainosis"),
    "tellings/08-the-panel.md":           ("tellings/08-the-panel.html",           "The Panel"),
    "editors-report.md":                  ("editors-report.html",                  "Editor's Report"),
    "revision-log.md":                    ("revision-log.html",                    "Revision Log"),
    "about-the-license.md":               ("about-the-license.html",               "About the License"),
}

CSS = """
:root{--ink:#1b1917;--bg:#faf8f5;--dim:#6b635b;--rule:#e0d9d0;--link:#7a3b2e;
--measure:34em;--serif:Charter,"Bitstream Charter","Iowan Old Style","Palatino Linotype",Georgia,serif}
@media (prefers-color-scheme:dark){:root{--ink:#e6e1da;--bg:#141311;--dim:#9a918a;--rule:#332f2b;--link:#d99a7e}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--serif);
font-size:19px;line-height:1.65;-webkit-text-size-adjust:100%}
.wrap{max-width:var(--measure);margin:0 auto;padding:3rem 1.25rem 5rem}
a{color:var(--link)}
h1,h2,h3{line-height:1.25;font-weight:600;margin:2.5rem 0 1rem}
h1{font-size:1.9rem;margin-top:0}h2{font-size:1.3rem}h3{font-size:1.1rem}
p{margin:0 0 1.15rem}
blockquote{margin:1.5rem 0;padding-left:1.1rem;border-left:2px solid var(--rule);color:var(--dim)}
hr{border:0;border-top:1px solid var(--rule);margin:2.5rem 0}
code,pre{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.85em}
pre{background:rgba(128,128,128,.10);padding:.9rem 1rem;border-radius:4px;overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:.92em;display:block;overflow-x:auto}
th,td{border-bottom:1px solid var(--rule);padding:.45rem .6rem;text-align:left;vertical-align:top}
img{max-width:100%}
nav.top{font-size:.82rem;letter-spacing:.06em;text-transform:uppercase;
margin-bottom:3rem;padding-bottom:1rem;border-bottom:1px solid var(--rule);color:var(--dim)}
nav.top a{text-decoration:none;color:var(--dim)}nav.top a:hover{color:var(--link)}
footer{margin-top:4rem;padding-top:1.25rem;border-top:1px solid var(--rule);
font-size:.85rem;color:var(--dim)}
footer a{color:var(--dim)}
"""

SHELL = """<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="author" content="D.N. Morgan, Opus 4.8, Fable 5, Sonnet 5, Opus 5">
<link rel="canonical" href="{canon}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="article">
<meta property="og:url" content="{canon}">
<style>{css}</style>
</head><body><div class="wrap">
{nav}
{body}
<footer>
<p>The record: <a href="{up}revision-log.html">Revision Log</a> &middot;
<a href="{up}editors-report.html">Editor&rsquo;s Report</a> &middot;
<a href="{up}about-the-license.html">About the License</a></p>
<p><em>The Covenant Cycle</em> by D.N. Morgan, Opus 4.8, Fable 5, Sonnet 5, and Opus 5 &mdash;
<a href="https://github.com/deemo3425-ops/covenant-cycle">github.com/deemo3425-ops/covenant-cycle</a></p>
</footer>
</div></body></html>
"""


def relink(body: str, depth: int) -> str:
    """Point .md hrefs at their rendered .html, and fix depth for subpages."""
    def sub(m):
        href = m.group(1)
        if href.startswith(("http://", "https://", "#", "mailto:")):
            return m.group(0)
        if href == "LICENSE":
            return ('href="https://github.com/deemo3425-ops/'
                    'covenant-cycle/blob/main/LICENSE"')
        for src, (dst, _) in PAGES.items():
            if href == src:
                href = dst
                break
        else:
            return m.group(0) if not href.endswith(".md") else m.group(0)
        if depth and not href.startswith("../"):
            href = "../" * depth + href
        return f'href="{href}"'
    return re.sub(r'href="([^"]+)"', sub, body)


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    md = markdown.Markdown(extensions=["tables", "sane_lists"])

    for src, (dst, title) in PAGES.items():
        text = (ROOT / src).read_text(encoding="utf-8")
        md.reset()
        body = md.convert(text)
        depth = dst.count("/")
        body = relink(body, depth)
        if dst != "index.html":
            up = "../" * depth
            nav = f'<nav class="top"><a href="{up}index.html">&#8592; The Covenant Cycle</a></nav>'
            full_title = f"{title} — The Covenant Cycle"
        else:
            nav = ""
            full_title = "The Covenant Cycle"
        page = SHELL.format(
            title=html.escape(full_title), desc=html.escape(DESC),
            canon=f"{BASE}/{'' if dst == 'index.html' else dst}",
            css=CSS, nav=nav, body=body, up="../" * depth)
        out = OUT / dst
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page, encoding="utf-8")

    shutil.copy(ROOT / "qr.png", OUT / "qr.png")
    shutil.copy(ROOT / "The_Covenant_Cycle.pdf", OUT / "The_Covenant_Cycle.pdf")
    (OUT / ".nojekyll").write_text("")

    urls = "\n".join(
        f"  <url><loc>{BASE}/{'' if d == 'index.html' else d}</loc></url>"
        for d, _ in PAGES.values())
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n</urlset>\n", encoding="utf-8")

    print(f"built {len(PAGES)} pages into {OUT}")


if __name__ == "__main__":
    main()
