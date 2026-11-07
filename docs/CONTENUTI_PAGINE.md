# Pagine di categoria e prodotto: provenienza dei contenuti

Testi e fotografie sono presi dalle pagine pubbliche di https://violimacchine.it/it/ (lette il 7 novembre 2026),
senza aggiunte. I testi sono in `content/pagine.json`, le foto in `assets/foto/prodotti/`
(ridimensionate a max 1400 px e convertite in WebP). L'origine di ogni foto è in `content/immagini.json`.

Rigenerare le pagine: `python3 tools/build_pages.py && python3 tools/build_seo.py && python3 tools/build_sprite.py`.

## Pagine create (25)
- 4 categorie: Per Tubo, Per Bricchettare Trucioli, Per Ceneri, Per Catalizzatori.
- 21 schede prodotto (Per Filo 3, Per Tubo 5, Lavaggio, Pulitura, Trucioli 2, Ceneri 5, Catalizzatori 3, Schede elettroniche).

## Non create / da verificare
- **Trafile a passaggi multipli per filo**: il sito ufficiale ha risposto con una verifica anti-bot ("One moment, please…")
  e il contenuto non è stato letto. La scheda in `per-filo.html` rimanda ancora alla pagina ufficiale.
- **Per Filo (categoria)**: stessa verifica anti-bot; resta la pagina già costruita a mano.
- **Raddrizzatubo** (`/prodotti/per-tubo/raddrizzatubo`): il sito la lista nel menu della categoria con questo nome,
  ma la scheda corrisponde a "Raddrizzatrici per tubo"; è stata trattata come la stessa pagina.
- **Campionatore rotativo**: nel sito ufficiale il collegamento della scheda in categoria punta per errore ai forni a microonde;
  qui punta alla sua pagina.
- **Dati tecnici**: i testi sono quelli ufficiali; non sono stati aggiunti numeri, modelli o schede PDF.
- Alcune foto di prodotto hanno un marchio "Violi Meccanica Industriale" (insegna storica) o sfondi colorati: valutare con il cliente.
