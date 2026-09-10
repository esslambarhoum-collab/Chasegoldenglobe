# Chase Golden Globe — site rebuild v4.1 (10 September 2026)

## How to deploy
1. Copy everything in this folder into the root of the GitHub Pages repo, replacing the existing files.
2. This zip is complete: `assets/` contains every file the site references, including the favicons. A full replace of the repo folder is safe.
3. Commit and push. No build step is needed on the server.

## Editing later
- Page content lives in `build.py` (structure) and `i18n_src.py` (every string, in EN / AR / ID).
- Run `python3 build.py` after any change: it regenerates the eight HTML pages and `assets/i18n.js`, and checks that every translation key used in the pages exists.
- `map.svg` is the simplified world map used on Home and Presence.
- `style.css` and `script.js` are hand-written; edit directly.

## Image map (v4.1)
- Home hero: `hero-home.jpg` (boardroom over the port) · Home sectors band: `hero-industries.jpg` (port aerial)
- About hero: `hero-lobby.jpg` · chapters: `chapter-2006.jpg` (workshop), `chapter-2010.jpg` (gilded interior), `hero-capabilities.jpg` (boardroom)
- Capabilities hero: `hero-handshake.jpg` · due-diligence block: `capabilities-desk.jpg`
- Industries hero: `hero-sectors.jpg` (farmland / solar / port aerial) · Presence hero: `hero-map-wall.jpg` · Contact hero: `hero-contact-new.jpg`
- All photos are 1264–1408px wide. Fine on laptops; re-export at ~2400px for large retina screens when convenient.

## Things to review
- Arabic and Indonesian are AI-drafted throughout (the file says so in its first line). A native-speaker read before you consider the languages "official" is still recommended.
- Presence page country cards: the one-line role per country (Saudi Arabia, Qatar, UAE, Egypt, UK, Switzerland, Luxembourg) is in `i18n_src.py` under `pres.c.*` — confirmed as correct, easy to edit there.
- Legal page shows "Last updated: September 2026" — update the `legal.updated` string when the page changes.

## What changed vs. the previous site (summary)
Fixed: unclosed `<main>` on Contact and Industries; beige gap above every hero; capabilities grid stretching; map zoom replaced by highlight-and-label; contrast failures on khaki panels; tap targets ≥40px; breadcrumbs, Presence cards and "(HQ)" now translated; language buttons labelled; About tabs support arrow keys; manifest colours; country count now "10 countries, four regions, incl. HQ" everywhere; placeholder "history in progress" note removed; Retail & Hospitality copy corrected; capabilities meta now matches the page; founder bio has a subject; Legal page gains Questions block and a last-updated line.
Added: Home capabilities strip, sectors band and presence teaser; Capabilities "Between opportunity and capital" block (due diligence, investor reporting, pitch preparation); About timeline with years and a photo per chapter; founder portrait plate; Contact copy-email button and head-office line; disclaimer moved to the footer bottom bar (visible on mobile); twitter:card and apple-touch-icon tags; llms.txt and sitemap refreshed.
