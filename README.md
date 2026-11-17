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

Each site folder holds the full source of that site (Astro or static HTML), its images, and a `BUILD-NOTES.md` recording the questionnaire answers it was built from and any edits made since.
