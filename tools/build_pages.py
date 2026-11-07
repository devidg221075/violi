#!/usr/bin/env python3
"""Genera le pagine di categoria e di prodotto a partire da content/pagine.json.

Testata, piè di pagina, sprite delle icone, fascia CTA e vantaggi vengono letti
dalle pagine esistenti (index.html e per-filo.html): una modifica a quelle parti
si propaga rieseguendo questo script. Esegue anche la rimappatura dei collegamenti
dal sito ufficiale alle pagine locali (idempotente) su tutte le pagine del sito.

Ordine consigliato dopo ogni modifica:
  python3 tools/build_pages.py && python3 tools/build_seo.py && python3 tools/build_sprite.py
"""
from pathlib import Path
import html, json, re, urllib.parse

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / 'content' / 'pagine.json').read_text())
CATS, PAGES = DATA['categorie'], DATA['pagine']
OFF = 'https://violimacchine.it/it/'
E = lambda s: html.escape(s, quote=True)

# ---------------------------------------------------------------- collegamenti
REMAP = {
    'prodotti/per-tubo': 'per-tubo.html',
    'prodotti/per-lavaggio-ultrasuoni/lavatrici-ad-ultrasuoni': 'lavatrici-ad-ultrasuoni.html',
    'prodotti/per-pulitura/banco-pulitrice-per-orafi': 'banco-pulitrice-per-orafi.html',
    'prodotti/per-bricchettare-trucioli': 'per-bricchettare-trucioli.html',
    'prodotti/per-ceneri': 'per-ceneri.html',
    'prodotti/per-catalizzatori': 'per-catalizzatori.html',
    'prodotti/per-schede-elettroniche/separatrice-di-componenti-da-schede-elettroniche': 'separatrice-schede-elettroniche.html',
    'prodotti/per-filo/bobinatore-per-filo': 'per-filo-bobinatore.html',
    'prodotti/per-filo/trafile-per-filo-bull-block': 'per-filo-bull-block.html',
    'prodotti/per-filo/raddrizzatrici-per-filo-con-taglio-al-volo': 'per-filo-raddrizzatrici.html',
    'prodotti/per-tubo/trafile-idrauliche-per-tubo': 'per-tubo-trafile-idrauliche.html',
    'prodotti/per-tubo/appuntatrici-per-tubo': 'per-tubo-appuntatrici.html',
    'prodotti/per-tubo/raddrizzatrici-per-tubo': 'per-tubo-raddrizzatrici.html',
    'prodotti/per-tubo/raddrizzatubo': 'per-tubo-raddrizzatrici.html',
    'prodotti/per-tubo/tagliatubo': 'per-tubo-tagliatubo.html',
    'prodotti/per-tubo/raddrizzatrici-per-profili': 'per-tubo-raddrizzatrici-profili.html',
    'prodotti/per-bricchettare-trucioli/bricchettatrici-per-truciolo': 'per-bricchettare-trucioli-truciolo.html',
    'prodotti/per-bricchettare-trucioli/bricchettatrici-per-truciolo-di-metalli-preziosi': 'per-bricchettare-trucioli-metalli-preziosi.html',
    'prodotti/per-ceneri/mulini-a-sfere-per-ceneri': 'per-ceneri-mulini-a-sfere.html',
    'prodotti/per-ceneri/miscelatori-per-ceneri': 'per-ceneri-miscelatori.html',
    'prodotti/per-ceneri/mulino-a-ganasce': 'per-ceneri-mulino-a-ganasce.html',
    'prodotti/per-ceneri/campionatore-rotativo': 'per-ceneri-campionatore-rotativo.html',
    'prodotti/per-ceneri/forni-a-microonde': 'per-ceneri-forni-a-microonde.html',
    'prodotti/per-catalizzatori/mulini-a-sfere-per-catalizzatori-ceramici': 'per-catalizzatori-mulini-a-sfere-ceramici.html',
    'prodotti/per-catalizzatori/mulini-per-catalizzatori-metallici': 'per-catalizzatori-mulini-metallici.html',
    'prodotti/per-catalizzatori/mulino-a-ganasce-per-catalizzatori': 'per-catalizzatori-mulino-a-ganasce.html',
}


def remap(t):
    """Sostituisce gli href del sito ufficiale con le pagine locali, dove esistono."""
    def one(m):
        path = m.group(2).rstrip('/')
        return m.group(1) + REMAP[path] + m.group(3) if path in REMAP else m.group(0)
    t = re.sub(r'(href=")' + re.escape(OFF) + r'([^"#?]+)(")', one, t)
    # "Vedi tutti i prodotti" -> catalogo
    t = re.sub(r'href="' + re.escape(OFF) + r'prodotti"(?=[^>]*>Vedi tutti i prodotti)', 'href="catalogo.html"', t)
    return t


# ---------------------------------------------------------------- parti comuni
def parts():
    home = (ROOT / 'index.html').read_text()
    filo = (ROOT / 'per-filo.html').read_text()
    head = home[:home.index('<!--seo-->')]
    head = re.sub(r'<title>.*?</title>', '<title>{TITLE}</title>', head, flags=re.S)
    tail_head = home[home.index('<!--/seo-->') + len('<!--/seo-->'):home.index('<body>') + 6]
    sprite = re.search(r'<!--icone-->.*?<!--/icone-->', home, flags=re.S)[0]
    header = home[home.index('<a class="skip"'):home.index('</header>') + 9]
    footer = home[home.index('<footer'):]
    cta = filo[filo.index('<section class="custom-band"'):filo.index('</main>')]
    return head, tail_head, sprite, header, footer, cta


ICO = lambda n, c='ico': f'<svg class="{c}" aria-hidden="true" focusable="false"><use href="#violi-{n}"/></svg>'
MAIL = lambda s: 'mailto:sales@violimacchine.it?subject=' + urllib.parse.quote(s)


def short(text, n=170):
    first = re.split(r'(?<=[a-zà-ù\)])\.\s', text, maxsplit=1)[0].rstrip('.') + '.'
    if len(first) <= n:
        return first
    cut = first[:n].rsplit(' ', 1)[0].rstrip(',;:')
    return cut + '…'


META = json.loads((ROOT / 'content' / 'immagini.json').read_text())
FIT = {v['file']: ('contain' if v['sfondo_bianco'] else 'cover') for v in META.values()}


def photo(fname, label, extra='', lazy=True, prio=False):
    fit = FIT.get(fname, 'cover')
    attrs = ' fetchpriority="high"' if prio else (' loading="lazy"' if lazy else '')
    return (f'<div class="photo ph {fit} {extra}" role="img" aria-label="{E(label)}">'
            f'<img src="assets/foto/prodotti/{fname}" alt="" aria-hidden="true" decoding="async"{attrs}></div>')


def breadcrumb(items):
    out = []
    for i, (label, href) in enumerate(items):
        out.append(f'<span aria-current="page">{E(label)}</span>' if href is None else f'<a href="{href}">{E(label)}</a>')
    return '<nav class="breadcrumb" aria-label="Percorso">' + '<span>/</span>'.join(out) + '</nav>'


def btn(text, href, cls='', ico='freccia-destra'):
    return f'<a class="button {cls}" href="{E(href)}">{text} {ICO(ico, "ico ico-arrow") if ico else ""}</a>'


def card(slug):
    p = PAGES[slug]
    img = p['immagini'][0] if p['immagini'] else None
    ph = photo(img, f"{p['titolo']} Violi Macchine") if img else ''
    d = short(p['paragrafi'][0]) if p.get('paragrafi') else ''
    return (f'<article class="product-card family">{ph}<div class="family-copy"><div><h3>{E(p["titolo"])}</h3>'
            f'<p>{E(d)}</p><div class="family-actions">{btn("Scopri il prodotto", slug + ".html")}'
            f'<a class="text-link" href="{MAIL("Informazioni: " + p["titolo"])}">Richiedi informazioni</a></div></div></div></article>')


def cta_for(cta, subject):
    return re.sub(r'href="mailto:[^"]*"', f'href="{MAIL(subject)}"', cta, count=1)


# ---------------------------------------------------------------- pagine
def page_prodotto(slug, p, c):
    cat = CATS[p['categoria']]
    group = [k for k, q in PAGES.items() if q['tipo'] == 'prodotto' and q['categoria'] == p['categoria']]
    multi = len(group) > 1
    crumbs = [('Home', 'index.html'), ('Prodotti', 'catalogo.html')]
    if multi:
        crumbs += [(cat['titolo'], cat['file']), (p['titolo'], None)]
        back = btn(f'Torna a {cat["titolo"]}', cat['file'], 'secondary', None)
    else:
        crumbs += [(cat['titolo'], None)]
        back = btn('Torna al catalogo', 'catalogo.html', 'secondary', None)
    hero_img = photo(p['immagini'][0], f'{p["titolo"]} Violi Macchine', lazy=False, prio=True) if p['immagini'] else ''
    hero = (f'<section class="hero hero-filo hero-prod"><div class="hero-image">{hero_img}</div>'
            f'<div class="wrap hero-inner"><div class="hero-copy">{breadcrumb(crumbs)}<span class="gold-line"></span>'
            f'<h1>{E(p["titolo"])}</h1><div class="actions">'
            f'<a class="button doc" href="{E(MAIL("Preventivo: " + p["titolo"]))}">{ICO("documento-preventivo", "ico doc-ico")} Richiedi un preventivo {ICO("freccia-destra", "ico ico-arrow")}</a>'
            f'<a class="button secondary" href="{E(MAIL("Informazioni: " + p["titolo"]))}">{ICO("informazioni", "ico info-ico")} Richiedi informazioni</a>'
            f'</div></div></div></section>')
    paras = ''.join(f'<p>{E(x)}</p>' for x in p['paragrafi'])
    rel = ''
    if p.get('correlato'):
        r = p['correlato']
        ext = r['url'].startswith('http')
        rel = (f'<p class="related">Potrebbe interessarti anche: <a href="{E(r["url"])}"'
               f'{" target=_blank rel=noopener" if ext else ""}>{E(r["testo"])}</a></p>')
    body = (f'<section class="wrap section prod-body"><div class="prod-text"><p class="eyebrow">Il prodotto</p>'
            f'<h2>{E(p["titolo"])}</h2>{paras}{rel}</div><aside class="prod-aside" aria-label="Richiedi informazioni">'
            f'<h3>Richiedi informazioni</h3><p>Scrivici o chiamaci: ti rispondiamo su questo prodotto.</p>'
            f'<a class="ic" href="tel:+390575810487">+39 0575 810487</a>'
            f'<a class="ic" href="mailto:sales@violimacchine.it">{ICO("email")}sales@violimacchine.it</a>'
            f'{btn("Scrivi a Violi Macchine", MAIL("Informazioni: " + p["titolo"]), "", "email")}</aside></section>')
    gal = ''
    if len(p['immagini']) > 1:
        shots = ''.join(f'<figure class="shot">{photo(f, f"{p["titolo"]} Violi Macchine, immagine {i + 2}")}</figure>'
                        for i, f in enumerate(p['immagini'][1:]))
        gal = (f'<section class="wrap section gallery" aria-label="Immagini del prodotto"><div class="section-heading"><div>'
               f'<p class="eyebrow">Immagini</p><h2>Il prodotto in dettaglio</h2></div></div><div class="gallery-grid g{min(len(p["immagini"]) - 1, 3)}">{shots}</div></section>')
    sib = ''
    if multi:
        others = [s for s in group if s != slug]
        if others:
            sib = (f'<section class="wrap section" id="altri"><div class="section-heading"><div><p class="eyebrow">{E(cat["titolo"])}</p>'
                   f'<h2>Altri prodotti</h2></div><a class="text-link" href="{cat["file"]}">Tutti i prodotti {ICO("freccia-destra")}</a></div>'
                   f'<div class="family-grid">{"".join(card(s) for s in others)}</div></section>')
    return '<main id="main">' + hero + body + gal + sib + cta_for(c['cta'], 'Preventivo: ' + p['titolo']) + '</main>'


def page_categoria(slug, p, c):
    cat = CATS[p['categoria']]
    first = PAGES[p['prodotti'][0]]['immagini'][0]
    hero = (f'<section class="hero hero-filo hero-prod"><div class="hero-image">{photo(first, p["titolo"] + " Violi Macchine", lazy=False, prio=True)}</div>'
            f'<div class="wrap hero-inner"><div class="hero-copy">{breadcrumb([("Home", "index.html"), ("Prodotti", "catalogo.html"), (p["titolo"], None)])}'
            f'<span class="gold-line"></span><h1>Macchine {E(p["titolo"].lower())}</h1><p>{E(p["descrizione"])}</p><div class="actions">'
            f'{btn("Scopri i prodotti", "#macchine")}{btn("Richiedi informazioni", MAIL("Informazioni: " + p["titolo"]), "secondary", "informazioni")}</div></div></div></section>')
    hero = hero.replace(ICO('informazioni', 'ico ico-arrow'), ICO('informazioni', 'ico info-ico'))
    grid = (f'<section class="wrap section" id="macchine"><div class="section-heading"><div><p class="eyebrow">Prodotti</p>'
            f'<h2>I nostri macchinari</h2></div></div><div class="family-grid">{"".join(card(s) for s in p["prodotti"])}</div></section>')
    return '<main id="main">' + hero + grid + cta_for(c['cta'], 'Soluzione su misura: ' + p['titolo']) + '</main>'


def main():
    head, tail_head, sprite, header, footer, cta = parts()
    c = {'cta': cta}
    n = 0
    for slug, p in PAGES.items():
        title = p['titolo'] + ' — Violi Macchine'
        body = page_categoria(slug, p, c) if p['tipo'] == 'categoria' else page_prodotto(slug, p, c)
        # voce "Prodotti" del menu come pagina corrente
        h = header.replace('<a href="catalogo.html">Prodotti', '<a aria-current=page href="catalogo.html">Prodotti', 1)
        out = (head.replace('{TITLE}', E(title)) + '<!--seo--><!--/seo-->' + tail_head + sprite + h + body + footer)
        (ROOT / (slug + '.html')).write_text(remap(out))
        n += 1
    # rimappa anche le pagine scritte a mano
    for name in ['index.html', 'catalogo.html', 'per-filo.html']:
        p = ROOT / name
        t = p.read_text()
        r = remap(t)
        if r != t:
            p.write_text(r)
    print(n, 'pagine generate')


if __name__ == '__main__':
    main()
