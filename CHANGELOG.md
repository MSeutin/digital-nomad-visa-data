# Changelog

Dated, breaking-change-first. If you hold an older copy of `data/visas.json`, read the entry for
the date you downloaded it and everything above.

## 2026-08-27 — one row per programme (shape change)

**Baseline: the previous public file, pushed 2026-08-24, held 45 records, one per country.**
If you hold that file, two things changed for you, and one of them is breaking.

### What changed

- **The file now carries one record per programme, not one per country.** 51 records across 46
  countries, up from 45 records. Thailand appears four times — the DTV, the education visa, the
  retirement route and the Non-B — where it previously appeared once. All six new records already existed on the
  site and were being withheld by the export.
- **The Philippines appears for the first time**, with two records — the SRRV Classic and the
  EO 86 digital nomad visa. It was absent from the 45-row file altogether, not merely reduced,
  so a consumer counting countries goes from 45 to 46.
- **🔴 BREAKING — one `slug` value changed.** Thailand's row was `slug: "thailand"`. That row no
  longer exists; the DTV is now `slug: "thailand-nomad"`, because its page moved to
  `/visa/thailand-nomad` when `/visa/thailand` became a chooser listing all four Thai routes.
  **Anyone who stored `"thailand"` as a key will not find it.** No other slug changed.
- **`slug` is now documented as the record key.** It always held the record's page address in
  practice; SCHEMA.md previously described it as a country identifier, and the two agreed only
  while every country held exactly one record.
- **`country_slug` added.** This is what `slug` was documented to be: the stable country key,
  shared by every record for that country. **Group by this.**
- **`programme_name` added.** A short label for the route within its country, so a row can be
  labelled without parsing the slug. Always populated, and equal to `visa_name` on countries
  holding a single record.
- `record_count` and the `description` inside the file now say "programme" where they said
  "country".

### What did NOT change

- No field was renamed, repurposed or removed. Every field present before is present now with the
  same meaning. `slug` kept its meaning too — what changed is one row's *value*, above, and the
  documentation, which was corrected to describe what the field always emitted.
- `null` still means the government has not published that rule. It never means "no".
- The licence is unchanged: CC BY 4.0, attribution the only condition.
- Records are still sorted by `slug` ascending, so `git diff` on the file stays reviewable.

### Migrating

- Grouping or joining by country: replace `slug` with `country_slug`.
- Expecting one row per country: you will now see several for countries running several routes.
  There is no flag marking a "main" route — deliberately, because we do not rank a country's
  programmes for you. To get one row per country, group by `country_slug` and pick by whatever
  your use case actually cares about (lowest income, longest stay, open status).
- Using `slug` as a stable primary key: still unique, still the primary key — but see the
  breaking note above. `"thailand"` is gone. If you cannot tolerate a key moving when a country
  gains routes, key on `country_slug` and pick a row.

### Why

The previous shape hid our deepest records. Thailand published as a single row while four fully
sourced records existed on the site, including a crackdown finding on the education visa and the
"the visa is not the work permit" correction on the Non-B — the kind of thing a dataset gets
cited for. A reference that under-reports what it holds argues against its own usefulness.

Recorded here rather than announced quietly because the 45-row file is already public and has
been since 2026-08-24, and a dataset that changes shape without saying so is precisely what this
one exists to be the opposite of.
