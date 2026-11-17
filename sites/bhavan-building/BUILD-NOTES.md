# Bhavan Building: build notes

- Source: Trade Websites sheet row 43 (submitted 7/1/2026)
- Domain: https://www.bhavanbuilding.com.au (canonical and schema point here)
- Preview: https://bhavan-building.vercel.app
- Built: 2026-11-17 by Claude with the go-polar-site-build skill
- Phone on site: 0426 045 004 / Form key: client key

## Design

- Direction: Photographs at uneven sizes (taste-skill uneven-photographs), green-black and bone, pale jade on the enquiry button only
- Idea: Bhavan's 'select number of projects' becomes a gallery wall: each finished room hung like a print with space around it, and the registration number signed under the work
- Live thing: Room filter on the project wall re-hangs the wall by room (All, Kitchens, Bathrooms, Laundries)
- Type: Newsreader 300/400/500 standing in for the dealt Sentient (Fontshare is unreachable from the build container), self-hosted
- Palette: Dealt 'green-black and bone' kept, it matches the dark fluted kitchen; no logo to sample
- Redraw: about: portraits pass needs team photos, none exist, so side facts and wide paragraph
- Decision: Contact blueprint has no form; house rule needs one, so the band keeps its geometry and the enquiry form follows it
- Decision: No video: client photos only

## Pages

- /
- /kitchen-renovations-melbourne/
- /bathroom-renovations-melbourne/
- /laundry-renovations-melbourne/
- /home-extensions-rebuilds-melbourne/
- /service-areas/
- /projects/
- /about/
- /contact/

## Photos

- `arch`: kitchen-fluted-arch.jpg (Dark fluted timber kitchen with an arched rangehood alcove, granite splashback and curved island)
- `wf1`: kitchen-waterfall-1.jpg (Timber and white kitchen with a marble-look waterfall island and three pendant lights)
- `wf2`: kitchen-waterfall-2.jpg (Waterfall island bench with a black sink and pull-down mixer under white pendants)
- `vanity1`: bath-double-vanity-1.jpg (Double timber vanity with two vessel basins and brushed brass wall mixers)
- `vanity2`: bath-double-vanity-2.jpg (Bathroom with brass shower rail, vertical gloss tiles and a timber double vanity)
- `basin`: bath-vessel-basin.jpg (Round vessel basin on a white stone top with a brushed brass mixer)
- `powder`: powder-terracotta.jpg (Powder room with terracotta wall tiles, terrazzo floor and an organic mirror)
- `laundry1`: laundry-sage-1.jpg (Sage green shaker laundry with stacked Miele washer and dryer)
- `laundry2`: laundry-sage-2.jpg (Sage green laundry cabinetry with a steel sink and white subway tiles)
- `laundry3`: laundry-black-timber.jpg (Laundry with black and oak cabinetry, terracotta tiles and Bosch machines under the bench)

## Flags for the client (confirm before go-live)

- [ ] Two phone numbers on the form: best contact 0474 906 716, website number 0426 045 004. The site uses 0426 045 004 as asked. CONFIRM which one Abi answers.
- [ ] No logo supplied, though the colours answer was 'match my logo'. Built a type wordmark and a 'B' favicon; palette (green-black, bone, pale jade) taken from the dark fluted kitchen photo. CLIENT TO SUPPLY logo files, then remap the palette.
- [ ] Reviews answered 'yes' but none were supplied, so there is no testimonials section and no review schema. CLIENT TO SUPPLY Google review link and wording.
- [ ] Address given as 'Bentliegh East' with no street. Corrected spelling; built as a Bentleigh East service-area business with no street shown. Postcode 3165 assumed.
- [ ] Suburb list cleaned: Oakliegh to Oakleigh, beumaruis to Beaumaris, bonbeach to Bonbeach, 'ArmadaleAshburton' split into two, duplicate Camberwell and Hawthorn removed. Grouped into five council-area regions (assumption).
- [ ] No photos of extensions or knock-down rebuilds. The extensions page uses kitchen photos from open-plan renovations. CLIENT TO SUPPLY build photos.
- [ ] powder-terracotta.jpg is 480x640 and laundry-black-timber.jpg is a phone shot; both used small only.
- [ ] About copy says the name means 'house' (Bhavan is Hindi and Sanskrit for a house or building). CONFIRM Abi is happy with that line.
- [ ] Client was told free hosting until 1 August then $30/month (old offer). Confirm plan before go-live.

## Editing

Change `_src/site.json`, `_src/build.py`, `_src/site.css` or `_src/site.js`, then:

```
python3 sites/bhavan-building/_src/build.py && python3 _kit/verify.py sites/bhavan-building
```

Commit and push to main; the workflow redeploys only this folder.
