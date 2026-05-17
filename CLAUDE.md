# CLAUDE.md — vee-labs/vee-labs

> Claude Code reads this file at the start of every session. Follow all instructions exactly. No deviation without explicit user approval.

---

## Project Identity

- **Org:** vee-labs
- **Source repo:** `vee-labs/vee-labs`
- **Docs source:** `docs/` (VitePress Markdown)
- **Sync targets:**
  - `vee-labs/vee-labs.github.io` → https://vee-labs.github.io (static site via GitHub Pages)
  - https://veelabs1.wordpress.com (WordPress.com via REST API)
- **Trigger:** Any commit touching `docs/**` or `scripts/sync_wordpress.py` fires both sync workflows automatically via GitHub Actions

---

## Data Flow (Read Before Any Docs Task)

```
vee-labs/vee-labs
  └── docs/           ← All content lives here (VitePress Markdown)
        │
        ├── [pages.yaml]           → builds & deploys to vee-labs.github.io
        └── [wordpress-sync.yaml]  → runs sync_wordpress.py → veelabs1.wordpress.com

Single commit to docs/** = both destinations updated simultaneously.
```

**Never** write content outside `docs/`. **Never** manually push to `vee-labs.github.io`. The pipeline handles it.

---

## Primary Task: Repo → Docs Pipeline

When instructed to generate or update documentation:

### Step 1 — Inventory All Repos

```bash
gh repo list vee-labs --limit 100 --json name,description,updatedAt,primaryLanguage \
  | jq '.[] | {name, description, updatedAt, primaryLanguage}'
```

For each repo, collect:
- `README.md` (root)
- Top-level directory structure (`find . -maxdepth 2 -type f -name "*.md"`)
- `package.json` / `pyproject.toml` / `Cargo.toml` (language/stack detection)
- Recent commit messages (`git log --oneline -10`)

### Step 2 — Generate Docs Content

For each repo, create or update a corresponding file in `docs/`:

```
docs/
  index.md              ← Landing page (auto-generated summary of all repos)
  projects/
    <repo-name>.md      ← One file per repo
  guides/               ← Any cross-cutting technical guides
  changelog.md          ← Auto-generated from recent commits across all repos
```

**Content schema per repo page (`docs/projects/<repo-name>.md`):**

```markdown
---
title: <repo name>
description: <one-line description>
updated: <ISO date>
---

# <Repo Name>

## What It Does
<2–3 sentence summary from README or inferred from code>

## Stack
<Languages, frameworks, key dependencies>

## Architecture
<High-level structure — key directories, data flow if applicable>

## Setup
<Install + run instructions, verbatim from README if present>

## Key Files
<3–5 most important files with one-line descriptions>

## Recent Changes
<Last 5 meaningful commits, formatted as a changelog>
```

**Rules for content generation:**
- Do not hallucinate. If a field has no source data, write `_Not documented._`
- Pull descriptions from README first, repo description second, code inference last
- Commit messages: filter out merge commits and bumps — include only meaningful changes
- Keep each page under 500 lines. Link out, don't embed

### Step 3 — Update Index

Regenerate `docs/index.md` with:
- Table of all projects (name, stack, last updated)
- Brief org mission statement (preserve existing if present)
- Links to each `docs/projects/<repo>.md`

### Step 4 — Commit and Trigger Pipeline

```bash
git add docs/
git commit -m "docs: auto-update from repo scan [$(date +%Y-%m-%d)]"
git push origin main
```

This commit triggers:
1. `pages.yaml` → builds VitePress → deploys to `vee-labs.github.io`
2. `wordpress-sync.yaml` → runs `sync_wordpress.py` → syncs to `veelabs1.wordpress.com`

**Do not run the sync script manually.** Let the Actions handle it.

---

## WordPress Sync Behavior

`scripts/sync_wordpress.py` handles Markdown → WordPress REST API sync.

- Each `.md` file in `docs/` maps to a WordPress post/page
- Front matter `title` and `description` map to WP post title and excerpt
- Do not modify `sync_wordpress.py` unless explicitly instructed
- If sync fails, check `WP_APP_PASSWORD` and `WP_USERNAME` in repo secrets

---

## Constraints

| Rule | Reason |
|------|--------|
| Never edit files in `vee-labs.github.io` repo directly | Pipeline overwrites on deploy |
| Never commit secrets or tokens to `docs/` | WordPress creds are in GitHub Secrets only |
| Always use front matter on every `.md` file | VitePress and sync script both require it |
| Keep `docs/` as the single source of truth | Both destinations pull from here |
| Don't create new GitHub Actions workflows | Existing `pages.yaml` + `wordpress-sync.yaml` cover all cases |

---

## Tech Stack Reference

| Component | Tool |
|-----------|------|
| Docs framework | VitePress |
| Static hosting | GitHub Pages (`peaceiris/actions-gh-pages`) |
| WordPress sync | Python (`sync_wordpress.py`) via WP REST API |
| CI/CD | GitHub Actions |
| Auth method (GH Pages) | PAT (Personal Access Token) |
| Auth method (WP) | Application Password via env secret |

---

## Commands You'll Use Often

```bash
# List all org repos
gh repo list vee-labs --limit 100

# Preview docs locally
cd docs && npx vitepress dev

# Build docs locally
cd docs && npx vitepress build

# Check workflow run status
gh run list --repo vee-labs/vee-labs --limit 5

# Watch live workflow
gh run watch --repo vee-labs/vee-labs

# Manually trigger wordpress sync (emergency only)
gh workflow run wordpress-sync.yaml --repo vee-labs/vee-labs
```

---

## Session Startup Checklist

At the start of every session involving docs or repos:

- [ ] Run `gh repo list vee-labs` to get current repo state
- [ ] Check `git status` in `vee-labs/vee-labs`
- [ ] Check last workflow run: `gh run list --limit 3`
- [ ] Confirm `docs/` structure matches expected layout above

---

## Auto-Memory Instructions

At the end of any session where you learned something new about this project (new repo found, sync error pattern, VitePress config quirk, WordPress API behavior), append a note to `MEMORY.md` in this format:

```
## [YYYY-MM-DD] <topic>
<1–3 sentences. Factual. No fluff.>
```

---

## Owner Context

Security engineer. Values: precision, minimal output, no padding. When in doubt — do less, confirm first. One sharp question beats three wrong actions.
