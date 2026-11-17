# Monthly suburb page

On the 1st of each month every site in `builds.json` with `"monthly_pages": true` gets one new suburb page. The order was planned at the original build in `sites/<slug>/_src/plan.json`.

## How a site is set up for it

- `_src/plan.json`: `pattern` (URL, for example `/builder-{slug}/`), `base` (the client's base suburb), `queue` (suburbs in order: nearest and highest value first, only suburbs the client listed), `done` (published pages).
- `_src/suburbs/<suburb-slug>.json`: one file per published page. The site's `build.py` renders every file through `s.suburbs()`, links each page from the areas page, and links neighbours that already have pages to each other.
- Reference: `sites/bhavan-building` (`suburbs/bentleigh.json` and the `for sp in SUBURB_PAGES` block in `build.py`). A site without that block needs it added once, in that site's own design.

## The monthly run, per site

1. `git pull --rebase`. Skip a site whose `queue` is empty and tell Chris it has run out.
2. Take the first suburb in `queue`. Research it with web search: postcode, council, distance and drive time from `base`, neighbouring suburbs, the housing stock (era, styles, block sizes), planning controls that matter for this trade (heritage or character overlays, flood or bushfire overlays), and anything about the suburb that changes the work (old galvanised pipes, clay sewers, coastal corrosion, slab or stumps). Keep the source URLs.
3. Write `_src/suburbs/<slug>.json` with the same fields as the reference: `suburb, postcode, council, region, distance_km, drive_min, neighbours, title, desc (165 max), h1 [two parts], lead, sections [3 x {h, p}], focus_services [service slugs], photos [3 keys from site.json images], faq [3 x [q, a]], published, sources`.
   - At least half of each page must be about this suburb. If the text would still be true with another suburb name swapped in, rewrite it.
   - Never invent jobs done there, clients, reviews or times on site. "We have built in X" only if the client said so.
   - Title `Trade Suburb | services | Business`, H1 starts with the trade and the suburb.
4. Move the suburb from `queue` to `done` in `plan.json` with its path and date.
5. `python3 sites/<slug>/_src/build.py && python3 _kit/verify.py sites/<slug>`. Fix until PASS, then look at the new page's first screen at both widths in `_src/shots/`.
6. Append a dated line to `## Edits` in `BUILD-NOTES.md`: `YYYY-MM-DD: added /path/ (Suburb)`.
7. Commit `Monthly page <slug>: <Suburb>` and push. The deploy workflow publishes it and the sitemap updates with it.
8. Report to Chris: site, new page URL on the live domain if live (preview otherwise), the next suburb in the queue, and anything that needed a guess.
