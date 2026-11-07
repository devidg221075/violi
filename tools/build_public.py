#!/usr/bin/env python3
"""Copia in public/ solo i file del sito (senza docs/, tools/, dist/).
public/ è la cartella da pubblicare (Vercel: outputDirectory; Cloudflare Pages: build output).
Uso: python3 tools/build_public.py
"""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'public'
shutil.rmtree(OUT, ignore_errors=True)
OUT.mkdir()
for name in ['index.html', 'catalogo.html', 'per-filo.html', '404.html', 'robots.txt', 'sitemap.xml', '_headers']:
    src = ROOT / name
    if src.exists():
        shutil.copy2(src, OUT / name)
shutil.copytree(ROOT / 'assets', OUT / 'assets')
shutil.copytree(ROOT / 'riferimenti', OUT / 'riferimenti')
n = sum(1 for f in OUT.rglob('*') if f.is_file())
print(f'public/: {n} file,', round(sum(f.stat().st_size for f in OUT.rglob('*') if f.is_file()) / 1e6, 2), 'MB')
