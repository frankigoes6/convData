#!/usr/bin/env python3
"""Métriques de qualité sur les données brutes (aucune correction).

Écrit `data/quality_report.json` et affiche un tableau lisible.
Usage : python src/quality.py
"""
from __future__ import annotations

import json
import re
from collections import Counter

from common import DATA, OUVERTURES, jugement, load_raw, parse_json_field, personne, procedure_type, siren

DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
NESTED = (
    "listepersonnes", "listeetablissements", "jugement", "acte", "divers",
    "depot", "radiationaurcs", "modificationsgenerales", "parutionavisprecedent",
    "listeprecedentexploitant", "listeprecedentproprietaire",
)


def main() -> None:
    rows = load_raw()
    n = len(rows)

    nested_invalid = sum(
        1 for r in rows for f in NESTED if isinstance(r.get(f), str) and parse_json_field(r[f]) is None
    )
    dates_bad = sum(1 for r in rows if not DATE.match(str(r.get("dateparution", ""))))
    siren_absent = sum(1 for r in rows if siren(r) is None)
    naf_present = sum(1 for r in rows if "naf" in json.dumps(r, ensure_ascii=False).lower())
    nature = Counter(procedure_type(jugement(r).get("nature")) for r in rows)
    # Doublons métier : même entreprise (SIREN), même jour, même type de procédure
    keys = Counter(
        (siren(r), r.get("dateparution"), procedure_type(jugement(r).get("nature"))) for r in rows
    )
    doublons = sum(c - 1 for c in keys.values() if c > 1)

    report = {
        "lignes": n,
        "colonnes": len(rows[0]),
        "identifiants_uniques": len({r.get("id") for r in rows}),
        "champs_imbriques_en_texte": sum(
            1 for f in NESTED if isinstance(rows[0].get(f), (str, type(None)))
        ),
        "champs_imbriques_json_invalides": nested_invalid,
        "dates_parution_invalides": dates_bad,
        "siren_absent_ou_mal_forme": siren_absent,
        "codes_naf_presents": naf_present,
        "doublons_metier": doublons,
        "familles": Counter(r.get("familleavis") for r in rows),
        "types_procedure": nature,
    }
    report = {k: (dict(v) if isinstance(v, Counter) else v) for k, v in report.items()}

    (DATA / "quality_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"Lignes                : {n}")
    print(f"Colonnes              : {report['colonnes']}")
    print(f"IDs uniques           : {report['identifiants_uniques']}")
    print(f"JSON imbriqué invalide: {nested_invalid}")
    print(f"Dates invalides       : {dates_bad}")
    print(f"SIREN manquant/malformé: {siren_absent}")
    print(f"Codes NAF présents    : {naf_present}")
    print(f"Doublons métier       : {doublons}")
    print(f"Familles              : {report['familles']}")
    print("\nTypes de procédure (après normalisation) :")
    for k, v in nature.most_common():
        flag = "  <- ouverture" if k in OUVERTURES else ""
        print(f"  {k:<24} {v:>5}{flag}")
    print(f"\n-> data/quality_report.json")


if __name__ == "__main__":
    main()
