# Serious-Incident Report (Art. 73 KI-VO) — Template

> Use for reporting **serious incidents** of high-risk AI systems to the market-surveillance authority. Deadlines: **15 days** if a link to the incident is probable; **otherwise immediately / ≤ 2 days**. If personal data is also affected, the **GDPR Art. 33 (72h)** notification to the DPA runs in parallel — file both.

---

## 1. Meldender (Reporter)

| Field | Value |
|-------|-------|
| Organisation | `[name]` |
| Rolle | Anbieter / Betreiber / Bevollmächtigter |
| Ansprechpartner | `[name, contact]` |
| Datum der Kenntnis | `[YYYY-MM-DD]` |

## 2. Betroffenes KI-System

| Field | Value |
|-------|-------|
| System / Marke | `[name]` |
| Risikoklasse | Hochrisiko — Anhang I / III Nr. `[x]` |
| EU-DB-Registrierung | `[ID falls vorhanden]` |
| Anbieter | `[name]` (falls meldender ≠ Anbieter) |
| Zweckbestimmung | `[short]` |

## 3. Vorfall (Incident)

- **Datum/Uhrzeit:** `[when]`
- **Ort:** `[Member State / location]`
- **Beschreibung:** `[what happened — sequence, affected persons]`
- **Schweregrad:** `[health / safety / fundamental-rights impact]`
- **Wahrscheinlichkeit des Zusammenhangs:** hoch / unklar

## 4. Auswirkungen

- [ ] Schaden / Verletzung von Personen?
- [ ] Diskriminierung / Grundrechtsverletzung?
- [ ] Personenbezogene Daten betroffen? (→ paralleler Art. 33-DSGVO-Bericht)

## 5. Ursache & Maßnahmen

- **Ursache:** `[root cause / hypothesis]`
- **Ergriffene Korrekturmaßnahmen** (Art. 20): `[fix, deactivation, recall]`
- **Benachrichtigte Stellen:** `[provider, distributor, DPO, authority]`

## 6. Fristenprüfung

| Szenario | Frist |
|----------|-------|
| Zusammenhang wahrscheinlich | ≤ 15 Tage |
| Sonst | unverzüglich / ≤ 2 Tage |
| Personenbezogene Daten betroffen | ≤ 72 h (Art. 33 DSGVO, gem. Art. 73 Abs. 3) |

## 7. Abschluss

**Meldung erstellt von:** `[name]` · **Datum:** `[YYYY-MM-DD]` · **Referenz:** `[no.]`

---

### DSFA-Ergänzung (bei Art. 26 Abs. 9 / Art. 35 DSGVO)

Wenn der Vorfall zeigt, dass die bestehende **Datenschutz-Folgenabschätzung** lückenhaft war: DSFA aktualisieren und das Update dokumentieren.