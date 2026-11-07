#!/usr/bin/env python3
"""Genera le versioni autonome (*-autonomo.html) in dist/.

Parte dai file sorgente alla radice del repo (index.html, catalogo.html,
per-filo.html + assets/) e incorpora font, logo, foto, CSS e JavaScript.
Uso: python3 tools/build_standalone.py
"""
from pathlib import Path
import re, base64, mimetypes

ROOT = Path(__file__).resolve().parent.parent
A = ROOT / 'assets'
OUT = ROOT / 'dist'
PAGES = ['index', 'catalogo', 'per-filo']


def data(path):
    mime = mimetypes.guess_type(str(path))[0] or 'application/octet-stream'
    return 'data:' + mime + ';base64,' + base64.b64encode(path.read_bytes()).decode()


fonts = (A / 'fonts.css').read_text()
for name in re.findall(r'url\(([^)]+)\)', fonts):
    fonts = fonts.replace(name, data(A / name))
sprites = (A / 'sprites.css').read_text()
style = (A / 'style.css').read_text().replace("@import url('sprites.css');", sprites)
script = (A / 'site.js').read_text()

boxes = {}
for n, w, h, pct, left, top in re.findall(
        r'\.crop-(\d+)\{aspect-ratio:(\d+)/(\d+)\}\.crop-\d+ img\{width:([^%]+)%;left:([^%]+)%;top:([^%]+)%;\}', sprites):
    boxes[n] = tuple(map(float, (w, h, pct, left, top)))

OUT.mkdir(exist_ok=True)
for file in PAGES:
    source = (ROOT / (file + '.html')).read_text()
    extras, sources = [], {}

    def replace_photo(m):
        cl, alt, name = m.groups()
        n = re.search(r'crop-(\d+)', cl)[1]
        w, h, pct, left, top = boxes[n]
        W = w * pct / 100
        H = 1683 if name == 'catalogo-riferimento.webp' else 1536
        x, y = -left * w / 100, -top * h / 100
        if name not in sources:
            sources[name] = f'ref{len(sources)}'
        extras.append(f'.photo.crop-{n}{{background-size:{pct}% auto;'
                      f'background-position:{x/(W-w)*100}% {y/(H-h)*100}%;background-repeat:no-repeat}}')
        return f'<div class="photo {cl} {sources[name]}" role="img" aria-label="{alt}"></div>'

    source = re.sub(
        r'<div class="photo ([^"]*)" role="img" aria-label="([^"]*)"><img src="assets/(?!foto/)([^"]*)"[^>]*></div>',
        replace_photo, source)
    local = (style + '\n'
             + ''.join(f'.photo.{v}{{background-image:url("{data(A / n)}");}}' for n, v in sources.items())
             + '\n' + '\n'.join(extras))
    source = source.replace('<link rel="stylesheet" href="assets/fonts.css">', '<style>' + fonts + '</style>')
    source = source.replace('<link rel="stylesheet" href="assets/style.css">', '<style>' + local + '</style>')
    source = source.replace('<script defer src="assets/site.js"></script>',
                            '<script>document.addEventListener("DOMContentLoaded",()=>{\n' + script + '\n});</script>')
    source = re.sub(r'<link rel="(?:icon" href="assets/favicon-32\.png|apple-touch-icon)"[^>]*>', '', source)
    source = re.sub(r'src="(assets/foto/[^"]+)"', lambda m: 'src="' + data(ROOT / m.group(1)) + '"', source)
    source = source.replace('assets/violi-logo-web.svg', data(A / 'violi-logo-web.svg'))
    source = source.replace('assets/violi-logo-web-bianco.svg', data(A / 'violi-logo-web-bianco.svg'))
    for name in PAGES:
        source = source.replace(f'href="{name}.html', f'href="{name}-autonomo.html')
    (OUT / (file + '-autonomo.html')).write_text(source)
    print('scritto', OUT / (file + '-autonomo.html'), len(source), 'byte')
