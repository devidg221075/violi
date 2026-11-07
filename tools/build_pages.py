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
import html, json, posixpath, re, urllib.parse

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
    'prodotti/per-filo/trafile-a-passaggi-multipli-per-filo': 'per-filo-trafile-passaggi-multipli.html',
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
    'impianti': 'impianti.html',
    'impianti/impianti-avvolgimento-svolgimento-tubi': 'impianti-svolgimento-avvolgimento-tubi.html',
    'impianti/impianti-raddrizzatura-tubi-5': 'impianti-raddrizzatura-tubi.html',
    'impianti/impianti-raddrizzatura-tubi': 'impianti-raddrizzatura-tubi.html',
    'impianti/impianti-trafilatura-tubi-automatici': 'impianti-trafilatura-tubi-automatici.html',
    'impianti/impianto-di-trafilatura-doppio-automatico-con-taglio-barre-trafilate': 'impianti-trafilatura-doppio.html',
    'impianti/impianti-automatici-triturazione-e-compattazione-truciolo': 'impianti-triturazione-compattazione.html',
    'impianti/impianto-automatico-triturazione-e-compattazione-truciolo': 'impianti-triturazione-compattazione.html',
    'impianti/impianto-automatico-recupero-metalli-preziosi-da-schede-elettroniche': 'impianti-recupero-schede-elettroniche.html',
    'impianti/impianto-automatico-di-frantumazione': 'impianti-frantumazione.html',
    'azienda-macchinari-orafi-recupero-metalli-preziosi-industrie': 'azienda.html',
    'azienda': 'azienda.html',
    'news-ed-eventi': 'news-ed-eventi.html',
    'fiere/violi-macchine-ipmi-eu-chapter-2026.html': 'news-ed-eventi.html#ipmi-eu-chapter-2026',
    'contatti': 'contatti.html',
}
IUB = 'https://www.iubenda.com/privacy-policy/86091182'


def remap(t):
    """Sostituisce gli href del sito ufficiale con le pagine locali, dove esistono."""
    def one(m):
        path = m.group(2).rstrip('/')
        return m.group(1) + REMAP[path] + m.group(3) if path in REMAP else m.group(0)
    t = re.sub(r'(href=")' + re.escape(OFF) + r'([^"#?]+)(")', one, t)
    # "Vedi tutti i prodotti" -> catalogo
    t = re.sub(r'href="' + re.escape(OFF) + r'prodotti"(?=[^>]*>Vedi tutti i prodotti)', 'href="catalogo.html"', t)
    # voci di testata e piè di pagina verso le pagine nuove
    for a, b in [('href="#contatti">Contatti', 'href="contatti.html">Contatti'),
                 ('href="index.html#azienda">Azienda', 'href="azienda.html">Azienda'),
                 ('href="index.html#azienda">Chi siamo', 'href="azienda.html">Chi siamo'),
                 ('href="index.html#mondo">Presenza nel mondo', 'href="index.html#mondo">Presenza nel mondo'),
                 ('href="' + OFF + 'news-ed-eventi">News ed eventi', 'href="news-ed-eventi.html">News ed eventi')]:
        t = t.replace(a, b)
    t = t.replace('<a href="azienda.html">Qualità e innovazione', '<a href="azienda.html#qualita">Qualità e innovazione')
    # privacy e cookie nel piè di pagina (testi ufficiali su iubenda)
    if 'footer-legal' not in t and '<div class="footer-bottom">' in t:
        t = t.replace('<div class="footer-bottom"><div class="wrap">',
                      '<div class="footer-bottom"><div class="wrap"><span class="footer-legal">', 1)
        t = re.sub(r'(P\.IVA IT02200090518) (<a [^>]*>Contatti e informazioni aziendali</a>)',
                   r'\1</span><span class="footer-links"><a href="' + IUB + r'" target="_blank" rel="noopener noreferrer">Privacy Policy</a>'
                   r'<a href="' + IUB + r'/cookie-policy" target="_blank" rel="noopener noreferrer">Cookie Policy</a>\2</span>', t, count=1)
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
            f'<img src="{posixpath.normpath("assets/foto/prodotti/" + fname)}" alt="" aria-hidden="true" decoding="async"{attrs}></div>')


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



# ---------------------------------------------------------------- impianti, azienda, contatti, news
SHOP = 'https://www.mechanicalparts.it/index.php'
CAT_IMP = {'titolo': 'Impianti', 'file': 'impianti.html'}


def hero_block(crumbs, h1, lead, img, buttons, label=''):
    im = photo(img, label or h1, lazy=False, prio=True) if img else ''
    lead_html = f'<p>{E(lead)}</p>' if lead else ''
    return (f'<section class="hero hero-filo hero-prod{"" if img else " hero-text"}"><div class="hero-image">{im}</div><div class="wrap hero-inner">'
            f'<div class="hero-copy">{breadcrumb(crumbs)}<span class="gold-line"></span><h1>{h1}</h1>{lead_html}'
            f'<div class="actions">{buttons}</div></div></div></section>')


def prev_btns(subject):
    return (f'<a class="button doc" href="{E(MAIL("Preventivo: " + subject))}">{ICO("documento-preventivo", "ico doc-ico")} Richiedi un preventivo {ICO("freccia-destra", "ico ico-arrow")}</a>'
            f'<a class="button secondary" href="{E(MAIL("Informazioni: " + subject))}">{ICO("informazioni", "ico info-ico")} Richiedi informazioni</a>')


def card_imp(slug):
    p = PAGES[slug]
    return (f'<article class="product-card family">{photo(p["immagini"][0], p["titolo"] + " Violi Macchine")}<div class="family-copy"><div>'
            f'<h3>{E(p["titolo"])}</h3><p>{E(short(p["paragrafi"][0]))}</p><div class="family-actions">{btn("Vedi impianto", slug + ".html")}'
            f'<a class="text-link" href="{MAIL("Informazioni: " + p["titolo"])}">Richiedi informazioni</a></div></div></div></article>')


def page_impianto(slug, p, c):
    crumbs = [('Home', 'index.html'), ('Impianti', 'impianti.html'), (p['titolo'], None)]
    hero = hero_block(crumbs, E(p['titolo']), '', p['immagini'][0], prev_btns(p['titolo']))
    paras, head = [], 'I vantaggi per il cliente'
    for x in p['paragrafi']:
        if x.endswith(':') and p.get('vantaggi'):
            head = x.rstrip(':')
        else:
            paras.append(x)
    body_p = ''.join(f'<p>{E(x)}</p>' for x in paras)
    adv = ''
    if p.get('vantaggi'):
        adv = f'<h3 class="adv-title">{E(head)}</h3><ul class="adv-list">' + ''.join(f'<li>{ICO("qualita")}<span>{E(x)}</span></li>' for x in p['vantaggi']) + '</ul>'
    rel = ''
    if p.get('correlato'):
        r = p['correlato']
        rel = f'<p class="related">Potrebbe interessarti anche: <a href="{E(r["url"])}">{E(r["testo"])}</a></p>'
    spare = f'<a class="button secondary" href="{SHOP}" target="_blank" rel="noopener noreferrer">Pezzi di ricambio {ICO("freccia-destra", "ico ico-arrow")}</a>' if p.get('ricambi') else ''
    aside = (f'<aside class="prod-aside" aria-label="Richiedi informazioni"><h3>Richiedi informazioni</h3><p>Scrivici o chiamaci: ti rispondiamo su questo impianto.</p>'
             f'<a class="ic" href="tel:+390575810487">+39 0575 810487</a><a class="ic" href="mailto:sales@violimacchine.it">{ICO("email")}sales@violimacchine.it</a>'
             f'{btn("Scrivi a Violi Macchine", MAIL("Informazioni: " + p["titolo"]), "", "email")}{spare}</aside>')
    body = (f'<section class="wrap section prod-body"><div class="prod-text"><p class="eyebrow">L’impianto</p><h2>{E(p["titolo"])}</h2>{body_p}{adv}{rel}</div>{aside}</section>')
    gal = ''
    if len(p['immagini']) > 1:
        shots = ''.join(f'<figure class="shot">{photo(f, p["titolo"] + " Violi Macchine, immagine " + str(i + 2))}</figure>' for i, f in enumerate(p['immagini'][1:]))
        gal = (f'<section class="wrap section gallery"><div class="section-heading"><div><p class="eyebrow">Immagini</p><h2>L’impianto in dettaglio</h2></div></div>'
               f'<div class="gallery-grid g{min(len(p["immagini"]) - 1, 3)}">{shots}</div></section>')
    others = [k for k, q in PAGES.items() if q['tipo'] == 'impianto' and k != slug]
    sib = (f'<section class="wrap section" id="altri"><div class="section-heading"><div><p class="eyebrow">Impianti</p><h2>Altri impianti</h2></div>'
           f'<a class="text-link" href="impianti.html">Tutti gli impianti {ICO("freccia-destra")}</a></div><div class="family-grid">{"".join(card_imp(k) for k in others[:4])}</div></section>')
    return '<main id="main">' + hero + body + gal + sib + cta_for(c['cta'], 'Preventivo: ' + p['titolo']) + '</main>'


def page_indice_impianti(slug, p, c):
    hero = hero_block([('Home', 'index.html'), ('Impianti', None)], 'Impianti', p['intro'], p['immagini'][0],
                      btn('Scopri gli impianti', '#impianti') + f'<a class="button secondary" href="{E(MAIL("Informazioni impianti"))}">{ICO("informazioni", "ico info-ico")} Richiedi informazioni</a>')
    grid = (f'<section class="wrap section" id="impianti"><div class="section-heading"><div><p class="eyebrow">Impianti</p><h2>Soluzioni su misura</h2></div></div>'
            f'<div class="family-grid">{"".join(card_imp(k) for k in p["impianti"])}</div></section>')
    return '<main id="main">' + hero + grid + cta_for(c['cta'], 'Preventivo impianto') + '</main>'


def page_azienda(slug, p, c):
    S = {x['titolo']: x for x in p['sezioni']}
    pics = ['azienda-industriale', 'azienda-orafo-1', 'azienda-orafo-3', 'azienda-recupero', 'azienda-officina']
    intro = S['Chi è Violi Macchine']
    hero = hero_block([('Home', 'index.html'), ('Azienda', None)], 'Chi è Violi Macchine', '', '../sede-violi.webp',
                      btn('Scopri i prodotti', 'catalogo.html') + f'<a class="button secondary" href="contatti.html">Contattaci {ICO("freccia-destra", "ico ico-arrow")}</a>',
                      'La sede di Violi Macchine a Monte San Savino')
    chi = (f'<section class="intro-band"><div class="wrap"><h2>Chi siamo</h2><div>' + ''.join(f'<p>{E(t)}</p>' for t in intro['testo']) + '</div></div></section>')
    rows = ''
    names = ['Progettazione', 'Ricerca', 'Innovazione', 'Una missione di qualità', 'Diamo forma alle tue esigenze']
    for i, n in enumerate(names):
        x = S[n]
        anchor = ' id="qualita"' if n == 'Una missione di qualità' else ''
        rows += (f'<article class="about-row{" rev" if i % 2 else ""}"{anchor}><div class="about-photo">{photo("../impianti/" + pics[i] + ".webp", n + " — Violi Macchine")}</div>'
                 f'<div class="about-text"><p class="eyebrow">{E(n)}</p><h2>{E(n)}</h2>' + ''.join(f'<p>{E(t)}</p>' for t in x['testo']) + '</div></article>')
    num = ('<section class="wrap section"><dl class="stats stats-row"><div><dt>2.000+</dt><dd>Macchine e impianti</dd></div><div><dt>50+</dt><dd>Paesi</dd></div>'
           '<div><dt>30+</dt><dd>Anni di esperienza</dd></div></dl></section>')
    return '<main id="main">' + hero + chi + '<section class="wrap section about">' + rows + '</section>' + num + cta_for(c['cta'], 'Contatto da pagina Azienda') + '</main>'


def page_contatti(slug, p, c):
    hero = hero_block([('Home', 'index.html'), ('Contatti', None)], 'Contatti', 'Richiedi informazioni o un preventivo: ti ricontatteremo il prima possibile.', None, '')
    hero = hero.replace('<div class="actions"></div>', '')
    form = ('<form class="contact-form" id="contact-form" data-mailto="sales@violimacchine.it" novalidate>'
            '<h2>Inviaci la tua richiesta</h2><p>Compila il modulo: si apre il tuo programma di posta con il messaggio già scritto, pronto da inviare. Nessun dato viene inviato dal sito.</p>'
            '<div class="fld"><label for="f-nome">Nome e cognome *</label><input id="f-nome" name="nome" required autocomplete="name"></div>'
            '<div class="fld"><label for="f-az">Azienda *</label><input id="f-az" name="azienda" required autocomplete="organization"></div>'
            '<div class="fld"><label for="f-mail">E-mail aziendale *</label><input id="f-mail" name="email" type="email" required autocomplete="email"></div>'
            '<div class="fld"><label for="f-tel">Telefono *</label><input id="f-tel" name="tel" type="tel" required autocomplete="tel"></div>'
            '<div class="fld wide"><label for="f-prod">Prodotto o impianto di interesse</label><select id="f-prod" name="prodotto"><option value="">Seleziona…</option>'
            + ''.join(f'<option>{E(q["titolo"])}</option>' for q in PAGES.values() if q['tipo'] in ('prodotto', 'impianto')) + '</select></div>'
            '<div class="fld wide"><label for="f-msg">Richieste e note *</label><textarea id="f-msg" name="messaggio" rows="5" required></textarea></div>'
            f'<label class="chk"><input type="checkbox" name="privacy" required> <span>Ho preso visione dell’<a href="{IUB}" target="_blank" rel="noopener noreferrer">informativa sulla privacy</a> (art. 13 GDPR). *</span></label>'
            f'<p class="form-msg" role="status" aria-live="polite"></p><button class="button" type="submit">Apri la posta {ICO("freccia-destra", "ico ico-arrow")}</button>'
            f'<noscript><p class="notice">Con JavaScript disattivato scrivi direttamente a <a href="mailto:sales@violimacchine.it">sales@violimacchine.it</a>.</p></noscript></form>')
    info = ('<aside class="contact-info"><h2>Come contattarci</h2>'
            '<h3>Violi Macchine S.r.l.</h3><p class="ic">' + ICO('localizzazione') + '<span>Via XXV Aprile, 86<br>52048 Monte San Savino (AR) — Italia</span></p>'
            '<a class="ic" href="tel:+390575810487">' + ICO('assistenza') + '+39 0575 810487</a><a class="ic" href="mailto:sales@violimacchine.it">' + ICO('email') + 'sales@violimacchine.it</a>'
            '<p class="small">P.IVA IT02200090518</p>'
            '<a class="button secondary" href="https://www.google.com/maps/place/Via+XXV+Aprile,+86,+52048+Monte+San+Savino+AR" target="_blank" rel="noopener noreferrer">Trovaci sulla mappa ' + ICO('freccia-destra', 'ico ico-arrow') + '</a>'
            '<hr><h3>Contatti area India e GCC</h3><p><strong>JTE DMCC</strong><br>Mr. Tarun Thadeshwar<br><a href="tel:+917506010750">+91 7506010750</a><br><a href="mailto:tarun@jtedmcc.com">tarun@jtedmcc.com</a></p></aside>')
    return '<main id="main">' + hero + f'<section class="wrap section contact-grid">{form}{info}</section></main>'


def page_news(slug, p, c):
    hero = hero_block([('Home', 'index.html'), ('News ed eventi', None)], 'News ed eventi', 'Fiere, eventi e novità da Violi Macchine.', None, '')
    hero = hero.replace('<div class="actions"></div>', '')
    arts = ''
    for a in p['articoli']:
        arts += (f'<article class="news-item" id="{a["id"]}"><p class="eyebrow">{E(a["categoria"])}</p><h2>{E(a["titolo"])}</h2><p class="news-date">{E(a["data"])}</p>'
                 + ''.join(f'<p>{E(t)}</p>' for t in a['testo'])
                 + f'<p><a class="text-link" href="mailto:{a["contatto"]}">Per informazioni: {a["contatto"]}</a></p></article>')
    return '<main id="main">' + hero + f'<section class="wrap section news-list">{arts}</section>' + cta_for(c['cta'], 'Contatto da News') + '</main>'


def main():
    head, tail_head, sprite, header, footer, cta = parts()
    c = {'cta': cta}
    n = 0
    for slug, p in PAGES.items():
        title = p['titolo'] + ' — Violi Macchine'
        body = {'categoria': page_categoria, 'prodotto': page_prodotto, 'impianto': page_impianto, 'indice-impianti': page_indice_impianti,
                'azienda': page_azienda, 'contatti': page_contatti, 'news': page_news}[p['tipo']](slug, p, c)
        # voce "Prodotti" del menu come pagina corrente
        h = header
        cur = {'impianto': 'impianti.html">Impianti', 'indice-impianti': 'impianti.html">Impianti', 'azienda': 'azienda.html">Azienda',
               'contatti': 'contatti.html">Contatti', 'news': 'news-ed-eventi.html">News ed eventi'}.get(p['tipo'])
        if cur is None:
            h = re.sub(r'<a\s+href="catalogo\.html">Prodotti', '<a aria-current=page href="catalogo.html">Prodotti', h, count=1)
        else:
            h = re.sub(r'<a href="(?:' + re.escape(OFF) + r'impianti|impianti\.html)">Impianti', '<a href="impianti.html">Impianti', h)
            h = re.sub(r'<a\s+href="' + re.escape(cur), '<a aria-current=page href="' + cur, h, count=1)
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
