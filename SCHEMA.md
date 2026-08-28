# Schema — `data/visas.json`

One UTF-8 JSON object. Top-level metadata, then `records`: an array with **one object per
programme**, sorted by `slug`. A country may hold several — group by `country_slug`.

**The one rule that matters:** `null` means the government has not published that rule. It never
means "no". Every field below is always present on every record — a value is either populated or
explicitly `null`, never absent.

Empty strings follow the same convention as `null`: unknown or not published, never "none".
List fields (`requirements`, `steps`, `faqs`) use `[]` for genuinely empty, never `null`.

---

## Top level

- **`dataset`** *(string)* — the dataset's name, for attribution: `GlobeNomad Visa Dataset`.
- **`description`** *(string)* — one-line description of what the file contains.
- **`source`** *(string)* — canonical landing page: `https://globenomad.com/data`.
- **`method_url`** *(string)* — how records are verified: `https://globenomad.com/how-we-verify`.
- **`license`** *(string)* — `CC BY 4.0`.
- **`license_url`** *(string)* — `https://creativecommons.org/licenses/by/4.0/`.
- **`attribution`** *(string)* — the credit line to reproduce when using the data.
- **`null_means`** *(string)* — the null rule, restated inside the file so it travels with the
  data even when the README does not.
- **`last_verified_at`** *(string, `YYYY-MM-DD`)* — the newest `verified_at` across all records.
  This is a property of the **data**, not of the build: it does not change when the file is
  regenerated without changes. For "when was this file built", use the git commit date.
- **`record_count`** *(integer)* — number of objects in `records`. This is a count of
  **programmes**, not countries; several records may share a `country_slug`.
- **`records`** *(array)* — the records, sorted by `slug` ascending.

---

## Record — identity

- **`slug`** *(string)* — stable URL-safe **record** identifier, e.g. `costa-rica` or
  `thailand-education`. The primary key: unique across the file, and the last segment of
  `page_url`. One country may hold several, one per programme.
- **`country_slug`** *(string)* — stable URL-safe **country** identifier, e.g. `costa-rica`,
  `thailand`. **Group by this, not by `slug`.** Not unique: Thailand's four records share it.
- **`country`** *(string)* — country name in English, e.g. `Costa Rica`.
- **`region`** *(string)* — broad grouping used for browsing. Editorial, not a standards body's
  list. The complete set of values in this file is `Africa`, `Americas`, `Asia`, `Europe`,
  `Middle East`. (Before 2026-08-27 this field was documented with the examples `Latin America`
  and `Asia-Pacific`, which have never been values — filtering on either returned nothing.)
- **`page_url`** *(string)* — the human-readable page for this record on globenomad.com, with the
  sourcing and caveats written out. The natural citation target for a single country.

## Record — programme

- **`programme_name`** *(string)* — a short label for the route within its country, e.g.
  `Digital Nomad Visa (DTV)`, `Education Visa (ED)`. Present so a consumer can label a row without
  parsing `slug`. Always populated, and equal to `visa_name` on countries holding a single record;
  it differs only where a country runs several routes and each needs naming briefly. Never use it
  to detect single-record countries — count `country_slug` instead.
- **`visa_name`** *(string)* — the programme's own name, e.g. `D8 Digital Nomad Visa`. Where a
  country has no dedicated route, this describes what the record covers instead.
- **`program_status`** *(string, enum)* — one of:
  - `open` — accepting applications.
  - `closed` — existed, no longer accepting. The record stays published because other sites still
    list these as live.
  - `announced_not_open` — legislated or announced, with no procedure to apply yet.
  - `none` — no nomad route at all; other visa types may still apply.
- **`summary`** *(string)* — a short plain-English description of the route.

**Operational fields are meaningless when `program_status` is not `open`.** A closed programme has
no processing time. Expect `null` and empty strings across most of the record in that case, and do
not read them as zeros.

## Record — money

- **`min_income_usd`** *(integer | null)* — minimum monthly income requirement converted to USD.
  Governments set these in local currency and they drift with exchange rates: treat it as a
  bracket for comparison, not a threshold to plan against. `null` where no income test is
  published, or where the requirement is a savings balance rather than monthly income.
- **`income_original`** *(string)* — the requirement as the government publishes it, including
  currency and framing, e.g. `€3,680 per month` or `฿500,000 in accessible funds`. **This is the
  authoritative form**; `min_income_usd` is a convenience.
- **`cost_usd`** *(integer | null)* — headline application fee in USD. Excludes downstream costs
  (residence cards, legalisation, translation, insurance) which vary too widely to compare.

## Record — duration and renewal

- **`max_stay_months`** *(integer | null)* — longest single permitted stay under the visa,
  including renewals granted as part of the same permit.
- **`processing_time`** *(string)* — published or commonly reported decision time, e.g.
  `2–4 months`. Free text because governments express this inconsistently.
- **`renewable`** *(boolean | null)* — whether the permit can be extended beyond its first term.
- **`max_total_years`** *(integer | null)* — total years obtainable including renewals.
- **`renewal_note`** *(string)* — conditions, caveats or contradictions around renewal.

## Record — settling

- **`pr_path`** *(boolean | null)* — whether time on this visa counts toward permanent residency.
  **`null` here is the single most dangerous field to render wrongly** — see the rule at the top.
- **`pr_after_years`** *(integer | null)* — years of residence before PR becomes available.
- **`citizenship_path`** *(boolean | null)* — whether the route can eventually lead to citizenship.
- **`citizenship_after_years`** *(integer | null)* — years before naturalisation becomes available.

## Record — tax

Tax treatment is jurisdiction-specific and interacts with your home country's rules and any treaty
between them. These fields describe the destination's published position only.

- **`tax_residency_days`** *(integer | null)* — days in-country that trigger tax residency.
- **`foreign_income_taxed`** *(boolean | null)* — whether foreign-earned income is taxed locally
  once you are tax resident.
- **`special_tax_regime`** *(boolean | null)* — whether a nomad- or expat-specific rate or
  exemption exists. What it actually is lives in `tax_note`: the shapes differ too much between
  countries to compare as a number.
- **`tax_note`** *(string)* — the detail, including where sources disagree.

## Record — family

- **`dependents_allowed`** *(boolean | null)* — whether a partner and children can be included.
- **`spouse_income_add_usd`** *(integer | null)* — additional monthly income required for a partner.
- **`child_income_add_usd`** *(integer | null)* — additional monthly income required per child.
- **`family_note`** *(string)* — conditions on dependants (age limits, proof of relationship,
  separate applications).

## Record — applying

- **`requirements`** *(array of string)* — documents and conditions the applicant must satisfy.
  Ordered as published where the source is ordered.
- **`steps`** *(array of string)* — the application process in order.
- **`apply_from_abroad`** *(boolean | null)* — `true` means the application must be made before
  travelling; `false` means it is made from inside the country.
- **`apply_method`** *(string, enum)* — one of `consulate`, `online`, `in_country`, `mixed`, or
  `""` when not established.
- **`logistics_note`** *(string)* — practical caveats: appointment backlogs, consulate-specific
  requirements, biometrics.
- **`faqs`** *(array of object)* — question/answer pairs, each `{"question": string, "answer": string}`.

## Record — provenance

- **`official_url`** *(string)* — the government page the record was checked against. The reason
  to cite this dataset rather than re-scrape one.
- **`verified_at`** *(string `YYYY-MM-DD` | `""`)* — the date this record was last checked against
  that source. On globenomad.com the corresponding badge disappears after twelve months; apply the
  same scepticism here rather than assuming a record is current because the file is.

---

## Stability

- **`slug` is the primary key** and is unique across the file.
- **⚠ `slug` was redefined on 2026-08-27** — see [`CHANGELOG.md`](CHANGELOG.md). It was documented
  here as a *country* identifier that "does not change when a programme is renamed or replaced".
  The exporter had always written the record's page address into it, and the two agreed only
  because every country held exactly one record. When Thailand's DTV moved to `/visa/thailand-nomad`
  so `/visa/thailand` could list all four Thai routes, that promise broke: the row keyed
  `"thailand"` in the 2026-08-24 file does not exist in this one. **`country_slug` is what `slug`
  was documented to be**, and it is the field to key on if you were relying on that promise.
- Fields are added, not renamed or repurposed. A consumer reading unknown fields as optional will
  not break on an update.
- If a field must ever be withdrawn, it stays present as `null` rather than disappearing, so
  parsers keyed on its presence keep working.
