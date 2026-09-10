# Chase Golden Globe — site rebuild (10 September 2026)

## How to deploy
1. Copy everything in this folder into the root of the GitHub Pages repo, replacing the existing files.
2. The `assets/` folder is additive: it adds `hero-handshake.jpg`, `hero-map-wall.jpg`, `hero-notebook.jpg` and the regenerated `i18n.js`, and re-supplies files that were already there. It does not remove anything. `hero-lobby.jpg`, `hero-presence.jpg`, `favicon.ico` and `favicon-32.png` are not in this zip — they are already on the server and still used (hero-presence is no longer referenced and can be deleted; hero-office-port.jpg is also no longer used).
3. Commit and push. No build step is needed on the server.

## Editing later
- Page content lives in `build.py` (structure) and `i18n_src.py` (every string, in EN / AR / ID).
- Run `python3 build.py` after any change: it regenerates the eight HTML pages and `assets/i18n.js`, and checks that every translation key used in the pages exists.
- `map.svg` is the simplified world map used on Home and Presence.
- `style.css` and `script.js` are hand-written; edit directly.

## Image slots that would benefit from a new photo
- `assets/hero-notebook.jpg` — About, chapter 1 (placeholder; brief: Indonesian teak furniture workshop, warm daylight, 3:2, ≥2400px wide)
- `assets/hero-contact-new.jpg` — About, chapter 2 (currently the desk-lamp shot; brief: finished luxury residence or embassy reception room, 3:2)
- `assets/hero-industries.jpg` — now the Home hero (1408×768; a 2880px-wide re-export would be sharper on large screens)
- All other heroes are 1376–1600px wide; fine for now, re-export at ~2400px when convenient.

## Things to review
- Arabic and Indonesian are AI-drafted throughout (the file says so in its first line). A native-speaker read before you consider the languages "official" is still recommended.
- Presence page country cards: the one-line role per country (Saudi Arabia, Qatar, UAE, Egypt, UK, Switzerland, Luxembourg) is in `i18n_src.py` under `pres.c.*` — confirmed as correct, easy to edit there.
- Legal page shows "Last updated: September 2026" — update the `legal.updated` string when the page changes.

## What changed vs. the previous site (summary)
Fixed: unclosed `<main>` on Contact and Industries; beige gap above every hero; capabilities grid stretching; map zoom replaced by highlight-and-label; contrast failures on khaki panels; tap targets ≥40px; breadcrumbs, Presence cards and "(HQ)" now translated; language buttons labelled; About tabs support arrow keys; manifest colours; country count now "10 countries, four regions, incl. HQ" everywhere; placeholder "history in progress" note removed; Retail & Hospitality copy corrected; capabilities meta now matches the page; founder bio has a subject; Legal page gains Questions block and a last-updated line.
Added: Home capabilities strip, sectors band and presence teaser; Capabilities "Between opportunity and capital" block (due diligence, investor reporting, pitch preparation); About timeline with years and a photo per chapter; founder portrait plate; Contact copy-email button and head-office line; disclaimer moved to the footer bottom bar (visible on mobile); twitter:card and apple-touch-icon tags; llms.txt and sitemap refreshed.
