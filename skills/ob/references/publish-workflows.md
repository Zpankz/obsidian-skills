# Publish Workflows

## First-Time Publish Setup

```bash
# 1. List available sites
ob publish-list-sites

# 2. Link vault to site (run from vault directory)
cd /path/to/vault
ob publish-setup --site my-site-slug

# 3. Always preview first
ob publish --dry-run

# 4. Publish
ob publish --yes
```

---

## Frontmatter-Based Publishing

The most precise control. Add to individual note YAML frontmatter:

```yaml
---
publish: true   # Always publish this file regardless of folder rules
---
```

```yaml
---
publish: false  # Never publish (overrides --all and folder includes)
---
```

Files with no `publish` key: included only if they are in an included folder or `--all` is passed.

**Priority order (highest to lowest):**
1. `publish: true/false` frontmatter
2. Configured includes/excludes (`ob publish-config`)
3. `--all` flag

---

## Folder-Based Publishing

Configure which folders are eligible:

```bash
# Include only specific top-level folders
ob publish-config --includes "Blog,Public Notes,Projects/Published"

# Exclude private folders (affects files without explicit publish frontmatter)
ob publish-config --excludes "Private,Archive,Drafts,Templates"

# View current config
ob publish-config

# Clear all includes (publish nothing by default without --all)
ob publish-config --includes ""
```

---

## Publish All Untagged Files

```bash
ob publish --all --yes
```

Includes files without a `publish` frontmatter key, subject to folder rules.

---

## Safe Publish Workflow (Always Dry-Run First)

```bash
# Step 1: see what would change
ob publish --dry-run --path /vaults/blog

# Step 2: if it looks right, publish
ob publish --yes --path /vaults/blog
```

---

## CI/CD Publish Pipeline

```yaml
name: Publish Obsidian Site

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '22'

      - run: npm install -g obsidian-headless

      - name: Login
        run: ob login --email "${{ secrets.OB_EMAIL }}" --password "${{ secrets.OB_PASSWORD }}"

      - name: Setup publish (idempotent)
        run: |
          ob publish-setup --site "${{ secrets.OB_SITE_SLUG }}" --path . 2>/dev/null || true

      - name: Dry run
        run: ob publish --dry-run --path .

      - name: Publish
        run: ob publish --yes --path .
```

---

## Site Appearance Configuration

```bash
# Set basic options
ob publish-site-options \
  --site-name "My Digital Garden" \
  --index-file "Home.md" \
  --default-theme dark

# Enable all sidebar features
ob publish-site-options \
  --show-navigation true \
  --show-graph true \
  --show-backlinks true \
  --show-search true \
  --show-outline true

# Set navigation order
ob publish-site-options \
  --nav-order "Home,Blog,Projects,Notes,About"

# Upload logo
ob publish-site-options --logo assets/logo.png

# Clear logo
ob publish-site-options --logo ""

# View current options
ob publish-site-options
```

---

## Incremental Publishing

`ob publish` is incremental by default — it compares local file hashes against the remote site and only uploads new/changed files and removes deleted ones. No special flags needed; every publish run is efficient.