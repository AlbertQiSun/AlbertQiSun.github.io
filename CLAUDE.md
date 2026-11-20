# CLAUDE.md

Personal academic homepage built on the al-folio v1.x starter (Jekyll). Layouts, includes and Sass live in the `al_folio_*` gems, not here — prefer changing content/data/config over shadowing gem files. `AGENTS.md` and `docs/` are upstream docs for the template itself (their `/al-folio` baseurl note does **not** apply: this site uses a blank baseurl).

## Local preview (Windows → WSL, no Docker)

```bash
wsl -e bash -lc 'bash /mnt/d/NYU/HomePage/bin/serve-wsl.sh'   # http://localhost:4000/
```

On Linux, `jekyll build` needs a UTF-8 locale (`LANG=C.UTF-8`), otherwise al_folio_core fails with "invalid byte sequence in US-ASCII".

Ruby 3.4 lives in the WSL conda env `jekyll`; gems in `~/.gems/homepage`. From Git Bash, don't pass `/mnt/...` paths to `wsl` directly (MSYS path mangling) — wrap in `bash -lc`. `_config.yml` changes need a server restart.

## Deploy

Repo: `AlbertQiSun/AlbertQiSun.github.io` → https://albertqisun.github.io. Pushing to `main` runs `.github/workflows/deploy.yml`, which builds and force-pushes `_site` to the `gh-pages` branch; Pages serves `gh-pages` (`.nojekyll` keeps GitHub from re-running Jekyll). The `upstream` remote is the al-folio template (unrelated history — reference only). Use `--repo AlbertQiSun/AlbertQiSun.github.io` with `gh` if it ever resolves to upstream.

## Where content lives (single source of truth)

| Content | File(s) |
| --- | --- |
| Papers (publications page + homepage "selected") | `_bibliography/papers.bib`, previews in `assets/img/publication_preview/` |
| Venue badge colors/links | `_data/venues.yml` (key = bib `abbr`) |
| Coauthor links | `_data/coauthors.yml` |
| News | `_news/YYYY-MM-DD-slug.md` (`inline: true`). Rendered by `_includes/news_list.liquid` (separate rows, no scroll box): the homepage shows the newest 6 (`visible=6` at the end of `_pages/about.md`; the layout's `announcements` is disabled) with the rest under a collapsible "Older news"; `/news/` lists all |
| Bio, photo, homepage sections | `_pages/about.md`, `assets/img/prof_pic.jpg` |
| Social icons | `_data/socials.yml` |
| CV | `assets/pdf/cv.pdf` (maintained in LaTeX elsewhere; CV page just embeds it) |
| Blog | `_posts/` (blog list + homepage "latest posts"); `read_time:` in a post's front matter overrides the word-count estimate (used by `_pages/blog.md`) |
| RSI report, public blog edition | `blog/rsi-report/` — **generated, don't hand-edit**. Rebuild with `bash bin/rsi-blog/build.sh` (clones `AlbertQiSun/rsi-report`, drops Section 6 and every Ling mention, English only, translates the reference metadata, builds with `BASE=/blog/rsi-report`). The post `_posts/2026-11-18-is-ai-improving-itself.md` redirects there. The interview page `/rsi-report/` is served by the `rsi-report` repo itself and is not touched |
| Projects | `_projects/` |
| Name bolding in author lists | `scholar.first_name/last_name` in `_config.yml` |

Placeholders are marked `TODO` — `grep -rn TODO _config.yml _pages _data _news _bibliography`.

## Conventions

- Under-review papers: no venue name (`abbr = {Preprint}`) until accepted.
- Keep customizations in `_config.yml`, `_data/`, content folders; avoid adding `_layouts/`, `_includes/`, `_sass/` overrides (new includes with their own names, like `_includes/news_list.liquid`, are fine: they shadow nothing) so gem upgrades stay painless (bump pins in both `Gemfile` and `_config.yml` `plugins:`).
- The one deliberate override is `assets/css/main.scss` (shadows the gem's copy). It sets the theme colors (`$purple-color` = light mode, `$cyan-color` = dark mode, both the report's accent blue) and ends with a "Report theme" block that restyles the whole site after the RSI report (warm paper background, Inter / Noto Sans SC + Fragment Mono via `third_party_libraries.google_fonts` in `_config.yml`, hairline rules, pill chips). PurgeCSS runs in CI, so only target classes that appear in the built HTML. After bumping `al_folio_core`, diff it against the gem's `assets/css/main.scss`.
- Paper 2 (Search, Do not Guess) is accepted to EACL 2027 (Nov 2026): `abbr = {EACL}`, `@inproceedings` with the EACL booktitle. Never post review scores.
- Status text for `@misc` entries goes in `note` (rendered under the year); `howpublished` is not displayed.
- Author markers: `*` equal contribution, `†` corresponding author (e.g. `Zhang*†, Siyue`), explained in `annotation`. Siyue Zhang and Chen Zhao are corresponding authors on PDA and DistOPD.
