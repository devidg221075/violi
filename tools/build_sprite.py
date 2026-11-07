#!/usr/bin/env python3
"""Genera lo sprite delle icone ufficiali (kit vettoriale Master 1.1) e lo incorpora
nelle tre pagine, tra i marcatori <!--icone--> e <!--/icone-->.

Sorgente: assets/icone/*.svg (varianti currentColor del kit).
Uso: python3 tools/build_sprite.py
Nel markup: <svg class="ico"><use href="#violi-nome"/></svg>
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
PAGES = ['index.html', 'catalogo.html', 'per-filo.html']

symbols, defs = [], []
for f in sorted((ROOT / 'assets' / 'icone').glob('*.svg')):
    t = f.read_text()
    body = t[t.index('</defs>') + 7:t.rindex('</svg>')] if '</defs>' in t else t[t.index('>', t.index('<svg')) + 1:t.rindex('</svg>')]
    # i gradienti del kit non servono alle icone currentColor; la maschera di LinkedIn si'
    for m in re.findall(r'<mask.*?</mask>', t, flags=re.S):
        defs.append(m)
    symbols.append(f'<symbol id="violi-{f.stem}" viewBox="0 0 64 64">{body}</symbol>')

sprite = ('<!--icone--><svg xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false" '
          'style="position:absolute;width:0;height:0;overflow:hidden"><defs>' + ''.join(defs) + '</defs>'
          + ''.join(symbols) + '</svg><!--/icone-->')

for name in PAGES:
    p = ROOT / name
    t = p.read_text()
    if '<!--icone-->' in t:
        t = re.sub(r'<!--icone-->.*?<!--/icone-->', lambda m: sprite, t, flags=re.S)
    else:
        t = t.replace('<body>', '<body>' + sprite, 1)
    p.write_text(t)
    print('sprite in', name, len(sprite), 'byte,', len(symbols), 'icone')
