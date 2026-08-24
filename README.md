---
license: cc-by-4.0
pretty_name: Digital Nomad & Long-Stay Visa Dataset (45 countries, sourced & dated)
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

Long-stay, remote-work and nomad visa records — one per country — each sourced to an official
government page and carrying the date it was last checked.

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

Every figure is checked against the destination country's own government source — the immigration
ministry, consulate or national visa portal that issues the permit — and that URL travels with the
record in `official_url`.

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
- **No scraped third-party content.** Records are compiled from primary government sources, which
  is why each one can carry a link you can check yourself.

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
