# Intake and output format

Ask one block at a time. Record answers as `field: value (source)`; unknown = `?`. Do not write personal data to the repo.

## Block 0 — frame
- Tax year? Today's date vs deadline (parameters.md).
- Single, married/eingetragene Partnerschaft (Zusammen-/Einzelveranlagung)? Steuerklasse(n) during the year, any change?
- Resident in Germany all year? (Move in/out of Germany → stop: Anlage WA-ESt, outside scope.)
- Already have a Mein ELSTER account + consent for Belegabruf? Which Bundesland/Finanzamt (Steuernummer vs new application)?
- Prior returns filed (so Steuernummer and Vorjahr data exist)?

## Block 1 — income documents
- Lohnsteuerbescheinigung per employer (Brutto, Lohnsteuer, Soli, KiSt, Steuerklasse, "S", Jobticket/Zuschüsse, Reisekostenerstattung).
- Several employers, gaps, unemployment, Elterngeld/Kurzarbeit/Krankengeld, Abfindung?
- Any income without tax withheld > 410 €; Nebengewerbe, Vermietung, Kapitalerträge beyond the Sparer-Pauschbetrag, Krypto/Gold/Aktien sales → flag out-of-scope Anlagen.

## Block 2 — commute and workplace (feeds Anlage N 27–34)
- Address of erste Tätigkeitsstätte; one-way km (whole km, shortest road or clearly faster usual route)?
- Days actually at the site (not holiday/sick/Homeoffice/Dienstreise)? Calendar or badge data is better than a guess.
- Mode: own car, Fahrgemeinschaft, ÖPNV (Deutschlandticket cost), mixed? Employer Jobticket/subsidy?
- Move or job change mid-year (split blocks)?
- Homeoffice days (no office), and was a desk available at the office on Homeoffice days?
- Separate Arbeitszimmer being the Mittelpunkt of all work? (Rare; Tagespauschale is the default.)

## Block 3 — job costs
Arbeitsmittel (PC, monitor, desk, chair, phone share, books), Fortbildung/Kurse, Gewerkschaft/Berufsverband, Bewerbungen, Umzug (job-caused), Dienstreisen not fully refunded, doppelte Haushaltsführung. For each: date, net amount, paid by whom, employer refund, private share.

## Block 4 — private deductions
Kirchensteuer (gezahlt/erstattet), Spenden (receipts), Krankheitskosten, Handwerker/Haushaltshilfe (invoice + transfer), KV/PV and Rürup/private insurance beyond what Belegabruf shows, Kinder (flag).

## Output format (deliver exactly this)
```
Tax year: YYYY | Deadline: … | Type: Pflicht / Antrag
Anlagen to file: Hauptvordruck, N, … (reason each)

Anlage N
 Zeile 27 Erste Tätigkeitsstätte: <value>   [source]   ✔/?
 Zeile 29 Arbeitstage: …
 …
Werbungskosten total: X €  vs Pauschbetrag 1 230 €  →  extra deduction: Y €  (approx. tax effect = Y × your marginal rate; say that the rate is unknown if not given)

Other Anlagen: <label> → value → source ✔/?
Open questions: …
Keep for 'Belegvorhaltepflicht': receipt list …
Not covered (see non-goals): …
Sources: ids from sources.md
```
Say clearly: estimate, not a binding result; the Finanzamt decides.
