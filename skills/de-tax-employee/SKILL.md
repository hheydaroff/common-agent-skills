---
name: de-tax-employee
description: "Prepare a German income tax return (Einkommensteuererklärung) as an employee, ending in a filled-in ELSTER worksheet the user submits themselves. Use for 'Steuererklärung', 'tax return Germany', 'Anlage N', 'Werbungskosten', 'Pendlerpauschale', 'Homeoffice-Pauschale', 'ELSTER', 'vorausgefüllte Steuererklärung', 'Steuerbescheid prüfen', or deciding whether to file at all. Covers duty vs voluntary filing, deadlines, intake, Werbungskosten vs Arbeitnehmer-Pauschbetrag (with calculator), which Anlagen to add, ELSTER line mapping, and checking the Bescheid. Year-keyed figures with sources. NOT for self-employed, civil servants, pensioners, freelancers, crypto or capital-gains detail, or foreign income."
---

# German tax return as an employee (Arbeitnehmer)

Goal: a complete, correct ELSTER worksheet for ONE tax year, plus a list of what to upload/keep. The user clicks "Absenden". This is guidance, not Steuerberatung.

## Non-goals (say so if asked)
Selbständige/Gewerbe, Beamte, Rentner, Vermietung (Anlage V), Kapitalerträge/Krypto (Anlage KAP/SO: only flag the trigger, then stop), Auslandseinkünfte (N-AUS, WA-ESt), Kinder-Details. For these: tell the user a Steuerberater or Lohnsteuerhilfeverein is the right tool.

## Hard rules
1. **Ask the tax year first.** Every figure is year-keyed. Use `references/parameters.md`. If the year is newer than the newest column there, say the numbers are unverified and check the sources in `references/sources.md` before using them.
2. **Never assume a missing value is 0.** Ask, or mark `?` in the output.
3. **Never log into ELSTER, handle the certificate, or submit.** Produce the worksheet; the user enters and sends it. Do not write Steuer-ID, IBAN or salary into the repo or memory. Scratch work only in a fresh `mktemp -d`.
4. Line numbers (Zeile) refer to the paper/PDF form of that year; ELSTER online matches by label. Quote the label, then the Zeile.
5. Cite the source for each year-specific number in the final answer (see `references/sources.md`).

## Workflow

### 1. Must I file, may I file, by when?
Check `references/parameters.md` section "Duty & deadlines". Decide: **Pflichtveranlagung** (e.g. Steuerklasse III/V or IV+Faktor, Freibetrag on the Lohnsteuerkarte, >410 € income without Lohnsteuer, Lohnersatz >410 €, Steuerklasse VI/several employers, "S" on the Lohnsteuerbescheinigung) or **Antragsveranlagung** (voluntary, 4 years back, refund only).
Compute today's date against the deadline. Past a Pflicht deadline: file now, expect a Verspätungszuschlag, do not wait for a request. Voluntary filing is almost always worth it when Werbungskosten, Sonderausgaben, Handwerker/haushaltsnahe costs, or a mid-year job/class change exist.

### 2. Intake
Run the questionnaire in `references/intake.md` (one block at a time, not all at once). Ask for the *Lohnsteuerbescheinigung* first: it fixes Brutto, Lohnsteuer, Soli, Kirchensteuer, and what the employer already netted (Jobticket, Fahrtkostenzuschuss, Reisekosten).

### 3. Pull what the tax office already knows
Tell the user to open Mein ELSTER → Vorausgefüllte Steuererklärung → **Belegabruf** (needs consent in the account, available ~1 day after consenting; covers last 4 years: Lohnsteuerbescheinigung, Kranken-/Pflegebeiträge, Riester/Rürup, Lohnersatz, Stammdaten). Anything pre-filled should be *checked*, not typed again.

### 4. Werbungskosten vs. Pauschbetrag
The Arbeitnehmer-Pauschbetrag is deducted automatically; only the part of real Werbungskosten **above** it lowers tax. Compute with:

```bash
uv run python scripts/wk_calc.py --year 2025 --km 18 --office-days 90 --home-days 120 \
  --other 250 --jobticket-subsidy 0
```
Options: `--car` (own car: lifts the 4 500 € cap), `--oepnv-cost N` (actual ticket cost, used if higher), `--no-konto` (skip the 16 € Kontoführung flat), `--pauschbetrag N` (override). It prints each component, the total, and the excess over the Pauschbetrag. Full rules and traps: `references/anlage-n-map.md`.

Don't double count: a day is either an office day (Entfernungspauschale) or a Homeoffice day (6 €), not both, unless no other workplace was available (Zeile 59). Homeoffice-Tagespauschale and Arbeitszimmer (Zeile 57) are mutually exclusive for the same period.

### 5. Other Anlagen the employee usually needs
Hauptvordruck + **N** always. Then by trigger (details in `references/anlage-n-map.md` §Other Anlagen):
- **Vorsorgeaufwand**: only if Basis-KV/PV paid exceeds what the employer already counted, or Rürup/private premiums. Belegabruf pre-fills most.
- **Sonderausgaben**: Spenden, Kirchensteuer *gezahlt/erstattet*, Ausbildungskosten. Pauschbetrag is only 36 € (72 € joint), so any real item matters.
- **Haushaltsnahe Aufwendungen**: Handwerker 20 % up to 1 200 €, Dienstleistungen 20 % up to 4 000 €, Minijob 20 % up to 510 €. Needs invoice + bank transfer; cash is rejected.
- **Außergewöhnliche Belastungen**: Krankheitskosten etc., only above the zumutbare Belastung.
- **N-Doppelte Haushaltsführung**, **Kind**, **KAP/SO** etc.: add on trigger; for KAP/SO stop at "flag".

### 6. Deliver the worksheet
Use the format in `references/intake.md` §Output: per Anlage, per Zeile label → value → source document → status (✔ confirmed / ? open). End with: estimated extra deduction over the Pauschbetrag, open questions, and documents to keep (Belegvorhaltepflicht: receipts are kept, sent only on request).

### 7. After submission
Follow `references/elster-workflow.md` §After: compare the Bescheid with the worksheet, watch the one-month Einspruchsfrist, note any Vorbehalt der Nachprüfung / Vorläufigkeit.

## Traps seen in the research
- Commute: **one-way** km, whole km only, only days actually at the first Tätigkeitsstätte; sick/holiday/Homeoffice days don't count. 2025: 0.30 €/km to km 20, 0.38 € from km 21. **From 2026: 0.38 € from km 1.** Don't apply 2026 rates to 2025.
- Employer Jobticket / tax-free subsidies reduce the Entfernungspauschale (Zeilen 51/52); a ticket you pay yourself can beat the flat rate.
- Computer/software: full deduction in the year of purchase; other Arbeitsmittel ≤ 800 € net deduct in full; above that spread over useful life. Private share must be split out.
- A Homeoffice day is not a Pendlertag; count both separately from a calendar.
- Fünftelregelung for Abfindung/mehrjährigen Lohn: since 2025 only through the return, not payroll (Zeilen 16/17).
- Company-car changes (Fahrtenbuch) need the tick in Anlage N Zeile 10.
- Blog "Steuertipps" pages are often a year behind: prefer elster.de, finanzamt.nrw.de, bundesfinanzministerium.de, gesetze-im-internet.de.
