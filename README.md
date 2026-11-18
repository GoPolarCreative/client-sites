# Go Polar client sites

Every Go Polar managed website lives here, one folder per client.

## How it works

- `sites/<client-slug>/` is one client's website, for example `sites/turquoise-plumbing/`.
- The folder name is the Vercel project name. Use lowercase letters, numbers and hyphens only.
- Pushing to `main` deploys only the sites whose folders changed. Each site gets its own Vercel project and `.vercel.app` preview link, created automatically on its first deploy.
- To redeploy one site by hand: Actions > Deploy client sites > Run workflow > enter the folder name.
- The `VERCEL_TOKEN` repository secret powers the deploys. Never commit tokens or keys to this repo.

## Going live

1. Approve the preview link with the client.
2. In Vercel, open the client's project > Settings > Domains and add their domain.
3. Point the domain's DNS at Vercel (Cloudflare or Synergy Wholesale).

## Handing a site over

If a client asks for their website after their 3 month minimum, copy their folder into its own repo with its history:

```
git subtree split --prefix=sites/<client-slug> -b handover-<client-slug>
```

Push that branch to a new repo and transfer it to the client.

## Folder contents

```
_kit/                  shared mechanics: gpkit.py (shell, SEO, schema, images, fonts, og-image, favicons),
                       gp.js / gp.css (nav, reveals, lightbox, Web3Forms), verify.py (checks + screenshots)
builds.json            registry of built sites and the questionnaire rows they came from
sites/<slug>/          the deployed static site (index.html per page, assets/, sitemap, robots, vercel.json)
sites/<slug>/_src/     source, never deployed: site.json (client data), build.py (pages and copy),
                       site.css, site.js, img/ (client photos), flags.json
sites/<slug>/BUILD-NOTES.md   direction, idea, pages, photos and the flags to confirm with the client
```

The kit holds mechanics only. Every site writes its own layout, CSS and copy, so no two sites share a composition.

Rebuild and check one site:

```
python3 sites/<slug>/_src/build.py && python3 _kit/verify.py sites/<slug>
```

Needs Python 3 with Pillow, fonttools, brotli, cairosvg and Playwright, Node 22 (for fonts via npm), and Chrome.

## Instant enquiry auto-reply

`_kit/autoreply/Code.gs` runs as a Google Apps Script web app ("Go Polar enquiry auto-reply", on chrismoule96@gmail.com). After Web3Forms accepts an enquiry, the site posts the customer's name and email to it, and it replies instantly in the client's business name with Reply-To set to the client. New clients only: never switch it on for existing or rebuilt past clients. Turn it on per site with `"autoreply": {"enabled": true, "on_job": "on the tools"}` in `_src/site.json`; the build writes `autoreply.json`, which the script reads. Limit: about 100 auto-replies a day across all sites (Gmail quota).
