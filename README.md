# RWCheck — Retraction Watch BibTeX Screener

[![GitHub Marketplace](https://img.shields.io/badge/Marketplace-RWCheck-blue?logo=github)](https://github.com/marketplace/actions/rwcheck-retraction-watch-bibtex-screener)
[![Test action](https://github.com/khan-lab/rwcheck-action/actions/workflows/test.yml/badge.svg)](https://github.com/khan-lab/rwcheck-action/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Automatically screen the `.bib` files in your repository against the
[Retraction Watch](https://retractionwatch.com/) database on every push or pull
request. The action fails the workflow (or emits a warning) when retracted
references are detected, and writes a rich Markdown summary to the GitHub
Actions job summary page.


## What it does

1. Installs the [`rwcheck`](https://github.com/khan-lab/rwcheck) Python package.
2. Downloads and caches the Retraction Watch database (≈ 50 MB CSV → SQLite).
3. Finds all `.bib` files in the repository (or a pattern you supply).
4. Checks every reference that has a DOI or PMID against the database.
5. Writes a job summary with counts and a table of any retracted entries.
6. Fails the workflow — or emits a `::warning::` annotation — depending on
   your `fail-on-retraction` setting.


## Usage

### Basic — check all `.bib` files, fail on retraction (default)

```yaml
- uses: khan-lab/rwcheck-action@v1
```

### Warn only — report findings without failing the workflow

```yaml
- uses: khan-lab/rwcheck-action@v1
  with:
    fail-on-retraction: 'false'
```

### Check a specific file or glob pattern

```yaml
- uses: khan-lab/rwcheck-action@v1
  with:
    bib-files: 'paper/references.bib'
```

### Pin to a specific `rwcheck` version for reproducibility

```yaml
- uses: khan-lab/rwcheck-action@v1
  with:
    rwcheck-version: '1.1.0'
```

### Use the outputs in a subsequent step

```yaml
- uses: khan-lab/rwcheck-action@v1
  id: rw
  with:
    fail-on-retraction: 'false'

- name: Summary
  run: |
    echo "Checked ${{ steps.rw.outputs.total-count }} references."
    echo "Retracted: ${{ steps.rw.outputs.retracted-count }}"
```

### Full example workflow

```yaml
name: Reference check

on: [push, pull_request]

jobs:
  rwcheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: khan-lab/rwcheck-action@v1
        with:
          bib-files: '**/*.bib'
          fail-on-retraction: 'true'
          post-summary: 'true'
```


## Inputs

| Input | Required | Default | Description |
|---|---|---|---|
| `bib-files` | No | `**/*.bib` | Glob pattern for `.bib` files to check, relative to the repo root. |
| `fail-on-retraction` | No | `true` | Set to `false` to emit a warning instead of failing the workflow. |
| `rwcheck-version` | No | `latest` | Version of `rwcheck` to install. Pin (e.g. `1.1.0`) for reproducibility. |
| `post-summary` | No | `true` | Write a Markdown summary table to the GitHub Actions job summary. |


## Outputs

| Output | Description |
|---|---|
| `retracted-count` | Total number of retracted references found across all checked `.bib` files. |
| `total-count` | Total number of references checked. |
| `unchecked-count` | References with no DOI or PMID that could not be verified. |


## Job summary example

When retracted references are found, the action posts a summary like:

| Metric | Count |
|---|---|
| Total references checked | 127 |
| **Retracted** | **2** |
| Clean (not found) | 121 |
| Unchecked (no DOI/PMID) | 4 |

**Retracted entries**

| Key | Title | Nature | Date | Journal | Reason |
|---|---|---|---|---|---|
| `stapel2011` | Coping with chaos: How disordered contexts … | Retraction | 2011-11-03 | Science | Data fabrication |
| `fujii2012` | The effects of… | Retraction | 2012-07-01 | Anesthesiology | Data fabrication |


## Requirements

- Runs on `ubuntu-latest` (Linux runners only — the action uses `bash` and Python 3).
- References must have a `doi` or `pmid` field to be checked; entries without
  either are counted as *unchecked* and never flagged.


## Related

- **[rwcheck](https://github.com/khan-lab/rwcheck)** — the underlying Python
  package (CLI, REST API, Python library).
- **[Retraction Watch](https://retractionwatch.com/)** — the database of
  retracted, corrected, and expression-of-concern papers.


