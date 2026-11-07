#!/usr/bin/env python3
"""Aggiorna meta tag, robots.txt, sitemap.xml e 404.html.

Uso:
  python3 tools/build_seo.py                       # senza dominio: meta base, icone, 404
  python3 tools/build_seo.py --domain https://esempio.it   # aggiunge canonical, og:url, og:image,
                                                           # sitemap.xml e riga Sitemap in robots.txt
Il blocco tra <!--seo--> e <!--/seo--> di ogni pagina viene riscritto a ogni esecuzione.
"""
from pathlib import Path
import argparse, html, re

ROOT = Path(__file__).resolve().parent.parent
PAGES = {
    'index.html': ('Violi Macchine — Tecnologie Made in Italy',
                   'Violi Macchine: da oltre 30 anni tecnologie Made in Italy per la lavorazione dei metalli. '
                   'Oltre 2.000 macchine e impianti in più di 50 Paesi.'),
    'catalogo.html': ('Catalogo Prodotti — Violi Macchine',
                      'Catalogo prodotti Violi Macchine: otto categorie di macchine e impianti per filo, tubo, '
                      'lavaggio a ultrasuoni, pulitura, trucioli, ceneri, catalizzatori e schede elettroniche.'),
    'per-filo.html': ('Macchine per la lavorazione del filo — Violi Macchine',
                      'Macchine per la lavorazione del filo: trafile a passaggi multipli, bobinatori, trafile '
                      'Bull Block e raddrizzatrici con taglio al volo. Tecnologie Made in Italy.'),
}
E = lambda s: html.escape(s, quote=True)

ap = argparse.ArgumentParser()
ap.add_argument('--domain', default='')
domain = ap.parse_args().domain.rstrip('/')


def seo_block(page, title, desc):
    t = [f'<meta name="description" content="{E(desc)}">',
         '<meta property="og:type" content="website">',
         '<meta property="og:locale" content="it_IT">',
         '<meta property="og:site_name" content="Violi Macchine">',
         f'<meta property="og:title" content="{E(title)}">',
         f'<meta property="og:description" content="{E(desc)}">',
         '<meta name="twitter:card" content="summary_large_image">',
         f'<meta name="twitter:title" content="{E(title)}">',
         f'<meta name="twitter:description" content="{E(desc)}">',
         '<link rel="icon" href="assets/violi-logo-web.svg" type="image/svg+xml">',
         '<link rel="icon" href="assets/favicon-32.png" sizes="32x32" type="image/png">',
         '<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">']
    if domain:
        url = domain + '/' + ('' if page == 'index.html' else page)
        img = domain + '/assets/og-image.jpg'
        t += [f'<link rel="canonical" href="{E(url)}">', f'<meta property="og:url" content="{E(url)}">',
              f'<meta property="og:image" content="{E(img)}">', '<meta property="og:image:width" content="1200">',
              '<meta property="og:image:height" content="630">', f'<meta name="twitter:image" content="{E(img)}">']
    return '<!--seo-->' + ''.join(t) + '<!--/seo-->'


for page, (title, desc) in PAGES.items():
    p = ROOT / page
    s = p.read_text()
    s = re.sub(r'<meta name="description"[^>]*>', '', s)
    s = re.sub(r'<link rel="icon"[^>]*>', '', s)
    s = re.sub(r'<!--seo-->.*?<!--/seo-->', '', s, flags=re.S)
    s = s.replace('<link rel="stylesheet" href="assets/fonts.css">', seo_block(page, title, desc) + '<link rel="stylesheet" href="assets/fonts.css">', 1)
    p.write_text(s)
    print('meta', page)

# ---- 404.html: stessa testata e stesso footer della home ----
home = (ROOT / 'index.html').read_text()
main = re.search(r'<main id="main">.*?</main>', home, flags=re.S)[0]
body = ('<main id="main"><section class="wrap section" style="min-height:48vh;display:flex;flex-direction:column;justify-content:center">'
        '<span class="gold-line"></span><h1>Pagina non trovata</h1>'
        '<p>L’indirizzo che hai aperto non esiste o è stato spostato.</p>'
        '<div class="actions"><a class="button" href="index.html">Torna alla home <svg class="ico ico-arrow" aria-hidden="true" focusable="false"><use href="#violi-freccia-destra"/></svg></a>'
        '<a class="button secondary" href="catalogo.html">Vai al catalogo</a></div></section></main>')
p404 = home.replace(main, body)
p404 = re.sub(r'<title>.*?</title>', '<title>Pagina non trovata — Violi Macchine</title>', p404, count=1)
p404 = re.sub(r'<!--seo-->.*?<!--/seo-->', '<meta name="robots" content="noindex"><link rel="icon" href="assets/violi-logo-web.svg" type="image/svg+xml">', p404, flags=re.S)
p404 = p404.replace('<head>', '<head><base href="/">', 1)   # il 404 viene servito a qualsiasi percorso
(ROOT / '404.html').write_text(p404)
print('404.html')

# ---- robots + sitemap ----
robots = 'User-agent: *\nAllow: /\n'
if domain:
    robots += f'\nSitemap: {domain}/sitemap.xml\n'
    urls = ''.join(f'<url><loc>{E(domain + "/" + ("" if pg == "index.html" else pg))}</loc></url>' for pg in PAGES)
    (ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    print('sitemap.xml')
elif (ROOT / 'sitemap.xml').exists():
    (ROOT / 'sitemap.xml').unlink()
(ROOT / 'robots.txt').write_text(robots)
print('robots.txt')
