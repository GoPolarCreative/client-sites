# Metrowide Plumbing: build notes

- Source: Trade Websites sheet row 47 (submitted 7/10/2026)
- Domain: https://www.metrowideplumbing.com.au (canonical and schema point here)
- Preview: https://metrowide-plumbing.vercel.app
- Built: 2026-11-17 by Claude with the go-polar-site-build skill
- Phone on site: 0423 017 489 / Form key: client key

## Design

- Direction: The well-kept board (taste-skill dense-tiles), dark board, tiles on 8px gaps, action tiles cut on the logo's slant
- Idea: The slanted black band of the Metrowide logo, with its blue marker square, becomes the board; the name runs wider than its band the way 'metro wide' covers more than one suburb
- Live thing: 'Tell Dan what is going on': three taps (job, how soon, suburb) write the message, sent as an SMS or a Web3Forms enquiry
- Type: Libre Franklin 700/800/900 + 900 italic (display), Source Serif 4 400/600 (text), self-hosted
- Palette: Logo black #181818 and blue #46a0d2 on a #0f0f0f board, paper #f4f4f2, blue tints for the process accordion
- Redraw: work: book-spine index needs 20 to 40 project names, Metrowide has 7 photos, so giant title and uneven wall
- Redraw: about: team portraits do not exist, so wide photo, colour tile and facts
- Decision: No video: house rule is client photos only and no honest clip of Metrowide's work exists
- Decision: Inspector covered-text at 390px is the fixed mobile call bar passing over one statement tile

## Pages

- /
- /emergency-plumber-melbourne/
- /bathroom-renovation-plumbing-melbourne/
- /new-build-plumbing-melbourne/
- /commercial-plumbing-melbourne/
- /plumbing-maintenance-melbourne/
- /service-areas/
- /our-work/
- /about/
- /contact/

## Photos

- `green`: bath-green-tile.jpg (Bathroom with green finger tiles, terrazzo floor and a freestanding bath)
- `arch`: bath-terrazzo-arch.jpg (Terrazzo bathroom with black tapware, floating vanity and arch mirror)
- `double`: shower-double.jpg (Double shower with two black rail sets over white finger tile)
- `brassvan`: vanity-brass.jpg (Brushed brass wall mixer over an oval vessel basin)
- `brassshower`: shower-brass.jpg (Brushed brass rain head and hand shower on large grey tiles)
- `combo`: bath-laundry-combo.jpg (Bathroom and laundry in one room with black fixtures and a frameless screen)
- `under`: vanity-underside.jpg (Open vanity showing neat chrome waste and isolation valves beside a freestanding bath)

## Flags for the client (confirm before go-live)

- [ ] Service area was answered as 'All areas' with no city. Melbourne assumed (CONFIRM). Regions and suburbs on the areas page are a starting list for Dan to correct.
- [ ] No plumbing registration or licence number supplied. Research says trade sites convert better with it shown up front. CLIENT TO SUPPLY: VBA registration number.
- [ ] No insurance details supplied, so the site makes no insurance claim. CLIENT TO SUPPLY if covered.
- [ ] No reviews yet ('None as of yet'), so there is no testimonials section and no review schema. Add Google reviews when they come in.
- [ ] No business hours supplied. The site says emergency and same-day work (form answer Yes) but does not claim 24/7. CLIENT TO CONFIRM hours.
- [ ] No street address. Built as a service-area business with no address shown. Google Business Profile should match.
- [ ] Client chose to host elsewhere ('I'll set myself up and pay for hosting elsewhere'). Preview is on Vercel; confirm hosting before going live.
- [ ] All seven job photos are bathrooms. No photos of new build rough-ins, commercial work or maintenance callouts, so those pages reuse bathroom photos. CLIENT TO SUPPLY site photos.
- [ ] Logo arrived as a phone screenshot of the artwork. Cropped and made transparent; it holds up at header size but a vector original would be better.
- [ ] Photo bath-laundry-combo had a screen scrollbar on its right edge; trimmed 44px.

## Editing

Change `_src/site.json`, `_src/build.py`, `_src/site.css` or `_src/site.js`, then:

```
python3 sites/metrowide-plumbing/_src/build.py && python3 _kit/verify.py sites/metrowide-plumbing
```

Commit and push to main; the workflow redeploys only this folder.
