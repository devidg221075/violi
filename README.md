# Violi Macchine — sito (Light Premium, Master 1.1)

Sito statico, senza build né dipendenze: apri `index.html` nel browser.

- `index.html`, `catalogo.html`, `per-filo.html` — le tre pagine, collegate tra loro
- `assets/` — CSS, JS, font (Inter, Montserrat, licenze OFL), logo SVG, immagini di riferimento
- `riferimenti/` — dati del confronto dimostrativo
- `docs/` — regole Master 1.1, brief, stato e provenienza, verifiche, mockup approvati
- `assets/icone/` — 24 icone ufficiali del kit vettoriale (varianti `currentColor`); `assets/violi-logo-web-bianco.svg` per i fondi scuri
- `tools/build_sprite.py` — incorpora lo sprite delle icone nelle tre pagine (rieseguirlo se cambiano le icone)
- `tools/build_standalone.py` — genera in `dist/` le versioni autonome (un solo file per pagina)
- `tools/build_seo.py` — meta tag, 404, robots e sitemap (opzione `--domain`)
- `tools/build_public.py` — crea `public/`, la cartella da pubblicare
- `docs/PUBBLICAZIONE.md` — checklist per mettere il sito online
- `docs/kit-vettoriale/` — kit vettoriale Master 1.1 (icone nei tre colori, componenti SVG, tavola riepilogativa)

## Stato

Le pagine sono una **ricostruzione** dalle anteprime di Homepage V3, Catalogo V2 e Per Filo V1:
gli HTML approvati originali sono andati persi. Leggere `docs/REGOLE_MASTER_1.1.md` e
`docs/BRIEF_PER_RIPRENDERE_IL_LAVORO.md` prima di modificare. Nessuna pubblicazione effettuata.

Colori: verde `#045327`, oro `#C29536`. Logo: `assets/VIOLI_MACCHINE.svg` (originale, da non modificare).

## Versioni autonome

```bash
python3 tools/build_standalone.py
```
