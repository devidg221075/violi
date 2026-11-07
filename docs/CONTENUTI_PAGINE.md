# Pagine di categoria e prodotto: provenienza dei contenuti

Testi e fotografie sono presi dalle pagine pubbliche di https://violimacchine.it/it/ (lette il 7 novembre 2026),
senza aggiunte. I testi sono in `content/pagine.json`, le foto in `assets/foto/prodotti/`
(ridimensionate a max 1400 px e convertite in WebP). L'origine di ogni foto è in `content/immagini.json`.

Rigenerare le pagine: `python3 tools/build_pages.py && python3 tools/build_seo.py && python3 tools/build_sprite.py`.

## Gruppo 2 (11 pagine, aggiunte dopo)
- **Impianti**: indice e 7 schede (`impianti-*.html`).
- **Azienda** (`azienda.html`), **Contatti** (`contatti.html`, modulo che apre la posta) e **News ed eventi** (`news-ed-eventi.html`, 1 articolo).
- **Privacy e Cookie policy**: non copiate. Il sito ufficiale le ospita su iubenda; il piè di pagina collega quelle pagine (testo legale non riscritto).
- **Contatti**: compare anche il referente per India e GCC (JTE DMCC, Mr. Tarun Thadeshwar) come sul sito ufficiale: confermare che sia ancora valido.
- **Foto**: 21 da violimacchine.it in `assets/foto/impianti/`; la pagina "recupero schede" riusa la foto del prodotto perché l'originale non era scaricabile. Esclusa una foto di officina con volto riconoscibile.
- I testi sono quelli ufficiali, con 7 correzioni minime di refusi evidenti (elenco in fondo). Non sono state toccate maiuscole di stile (es. "Pannello Touch").

## Pagine create nel gruppo 1 (25)
- 4 categorie: Per Tubo, Per Bricchettare Trucioli, Per Ceneri, Per Catalizzatori.
- 21 schede prodotto (Per Filo 3, Per Tubo 5, Lavaggio, Pulitura, Trucioli 2, Ceneri 5, Catalizzatori 3, Schede elettroniche).

## Non create / da verificare
- **Trafile a passaggi multipli per filo**: al primo tentativo il sito ha risposto con una verifica anti-bot; al secondo tentativo (richiesta normale, senza aggirare nulla) la pagina è stata letta e la scheda creata (`per-filo-trafile-passaggi-multipli.html`, 4 foto).
- **Per Filo (categoria)**: resta la pagina già costruita a mano; i quattro prodotti corrispondono a quelli del sito ufficiale.
- **Raddrizzatubo** (`/prodotti/per-tubo/raddrizzatubo`): il sito la lista nel menu della categoria con questo nome,
  ma la scheda corrisponde a "Raddrizzatrici per tubo"; è stata trattata come la stessa pagina.
- **Campionatore rotativo**: nel sito ufficiale il collegamento della scheda in categoria punta per errore ai forni a microonde;
  qui punta alla sua pagina.
- **Dati tecnici**: i testi sono quelli ufficiali; non sono stati aggiunti numeri, modelli o schede PDF.
- Alcune foto di prodotto hanno un marchio "Violi Meccanica Industriale" (insegna storica) o sfondi colorati: valutare con il cliente.

## Correzioni ai testi originali

| Pagina | Tipo | Prima | Dopo |
|---|---|---|---|
| `per-filo-bull-block/paragrafi` | spazio prima della punteggiatura | …afile a passaggi multipli . Il diametro dei cabest… | …afile a passaggi multipli. Il diametro dei cabesta… |
| `per-ceneri-miscelatori/paragrafi` | piò → può | …do rapido ed efficace e piò essere applicato anche… | …do rapido ed efficace e può essere applicato anche… |
| `impianti-trafilatura-tubi-automatici/paragrafi` | spazio prima della punteggiatura | …ante del mandrino interno . Porta foro regolabile … | …ante del mandrino interno. Porta foro regolabile e… |
| `impianti-trafilatura-tubi-automatici/paragrafi` | spazio dopo l' | … esclusivo che permette l ’avviamento della trafil… | … esclusivo che permette l’avviamento della trafila… |
| `impianti-trafilatura-tubi-automatici/paragrafi` | spazio prima della punteggiatura | …ule e barriere metalliche . La velocità di lavoro … | …ule e barriere metalliche. La velocità di lavoro e… |
| `impianti-trafilatura-doppio/paragrafi` | spazio prima della punteggiatura | …l tipo di olio utilizzato . Tutti i movimenti veng… | …l tipo di olio utilizzato. Tutti i movimenti vengo… |
| `azienda/Diamo forma alle tue esigenze` | maiuscola a metà frase | …rgia tra cliente e Violi Permette di produrre tecn… | …rgia tra cliente e Violi permette di produrre tecn… |
