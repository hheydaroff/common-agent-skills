# Anhänge (Annexes) der KI-VO — Referenz

Übersicht über alle **13 Anhänge** der EU-KI-Verordnung (2024/1689). Die Anhänge sind Teil des Verordnungstexts — sie sind **keine unverbindlichen Anlagen**, sondern normativ. Für die Rolle als KI-Beauftragter/AI Officer sind **Anhang I, II und III** (Risikoklassifizierung) sowie **XI–XIII** (GPAI) die wichtigsten.

## Gesamtübersicht

| Anhang | Inhalt | Bezug / Artikel |
|--------|--------|-----------------|
| **I** | Liste der EU-Harmonisierungsrechtsvorschriften (Produktgesetze) | Art. 6 Abs. 1 |
| **II** | Liste der Straftaten (für Ausnahme biometrische Fernidentifizierung) | Art. 5 Abs. 1 lit. h Ziff. iii |
| **III** | Hochrisiko-KI-Systeme (die 8 Anwendungsbereiche) | Art. 6 Abs. 2 |
| **IV** | Technische Dokumentation (Hochrisiko) | Art. 11 Abs. 1 |
| **V** | EU-Konformitätserklärung (Inhalt + Muster) | Art. 47 |
| **VI** | Konformitätsbewertung auf Grundlage interner Kontrolle | Art. 43 |
| **VII** | Konformitätsbewertung durch notifizierte Stelle (QM + technische Doku) | Art. 43 |
| **VIII** | Registrierungsinformationen Hochrisiko-KI-Systeme | Art. 49 |
| **IX** | Registrierungsinformationen für Tests unter realen Bedingungen (Anhang III) | Art. 60 |
| **X** | Rechtsakte über IT-Großsysteme (Raum der Freiheit, Sicherheit, Recht — FSJ) | Art. 83 |
| **XI** | Technische Dokumentation für GPAI-Anbieter | Art. 53 Abs. 1 lit. a |
| **XII** | Transparenzinformationen GPAI → nachgeschaltete Anbieter | Art. 53 Abs. 1 lit. b |
| **XIII** | Kriterien für GPAI mit systemischem Risiko | Art. 51 |

## Die prüfungsrelevanten Anhänge im Detail

### Anhang I — Liste der Harmonisierungsrechtsvorschriften

> [!important] Anhang I ist **KEINE Liste von KI-Systemen.**
> Er zählt **Produkt-Sicherheitsgesetze** der EU auf. Ein KI-System wird über Anhang I nur dann hochriskant (Art. 6 Abs. 1), wenn es **Sicherheitskomponente** eines unter diese Gesetze fallenden Produkts ist (oder selbst ein solches Produkt ist) **und** eine **Konformitätsbewertung durch Dritte** braucht.

Typische Anhang-I-Produkte (keine KI-Systeme!):
- **Medizinprodukte** (MDR 2017/745)
- **Fahrzeuge** (KFZ-Typgenehmigung)
- **Maschinen** (Maschinenverordnung)
- Aufzüge, Spielzeug, persönliche Schutzausrüstung, Funkgeräte u.a.

> **KI-Omnibus-Änderung:** Maschinen wandern von Anhang I **Abschnitt A → Abschnitt B** und unterliegen der KI-VO nur noch marginal.
> **Zeitpunkt:** Anhang I startet **02.08.2028** (Anhang III schon 02.12.2027).

### Anhang II — Liste der Straftaten

Aufzählung schwerer Straftaten (z.B. Terrorismus, Menschenhandel, sexuelle Ausbeutung), die als Anknüpfung für die **Ausnahmen** bei der **biometrischen Fernidentifizierung** dienen (Art. 5 Abs. 1 lit. h Ziff. iii = gezielte Suche nach Verdächtigen schwerer Straftaten). Für den KI-Beauftragten relevant, weil es die **enge Ausnahme** vom Verbot der Echtzeit-Fernbiometrie definiert.

### Anhang III — die 8 Hochrisiko-Bereiche

Die eigentliche Liste riskanter **KI-Anwendungsbereiche** (Art. 6 Abs. 2). Diese 8 Bereiche muss ein KI-Beauftragter auswendig kennen:

| Nr. | Bereich | Typische Beispiele |
|-----|---------|--------------------|
| 1 | **Biometrie** (Fernidentifizierung, Kategorisierung, Emotionserkennung) | Zutrittskontrolle per Gesicht |
| 2 | **Kritische Infrastruktur** (Verkehr, Wasser/Gas/Strom) | KI-Steuerung Stromnetz |
| 3 | **Allgemeine & berufliche Bildung** | Automatisierte Prüfungs-/Lernbewertung |
| 4 | **Beschäftigung & Personalmanagement** | Recruiting-KI, Bewerbungsfilter, Leistungsüberwachung |
| 5 | **Wesentliche Dienstleistungen** (Zugang + Inanspruchnahme) | Kreditwürdigkeit, Kranken-/Lebensversicherung (Risikobewertung & Preisbildung) |
| 6 | **Strafverfolgung** | Rückfallrisiko, Beweis-/Zeugenbewertung |
| 7 | **Migration, Asyl & Grenzkontrolle** | Dokumentenprüfung, Risikoabschätzung |
| 8 | **Rechtspflege & demokratische Prozesse** | KI bei Gerichtsurteilen, Wahlbeeinflussung |

> **Rückausnahme Profiling:** Die Ausnahme „kein wesentliches Risiko für Gesundheit/Sicherheit/Grundrechte" gilt **nicht**, wenn die Person **profiliert** wird.
> **Zeitpunkt:** Anhang III startet **02.12.2027** (per KI-Omnibus von 02.08.2026 verschoben).

## Die Verfahrens-/Dokumentations-Anhänge (IV–X)

Diese sind primär für **Anbieter** (und notifizierte Stellen) relevant — ein KI-Beauftragter prüft, ob sie existieren/vollständig sind, erstellt sie aber meist nicht selbst:

- **Anhang IV** — Mindestinhalt der **technischen Dokumentation** (Art. 11). Der Anbieter muss nachweisen, wie das System die Hochrisiko-Anforderungen (Art. 9–15) erfüllt.
- **Anhang V** — **EU-Konformitätserklärung** (Art. 47): Bestätigung der Konformität; 10 Jahre aufbewahren.
- **Anhang VI** — **Konformitätsbewertung** per **interner Kontrolle** (Selbstbewertung durch den Anbieter; Regelfall für Anhang-III-Bereiche 2–8).
- **Anhang VII** — Konformitätsbewertung **unter Einbeziehung einer notifizierten Stelle** (Bewertung QM-System + technische Doku; Pflicht bei Anhang-III-Bereich 1 / biometrische Fernidentifizierung u.ä.).
- **Anhang VIII** — Angaben für die **Registrierung** in der EU-Datenbank (Art. 49).
- **Anhang IX** — Angaben für die Registrierung bei **Tests unter realen Bedingungen** (Art. 60).
- **Anhang X** — EU-Rechtsakte über **IT-Großsysteme** im Raum der Freiheit, der Sicherheit und des Rechts (z.B. Schengen-, Visa-, Eurodac-Systeme).

## Die GPAI-Anhänge (XI–XIII)

- **Anhang XI** — Mindestinhalt der **technischen Dokumentation** für **GPAI-Anbieter** (Art. 53 Abs. 1 lit. a): Modellbeschreibung, Architektur/Parameter, Trainingsdaten (Art, Herkunft, Aufbereitung), Rechenressourcen, Energieverbrauch.
- **Anhang XII** — **Transparenzinformationen**, die GPAI-Anbieter an **nachgeschaltete Anbieter** weitergeben müssen, die das Modell in ihr KI-System integrieren (Art. 53 Abs. 1 lit. b).
- **Anhang XIII** — **Kriterien für die Einstufung** eines GPAI als **systemisches Risiko** (Art. 51) — ergänzt die automatische Schwelle von **10²⁵ FLOP**.

## Merksatz

> 📌 **Anhang I = Produktgesetze** (KI *in* einem Produkt) · **Anhang II = Straftaten** (biometrische Ausnahme) · **Anhang III = die 8 Bereiche** (der Einsatz ist riskant) · **IV–X = Dokumentation + Konformität + Registrierung** (Anbieter-Ballast) · **XI–XIII = GPAI** (technische Doku + Transparenz + Systemrisiko-Kriterien).