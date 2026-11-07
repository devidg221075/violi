# Checklist di pubblicazione — Violi Macchine

Stato al momento della stesura: **nulla è stato pubblicato**. Questo documento elenca cosa
serve prima di mettere il sito online e come farlo. Le misure sotto sono state rilevate
aprendo le pagine in locale.

## 1. Blocchi da risolvere prima di pubblicare

| # | Punto | Perché | Chi |
|---|-------|--------|-----|
| 1 | **Fotografie reali dei prodotti** | Inserite 3 foto reali (sede, lavaggio a ultrasuoni, dettaglio meccanico); le altre posizioni usano ancora ritagli dei tre mockup (`assets/*-riferimento.png`), illustrazioni non certificate che mostrano anche marchi provvisori. Non vanno pubblicate come fotografie dei prodotti. | Violi: fornire le foto |
| 2 | **Approvazione della ricostruzione** | Gli HTML approvati originali sono andati persi (`docs/STATO_E_PROVENIENZA.md`): le pagine attuali non sono ancora state approvate dal cliente. | Cliente |
| 3 | **Prodotti VP / IU / BT** | Nomi e abbinamenti arrivano dal mockup, non sono verificati. Il confronto non contiene dati tecnici (corretto). | Violi: confermare |
| 4 | **Informativa privacy** | Il sito non usa cookie né analytics, ma i contatti avvengono via email e nel footer manca il collegamento alla privacy policy. Oggi punta a `violimacchine.it/it/contatti`. | Violi / consulente |
| 5 | **Dati aziendali** | Controllare indirizzo, telefono, P.IVA e email del footer (presi dal sito ufficiale il 7 novembre 2026). | Violi |
| 6 | **PDF e video** | I pulsanti rimandano al sito ufficiale: non ci sono PDF né video propri. | Violi: materiali |

## 2. Ottimizzazioni tecniche (fatte)

| Voce | Prima | Dopo |
|------|-------|------|
| Font | 8 file TTF, circa 2 MB | 8 file WOFF2 ridotti al set latino, circa 120 KB |
| Immagini di riferimento | 3 PNG, circa 6,4 MB | 3 WebP, circa 0,7 MB (stessa dimensione in pixel) |
| Home (peso totale) | 5,3 MB | circa 1,0 MB |
| Versioni autonome | 5,6-8,4 MB ciascuna | 0,6-0,9 MB ciascuna |
| Cartella `public/` | non esisteva | 1,2 MB in tutto |

Il confronto pixel per pixel con la versione precedente (390 e 1280 px, tre pagine) non mostra differenze visibili.

Fatto anche: meta description distinte per pagina, Open Graph e Twitter card, favicon PNG e `apple-touch-icon`,
`404.html` (noindex, funziona a qualsiasi percorso), `robots.txt`, immagine di anteprima `assets/og-image.jpg` (1200×630).

**Quando il dominio è definito** eseguire una volta:

```bash
python3 tools/build_seo.py --domain https://IL-TUO-DOMINIO
```

Aggiunge `canonical`, `og:url`, `og:image` e genera `sitemap.xml` con la riga `Sitemap:` in `robots.txt`.
Senza `--domain` il comando ripristina lo stato attuale (nessun URL assoluto).

Ancora da fare, quando disponibili i materiali:

- **Foto reali**: esportarle in WebP/AVIF a più larghezze (`srcset`) al posto dei ritagli dei mockup.
- **Dati strutturati**: `Organization` e `LocalBusiness` (JSON-LD) con i dati aziendali confermati.
- **Immagine di anteprima**: rifarla con una foto reale al posto del ritaglio del mockup.

## 3. Hosting consigliato (sito statico)

Le pagine sono statiche: nessun framework. La cartella da pubblicare è `public/`, generata da
`python3 tools/build_public.py` (copia solo pagine, `assets/`, `riferimenti/`, `404.html`, `robots.txt`,
`sitemap.xml` e `_headers`; esclude `docs/`, `tools/` e `dist/`).

**Vercel** — il file `vercel.json` è già pronto (build command, cartella `public`, intestazioni di cache e sicurezza).
Importare il repository e lasciare le impostazioni proposte.

**Cloudflare Pages** — Framework preset *None*, Build command `python3 tools/build_public.py`,
Build output directory `public`. Le intestazioni vengono lette da `_headers`.

Cache: i file in `assets/` hanno cache di un anno (`immutable`); se un file di `assets/` cambia, va cambiato anche il nome
(per esempio `style.v2.css`) oppure rimossa la cache. Le pagine HTML si ricontrollano a ogni visita.

## 4. Dominio

1. Decidere il dominio (nuovo sottodominio di prova, per esempio `nuovo.violimacchine.it`, prima di toccare `violimacchine.it`).
2. Aggiungere il dominio al progetto sul provider e creare i record DNS indicati (CNAME o A).
3. Verificare il certificato HTTPS, poi impostare il reindirizzamento da `www` al dominio principale.
4. Non spostare il dominio principale finché il cliente non ha approvato le pagine.

## 5. Controlli finali (da ripetere sul sito online)

- [ ] Le tre pagine si aprono e i collegamenti tra loro funzionano.
- [ ] Sottomenu di Prodotti, Impianti e Azienda: aprono le pagine giuste.
- [ ] Ricerca, filtri combinati, stato "nessun risultato" e ripristino.
- [ ] Confronto prodotti: apertura, chiusura, limite di 3, nessuna specifica inventata.
- [ ] Menu mobile su smartphone reale (iOS e Android).
- [ ] Nessuno scorrimento orizzontale a 320, 360, 390, 768, 1024, 1440 px.
- [ ] Pagine leggibili con JavaScript disattivato.
- [ ] Tutti i collegamenti esterni (sito ufficiale, shop, LinkedIn, YouTube) rispondono.
- [ ] `mailto:` apre il programma di posta con indirizzo e oggetto corretti.
- [ ] Lighthouse mobile: Performance, Accessibilità, Best Practices, SEO.
- [ ] Anteprima di condivisione (WhatsApp, LinkedIn) con titolo e immagine corretti.

La suite di controlli usata finora (92 verifiche automatiche nel browser) è documentata nei messaggi
della pull request; per ripeterla sul sito online basta sostituire gli indirizzi `file://` con l'URL.

## 6. Dopo la pubblicazione

- Impostare un monitoraggio di disponibilità (anche gratuito).
- Se si aggiunge un form di contatto o statistiche, aggiornare privacy policy e informativa cookie **prima**.
- Aggiornare `docs/STATO_E_PROVENIENZA.md` con la data di pubblicazione e la versione online.
