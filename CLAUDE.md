# CLAUDE.md

Personal academic homepage built on the al-folio v1.x starter (Jekyll). Layouts, includes and Sass live in the `al_folio_*` gems, not here — prefer changing content/data/config over shadowing gem files. `AGENTS.md` and `docs/` are upstream docs for the template itself (their `/al-folio` baseurl note does **not** apply: this site uses a blank baseurl).

## Local preview (Windows → WSL, no Docker)

```bash
wsl -e bash -lc 'bash /mnt/d/NYU/HomePage/bin/serve-wsl.sh'   # http://localhost:4000/
```

Ruby 3.4 lives in the WSL conda env `jekyll`; gems in `~/.gems/homepage`. From Git Bash, don't pass `/mnt/...` paths to `wsl` directly (MSYS path mangling) — wrap in `bash -lc`. `_config.yml` changes need a server restart.

## Where content lives (single source of truth)

| Content | File(s) |
| --- | --- |
| Papers (publications page + homepage "selected") | `_bibliography/papers.bib`, previews in `assets/img/publication_preview/` |
| Venue badge colors/links | `_data/venues.yml` (key = bib `abbr`) |
| Coauthor links | `_data/coauthors.yml` |
| News | `_news/YYYY-MM-DD-slug.md` (`inline: true`) |
| Bio, photo, homepage sections | `_pages/about.md`, `assets/img/prof_pic.jpg` |
| Social icons | `_data/socials.yml` |
| CV | `assets/pdf/cv.pdf` (maintained in LaTeX elsewhere; CV page just embeds it) |
| Projects / Blog | `_projects/`, `_posts/` — pages hidden via `nav: false` until there is content |
| Name bolding in author lists | `scholar.first_name/last_name` in `_config.yml` |

Placeholders are marked `TODO` — `grep -rn TODO _config.yml _pages _data _news _bibliography`.

## Conventions

- Under-review papers: no venue name (`abbr = {Preprint}`) until accepted.
- Keep customizations in `_config.yml`, `_data/`, content folders; avoid adding `_layouts/`, `_includes/`, `_sass/` overrides so gem upgrades stay painless (bump pins in both `Gemfile` and `_config.yml` `plugins:`).
- The one deliberate override is `assets/css/main.scss` (shadows the gem's copy) to set NYU violet theme colors (`$purple-color` = light mode, `$cyan-color` = dark mode). After bumping `al_folio_core`, diff it against the gem's `assets/css/main.scss`.
- Paper 2 (Search, Do not Guess) is under review at ARR — keep `abbr = {Preprint}` / "Under review" with no venue or scores until accepted.
