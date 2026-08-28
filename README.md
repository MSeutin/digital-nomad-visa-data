---
license: cc-by-4.0
pretty_name: Digital Nomad & Long-Stay Visa Dataset (51 programmes, 46 countries, sourced & dated)
language:
  - en
size_categories:
  - n<1K
tags:
  - visa
  - immigration
  - digital-nomad
  - remote-work
  - expat
  - government
  - open-data
---

# GlobeNomad Visa Dataset

Long-stay, remote-work and nomad visa records — **one per programme** — each sourced to an
official government page and carrying the date it was last checked.

**A country may hold several records.** Thailand publishes four: the DTV, the education visa, the
retirement route and the Non-B. Group by `country_slug`, not by `slug` — `slug` is the record key.
See [`CHANGELOG.md`](CHANGELOG.md) if you are holding a file from before 2026-08-27, when this
was one row per country.

**Free to use, including commercially, under [CC BY 4.0](LICENSE). The only condition is
attribution.**

- **Download:** [`data/visas.json`](data/visas.json)
- **Field reference:** [`SCHEMA.md`](SCHEMA.md)
- **About the dataset:** <https://globenomad.com/data>
- **How records are verified:** <https://globenomad.com/how-we-verify>

## Why this exists

Visa rules are published by dozens of governments in dozens of formats — most unstructured,
several self-contradicting, and a few describing programmes that shut years ago. Anyone building
a tool, running a study or writing about where people can legally live and work has to assemble
this by hand first.

So it is published: the whole set, the same records that power every country page on
[globenomad.com](https://globenomad.com), regenerated from the same database. Not a sample, not
a teaser for a paid tier.

## Read this before you render it

**A `null` value means the government has not published that rule. It never means "no".**

A record whose `pr_path` is `null` must not be displayed as *"No permanent residency path"* — no
source says that, and someone may plan a move around it. Show unknown as unknown.

Every field is present in every record. A value is either populated or explicitly `null`, so you
never have to work out whether a missing key means an unknown answer or a dropped field.

## How it is verified

Every record carries the URL it was checked against, in `official_url`, and for most that is the
issuing authority itself — the immigration ministry, consulate, e-visa portal or the programme's
own government site.

**It is not the issuing authority for every record, and the field tells you which.** Some
governments publish nothing usable, and a few block automated reads outright: the Philippine
EO 86 record is sourced to a law library because the government pages return 403, and a handful of
programmes are documented only by a national tourism or investment board. Where that happens the
record links what was actually read rather than a government URL that does not carry the figure —
check `official_url` before citing a record as a government source. We would rather publish the
substitution than imply a provenance the file does not have.

- Records are re-checked at least once a year, and immediately when we learn a rule changed.
- Where an official page is ambiguous or contradicts itself, a second reputable source is
  cross-checked. Where sources genuinely conflict, the field is left `null` rather than guessed.
- Closed and never-launched programmes stay in the set with an honest `program_status` instead of
  being quietly deleted. *"This closed in 2024"* is a fact people need and almost nobody publishes.
- Income requirements are set in local currency and move with exchange rates. Treat `min_income_usd`
  as a bracket, not a threshold; `income_original` carries the government's own wording.

Full method: <https://globenomad.com/how-we-verify>

## What is deliberately not in here

- **No affiliate or tracking links.** globenomad.com is funded by affiliate referrals, and the
  dataset is kept clear of them on purpose. Data you can cite has to be data nobody paid to shape.
- **No images.** The country photography on the site is not covered by this licence — only the
  data is.
- **No scraped third-party content.** Records are compiled from official sources — primarily
  government ones, and where none is usable, the best available published source, named in
  `official_url` so you can judge it yourself. Nothing here is lifted from another visa site.

## Attribution

CC BY 4.0 asks for credit and a link. Paste this, or anything that names the dataset and links
back:

```html
Data: <a href="https://globenomad.com/data">GlobeNomad Visa Dataset</a>, CC BY 4.0
```

Plain text:

```text
GlobeNomad Visa Dataset — https://globenomad.com/data — CC BY 4.0
```

No registration, no API key, no rate limit, no email address to hand over, nothing to renew.

## Corrections

If you have just been through one of these applications, you know the current rules better than
any published page does — consulates change requirements faster than they update their websites.

Open an issue here, or send it through <https://globenomad.com/contact> with the country and what
you ran into. It gets checked against the official source and fixed in the dataset and on the site
at the same time. Corrections are the single most useful thing anyone can send.

## Regenerating

The file is generated from the live database, not hand-edited:

```sh
go run ./cmd/export-dataset
```

Re-running on unchanged data produces a byte-identical file, so `git diff` on `data/visas.json` is
an exact record of what changed in the dataset and when.

## Licence

[CC BY 4.0](LICENSE) — Creative Commons Attribution 4.0 International.

The dataset is provided as-is. It is not immigration advice: GlobeNomad reports what official
rules say and links to where they say it. For a complicated case — unusual nationality,
dependants, or tax-residency questions — pay a professional in the destination country.
