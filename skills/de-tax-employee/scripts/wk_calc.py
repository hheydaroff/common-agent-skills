#!/usr/bin/env python3
"""Werbungskosten vs Arbeitnehmer-Pauschbetrag (German employee). Estimate only.

Rates per sources in references/parameters.md. Change them there AND here.
"""
import argparse

RATES = {  # year -> (first20 per km, from km 21 per km)
    2025: (0.30, 0.38),
    2026: (0.38, 0.38),
}
PAUSCH = {2025: 1230.0}
HO_RATE, HO_MAX_DAYS, CAP, KONTO = 6.0, 210, 4500.0, 16.0


def main():
    a = argparse.ArgumentParser(description=__doc__)
    a.add_argument("--year", type=int, required=True)
    a.add_argument("--km", type=float, default=0, help="one-way km to first Tätigkeitsstätte (whole km used)")
    a.add_argument("--office-days", type=int, default=0, help="days actually at the site")
    a.add_argument("--home-days", type=int, default=0, help="Homeoffice days (no office visit)")
    a.add_argument("--car", action="store_true", help="own/provided car: 4500 cap does not apply")
    a.add_argument("--oepnv-cost", type=float, default=0, help="actual public transport cost for the commute")
    a.add_argument("--jobticket-subsidy", type=float, default=0, help="tax-free employer subsidy, reduces commute claim")
    a.add_argument("--other", type=float, default=0, help="Arbeitsmittel, Fortbildung, dues, Bewerbung… (net, after refunds)")
    a.add_argument("--no-konto", action="store_true", help="skip 16 EUR Kontoführung flat")
    a.add_argument("--pauschbetrag", type=float, help="override Pauschbetrag")
    a = a.parse_args()

    if a.year not in RATES:
        raise SystemExit(f"Year {a.year} not verified. Known: {sorted(RATES)}. Check references/sources.md, add the year.")
    pb = a.pauschbetrag if a.pauschbetrag is not None else PAUSCH.get(a.year)
    if pb is None:
        raise SystemExit(f"Pauschbetrag for {a.year} not verified; pass --pauschbetrag.")

    km = int(a.km)
    lo, hi = RATES[a.year]
    per_day = min(km, 20) * lo + max(km - 20, 0) * hi
    flat = per_day * a.office_days
    if not a.car:
        flat = min(flat, CAP)
    commute = max(flat, a.oepnv_cost)  # actual ticket cost beats flat if higher, cap-free
    commute = max(commute - a.jobticket_subsidy, 0)
    ho_days = min(a.home_days, HO_MAX_DAYS)
    ho = ho_days * HO_RATE
    konto = 0 if a.no_konto else KONTO
    total = commute + ho + a.other + konto

    print(f"Tax year {a.year}")
    print(f"  Entfernungspauschale: {km} km x {a.office_days} d -> flat {flat:,.2f}; ÖPNV actual {a.oepnv_cost:,.2f}; subsidy -{a.jobticket_subsidy:,.2f} => {commute:,.2f}")
    print(f"  Homeoffice: {ho_days} d x {HO_RATE:.0f} = {ho:,.2f}" + ("  (capped at 210 d)" if a.home_days > HO_MAX_DAYS else ""))
    print(f"  Other: {a.other:,.2f}   Kontoführung: {konto:,.2f}")
    print(f"  TOTAL Werbungskosten: {total:,.2f}  vs Pauschbetrag {pb:,.2f}")
    extra = total - pb
    if extra > 0:
        print(f"  => {extra:,.2f} above the Pauschbetrag: enter all costs; only this amount reduces taxable income.")
    else:
        print(f"  => {-extra:,.2f} below: Pauschbetrag already applies; entering costs changes nothing by itself.")
    print("  Estimate only. Day counts are your input; Homeoffice and office days must not overlap.")


if __name__ == "__main__":
    main()
