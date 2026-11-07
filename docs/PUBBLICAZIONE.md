# Checklist di pubblicazione — Violi Macchine

Stato al momento della stesura: **nulla è stato pubblicato**. Questo documento elenca cosa
serve prima di mettere il sito online e come farlo. Le misure sotto sono state rilevate
aprendo le pagine in locale.

## 1. Blocchi da risolvere prima di pubblicare

| # | Punto | Perché | Chi |
|---|-------|--------|-----|
| 1 | **Fotografie reali dei prodotti** | Le immagini del sito sono ritagli dei tre mockup (`assets/*-riferimento.png`), illustrazioni non certificate che mostrano anche marchi provvisori. Non vanno pubblicate come fotografie dei prodotti. | Violi: fornire le foto |
| 2 | **Approvazione della ricostruzione** | Gli HTML approvati originali sono andati persi (`docs/STATO_E_PROVENIENZA.md`): le pagine attuali non sono ancora state approvate dal cliente. | Cliente |
| 3 | **Prodotti VP / IU / BT** | Nomi e abbinamenti arrivano dal mockup, non sono verificati. Il confronto non contiene dati tecnici (corretto). | Violi: confermare |
| 4 | **Informativa privacy** | Il sito non usa cookie né analytics, ma i contatti avvengono via email e nel footer manca il collegamento alla privacy policy. Oggi punta a `violimacchine.it/it/contatti`. | Violi / consulente |
| 5 | **Dati aziendali** | Controllare indirizzo, telefono, P.IVA e email del footer (presi dal sito ufficiale il 7 novembre 2026). | Violi |
| 6 | **PDF e video** | I pulsanti rimandano al sito ufficiale: non ci sono PDF né video propri. | Violi: materiali |

## 2. Miglioramenti tecnici consigliati (non bloccanti)

Peso misurato in locale (senza compressione del server):

| Pagina | Peso | Voce più pesante |
|--------|------|------------------|
| Home | 5,3 MB | `homepage-riferimento.png` 2,1 MB + `catalogo-riferimento.png` 2,1 MB |
| Catalogo | 3,6 MB | `catalogo-riferimento.png` 2,1 MB |
| Per Filo | 3,3 MB | `per-filo-riferimento.png` 2,2 MB |

- **Immagini**: con le foto reali, esportarle in WebP/AVIF a più larghezze (`srcset`); oggi le pagine caricano l'intero mockup per mostrarne un ritaglio.
- **Font**: 8 file TTF da circa 2 MB in totale. Convertire in WOFF2 (circa -60%) e caricare solo i pesi usati (Montserrat 600/700, Inter 400/500/600).
- **Meta**: aggiungere `canonical` e Open Graph/Twitter card (titolo, descrizione, immagine 1200×630) quando il dominio è definito.
- **File mancanti**: `robots.txt`, `sitemap.xml`, `404.html`, favicon PNG/`apple-touch-icon` per i dispositivi che non leggono l'SVG.
- **Dati strutturati**: `Organization` e `LocalBusiness` (JSON-LD) con i dati aziendali.

## 3. Hosting consigliato (sito statico, nessuna build)

Il repository si pubblica così com'è: la radice contiene `index.html`, `catalogo.html`, `per-filo.html` e `assets/`.

**Vercel** — Framework preset *Other*, Build command vuoto, Output directory `.` (radice).
**Cloudflare Pages** — Framework preset *None*, Build command vuoto, Build output directory `/`.

Prima di collegare il ramo di produzione, escludere `docs/` e `tools/` dal deploy (non servono online):
- Vercel: file `.vercelignore` con `docs`, `tools`, `dist`.
- Cloudflare Pages: spostare le pagine in `public/` oppure usare una build che copia solo i file del sito.

Intestazioni consigliate (Vercel `vercel.json` / Cloudflare `_headers`):

```
/assets/*   Cache-Control: public, max-age=31536000, immutable
/*.html     Cache-Control: public, max-age=0, must-revalidate
/*          X-Content-Type-Options: nosniff
/*          Referrer-Policy: strict-origin-when-cross-origin
```

Se i nomi dei file in `assets/` cambiano a ogni modifica, la cache lunga è sicura; altrimenti
aggiungere un suffisso di versione ai file modificati.

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
