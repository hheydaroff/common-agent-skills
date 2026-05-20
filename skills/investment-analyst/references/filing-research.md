# Filing Research — US & European

## US — SEC EDGAR

```bash
# Get latest 10-K or 10-Q via r.jina.ai
curl -s "https://r.jina.ai/https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=<TICKER>&type=10-K&dateb=&owner=include&count=5"
```

## European Filing Sources

```bash
# UK — Regulatory News Service (RNS) via Investegate
curl -s "https://r.jina.ai/https://www.investegate.co.uk/company-search?company=<COMPANY>"

# Germany — Bundesanzeiger (official company disclosures)
curl -s "https://r.jina.ai/https://www.bundesanzeiger.de"

# France — AMF (Autorité des marchés financiers)
curl -s "https://r.jina.ai/https://www.amf-france.org/en"

# Pan-European insider dealing tracker
curl -s "https://r.jina.ai/https://disclosyr.com"

# EU public procurement (equivalent to SAM.gov)
# TED — Tenders Electronic Daily
curl -s "https://r.jina.ai/https://ted.europa.eu/en/"
```

## European Regulatory Bodies

| Country | Regulator | Insider Filings | Company Filings |
|---------|-----------|-----------------|------------------|
| UK | FCA | RNS via Investegate | Companies House |
| Germany | BaFin | BaFin Insiderregister | Bundesanzeiger |
| France | AMF | AMF déclarations | AMF BDIF |
| Netherlands | AFM | AFM register | AFM |
| Spain | CNMV | CNMV hechos relevantes | CNMV |
| Italy | CONSOB | CONSOB | Borsa Italiana |
| Sweden | FI | Finansinspektionen | FI.se |
| Switzerland | FINMA | SIX disclosure | SIX |

**Aggregator:** [Disclosyr.com](https://disclosyr.com) — consolidates insider transactions across all European regulators.
