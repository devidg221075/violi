# VIOLI MACCHINE — Regole del progetto / Master 1.1

Esportazione del 7 novembre 2026. Raccoglie le regole recuperate dalla conversazione “violi”, le richieste esplicite dell’utente e le note necessarie a proseguire il progetto. Le misure implementate nella ricostruzione non sono presentate come misure originali approvate.

## 1. Obiettivo e riferimenti

Tre pagine di riferimento: Homepage V3, Catalogo Prodotti V2 e Categoria Per Filo V1. Nella conversazione precedente risultavano approvate. La direzione visiva è Light Premium: bianco dominante, verde e oro, hero luminosa, macchinario protagonista e fotografie industriali grandi.

Le tre anteprime sono in `03-MOCKUP`. La Master 1.1 aggiorna l’identità cromatica e il logo della Master 1.0 mantenendo l’impostazione approvata. Le varianti storiche servono come archivio e non sostituiscono il riferimento scelto.

## 2. Identità ufficiale

| Elemento | Regola |
| --- | --- |
| Logo | Usare l’autentico `VIOLI_MACCHINE.svg`; non ricostruirlo o ridisegnarlo |
| Verde primario | `#045327` |
| Oro | `#C29536` |
| Verde secondario nel logo | `#025227` |
| Fondi | Bianco e avorio chiaro |
| Font di progetto proposti | Montserrat per titoli e pulsanti; Inter per testi |

Verde per azioni principali, titoli, icone e navigazione attiva. Oro per dettagli, linee, bordi e accenti. Pulsanti principali verdi; secondari con bordo oro. La versione ricostruita usa Montserrat per h1/h2 e Inter per testo, h3 e controlli: è un dettaglio dell’implementazione, non una nuova approvazione tipografica.

Il logo originale ha margini molto ampi nel foglio SVG. `violi-logo-web.svg` conserva i tracciati e cambia soltanto il viewBox per la visualizzazione. L’originale inalterato è conservato nel sito e nella cartella logo. Usarlo in header, footer e menu mobile dove previsto, senza deformazioni o tagli.

Le tavole PNG e le fotografie dei mockup possono contenere loghi provvisori e tonalità storiche. Sono riferimenti visivi raster: per tracciati e codici esatti prevalgono SVG ufficiale e valori riportati qui. Non campionare i colori dalle fotografie per ridefinire la palette.

## 3. Vincoli di conservazione

- Non riprogettare le pagine già approvate.
- Non cambiare arbitrariamente layout, proporzioni, testi, hero e immagini.
- Non modificare le spaziature mobile già corrette della Homepage V3.
- Preservare loghi, scritte e geometria dei macchinari; non tagliare elementi importanti.
- Conservare struttura delle sezioni, disposizione delle schede e gerarchie tipografiche.
- Conservare ricerca, filtri e navigazione.
- Evitare animazioni di comparsa che lascino contenuti invisibili e grandi spazi vuoti.
- Le schede del catalogo devono esistere nell’HTML ed essere visibili senza JavaScript.
- Usare stili condivisi per mantenere coerenza tra pagine.

La fedeltà esatta agli HTML perduti non è verificabile. L’attuale esportazione è una ricostruzione dalle anteprime, da valutare come tale; non è una copia certificata delle versioni approvate.

## 4. Homepage V3 — struttura di riferimento

1. Header con navigazione, logo e richiesta preventivo.
2. Hero luminosa: macchina a destra, titolo “Da oltre 30 anni, tecnologie Made in Italy nel mondo”, dato 2.000 macchine / 50 Paesi, pulsanti prodotti e azienda.
3. Tre settori: Macchine industriali, Industria orafa, Recupero metalli preziosi.
4. Otto categorie originali del catalogo; non riutilizzare le categorie industriali generiche apparse nelle prime immagini esplorative.
5. Presentazione aziendale con anteprima video.
6. Violi nel mondo, mappa e dati 2.000+, 50+, 30+.
7. Plus aziendali e footer con contatti ufficiali.

I plus originali sono “Ascoltiamo le tue necessità”, “Costruiamo Made in Italy”, “Assistenza garantita”. I testi Tecnologia / Qualità / Supporto presenti in alcuni mockup sono parte dello storico visivo.

## 5. Catalogo V2 — contenuti e comportamento

Otto categorie originali:

1. Per Filo.
2. Per Tubo.
3. Per Lavaggio ad Ultrasuoni.
4. Per Pulitura.
5. Per Bricchettare Trucioli.
6. Per Ceneri.
7. Per Catalizzatori.
8. Per Schede Elettroniche.

La pagina comprende hero, ricerca testuale, filtri categoria/settore/applicazione, griglia categorie, tre macchinari in evidenza e area PDF/supporto/confronto. Filtri combinabili, stato senza risultati e ripristino. Le otto categorie e le tre schede in evidenza sono contenuti statici nell’HTML.

Le denominazioni VP / IU / BT nelle schede in evidenza provengono dall’immagine del mockup; non sono specifiche commerciali verificate. Il confronto è dimostrativo e non deve inventare velocità, dimensioni, capacità o altri dati tecnici.

## 6. Per Filo V1 — struttura e quattro famiglie

Hero chiara con macchina e filo, breadcrumb, titolo, descrizione e inviti ad approfondire o richiedere informazioni. Introduzione “Soluzioni per il filo”. Quattro schede su due colonne desktop e una colonna smartphone:

1. Trafile a passaggi multipli per filo.
2. Bobinatore per filo.
3. Trafile per filo Bull Block.
4. Raddrizzatrici per filo con taglio al volo.

Seguono richiesta di soluzione personalizzata, vantaggi aziendali e contatti. Le schede comprendono fotografia, descrizione e accesso alla scheda prodotto; la ricostruzione aggiunge il collegamento per richiedere informazioni.

## 7. Responsive e visibilità

Le correzioni registrate nella chat per la V3 eliminavano l’altezza minima fissa di 605 px della hero, riducevano le distanze tra immagini, testi e sezioni, rendevano compatta la sezione aziendale/video ed eliminavano la dipendenza dalle animazioni di comparsa su mobile.

Non introdurre altezze minime eccessive, elementi invisibili che occupano spazio o grandi vuoti fra hero, video e contenuti successivi. Il menu deve funzionare su smartphone, i controlli essere raggiungibili e le immagini restare leggibili. Verificare ogni aggiornamento sia su desktop sia su mobile.

Nella ricostruzione attuale i breakpoint sono 1500, 1180, 950 e 600 px. Sono scelte implementative ricostruite, non valori recuperati dal codice originale. Per tutte le misure effettive prevale `01-SITO/assets/style.css`.

## 8. Immagini e materiali

Sono inclusi i tre mockup recuperati integralmente. I riquadri fotografici del sito provengono da queste immagini, visualizzati tramite CSS; non sono stati rigenerati. Sono immagini illustrative dei prototipi, non fotografie certificate dei prodotti effettivi. Non dichiararle native ad alta risoluzione né sostituirle senza confronto con il riferimento.

Le tavole ad alta risoluzione sono incluse nei formati recuperati. La dimensione in pixel di ogni PNG è riportata nell’inventario; l’aumento di dimensione non dimostra nuovo dettaglio fotografico.

## 9. Funzioni presenti e predisposizioni

Presenti: navigazione locale tra tre pagine, menu mobile nativo HTML, ricerca, filtri combinati, stato vuoto/ripristino, collegamenti iniziali con filtro settore, confronto dimostrativo, link alle pagine ufficiali e richieste via email.

Predisposizioni: PDF tecnici e video sono collegamenti di approfondimento al sito ufficiale, senza documenti PDF o filmati incorporati. Preventivi e informazioni aprono il programma di posta, non inviano messaggi automaticamente. Le categorie non ricostruite e le schede dettagliate aprono il sito ufficiale.

Assistente virtuale, confronto tecnico reale, mappa interattiva avanzata, area assistenza e integrazione CMS erano funzionalità future discusse: non sono consegnate come già operative.

## 10. Verifiche richieste per le modifiche future

Controllare tutte e tre le pagine, la comparsa delle schede con JavaScript assente, menu, immagini, ricerca/filtri, stato senza risultati e collegamenti. Confrontare i mockup prima di modificare il disegno. Controllare almeno desktop, smartphone e larghezze ridotte, senza scorrimento orizzontale. Non dichiarare verifiche o approvazioni non svolte.

## 11. Consegna e uso

`01-SITO/index.html`, `catalogo.html`, `per-filo.html` condividono la cartella assets: mantenerla insieme alle pagine. I corrispondenti file `*-autonomo.html` incorporano risorse e possono essere aperti singolarmente. Tenerli nella stessa cartella per navigare tra loro.

L’archivio include regole, brief, mockup, tavole, logo, caratteri con licenze, verifiche e materiali intermedi disponibili. Non è un’esportazione integrale della cronologia ChatGPT: gli allegati HTML storici non recuperabili non sono stati reinseriti come se fossero originali.
