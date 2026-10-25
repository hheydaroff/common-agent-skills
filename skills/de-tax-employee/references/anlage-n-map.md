# Anlage N (tax year 2025) — Zeile map and rules

Source: ELSTER Anleitung 2025 (E1). Zeilen = paper/PDF form 2025. Online ELSTER follows the same labels. For another year, re-fetch the guide and re-map before use.

Anlage N is per person (spouses each fill their own). It can be skipped only if the employer's data came in electronically, Zeilen 10, 18, 19, 21–26 are empty, and Werbungskosten do not exceed the Pauschbetrag.

## Einnahmen
| Zeile | Label (short) | Take from |
|---|---|---|
| 5 | Bruttoarbeitslohn | normally pre-filled from Lohnsteuerbescheinigung (Belegabruf). Only overwrite for company-car corrections |
| 10 | Haken: Angaben abweichend (z.B. Fahrtenbuch) | tick if Zeile 5 changed |
| 16/17 | Entschädigungen / mehrjähriger Arbeitslohn (Fünftelregelung) | Lohnsteuerbescheinigung; related costs Zeile 79/80 |
| 18 | Arbeitslohn ohne Steuerabzug (foreign employer, third party) | own records; costs in Zeilen 27–77, 82 |
| 19 | steuerfreie Aufwandsentschädigung / Übungsleiter | only the actually tax-free part, only if not already in the Lohnsteuerbescheinigung |
| 20 | Lohn-/Entgeltersatz (steuerfrei, Progressionsvorbehalt) | Hauptvordruck Zeile 35 if not on the Bescheinigung |

## Werbungskosten
| Zeile | Label | Rule |
|---|---|---|
| 27 | Erste Tätigkeitsstätte (Ort) | employer-assigned permanent site; else the site you work at typically daily / 2 full days a week / ≥ 1/3 of working time. Max one per employment |
| 29 | Arbeitstage | only days actually at the site; no sick/holiday/Homeoffice/Dienstreise days |
| 30–33 | Entfernungskilometer (Pkw, Fahrgemeinschaft, ÖPNV, other) | **whole one-way km** of the shortest road link; a longer road is allowed if clearly faster and used regularly. Split km if mixed Pkw/ÖPNV (Zeilen 31/32/33) |
| 34 | Aufwendungen ÖPNV (ohne Fähre/Flug) | actual ticket cost; the higher of flat vs actual is used. Also valid if the ticket went partly unused (Homeoffice) |
| 38+ | second site / job change / move | separate block per employment or per period |
| 51/52 | Arbeitgeber-Zuschüsse (Jobticket, pauschal versteuert) | reduce the flat rate, floor 0 € |
| 54–56 | Arbeitsmittel | ≤ 800 € net: full that year. Computer HW/SW: full that year. Private-use share must be taken out |
| 57 | Häusliches Arbeitszimmer | only if the room is the Mittelpunkt of all work; actual cost or 1 260 €/yr (−1/12 per missing month). Excludes Tagespauschale same period |
| 58 | Homeoffice-Tage (kein Büro besucht) | 6 €/day, max 210 days |
| 59 | Homeoffice-Tage mit Büro-Besuch, wenn dauerhaft kein anderer Arbeitsplatz | same 6 €, shares the 210-day cap |
| 60 | Fortbildung / Zweitstudium / Umschulung | Gebühren, Fachliteratur, Material, Reise; minus Förderungen (Aufstiegs-BAföG, SGB III) |
| 62–64 | Weitere Werbungskosten (Gewerkschaft, Bewerbung, Kontoführung, Umzug, Unfallkosten, Fähr-/Flugkosten) | Berufsverband dues; Bewerbungen even if unsuccessful; Kontoführung 16 € flat without proof |
| 65–77 | Reisekosten (Auswärtstätigkeit) | Fahrt: actual or 0.30 € Pkw; Verpflegung 14/28 €, max 3 months, Kürzung for provided meals in Zeile 75; Übernachtung actual; tax-free employer refund in Zeile 71/77 reduces the claim |
| 78–83 | costs tied to Versorgungsbezüge, Fünftelregelung, N-AUS, no-tax-withheld wage, Belgium case | rare |

## Decide quickly
1. Total real Werbungskosten ≤ 1 230 € → they change nothing (flat is auto-applied); skip entering them unless another Anlage forces filing.
2. Total > 1 230 € → enter all of them; the excess lowers taxable income. Use `scripts/wk_calc.py`.
3. Employer-paid, tax-free refunds always reduce the claim.

## Other Anlagen (employee triggers)
| Anlage | Trigger | Notes |
|---|---|---|
| Vorsorgeaufwand | own KV/PV above the employer's Mindestvorsorgepauschale, Rürup, private PV, Riester | Belegabruf pre-fills KV/PV/Rürup |
| Sonderausgaben | Spenden, Mitgliedsbeiträge, Kirchensteuer gezahlt/erstattet, Berufsausbildungskosten, Ehegatten-Unterhalt | pauschal only 36 €/72 € |
| Haushaltsnahe Aufwendungen | Handwerker, Haushaltshilfe, Minijob, Pflege | 20 %; caps in parameters.md; invoice + transfer |
| Außergewöhnliche Belastungen | Krankheit, Pflege, Behinderung | only above zumutbare Belastung (computed by the Finanzamt); use Behinderten-Pauschbetrag if eligible |
| N-Doppelte Haushaltsführung | own Hausstand away from work place + second flat at work place | Unterkunft max 1 000 €/Monat; only own costs |
| Kind | child living with you | out of scope detail |
| Mobilitätsprämie | long commuter with taxable income below Grundfreibetrag | narrow |
| KAP, KAP-INV, SO, V, R | Kapitalerträge ohne Abgeltungsteuer, private Veräußerung/Krypto, Vermietung, Rente | **flag and stop**, outside this skill |
| Sonstiges | Einzelveranlagung Ehegatten, Spendenvortrag, Verlustabzug | on trigger |
