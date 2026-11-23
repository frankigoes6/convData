#!/usr/bin/env python3
"""Vérification indépendante : recalcule un résultat sans DuckDB ni `common.py`.

On recompte à la main, en Python pur, les ouvertures de procédure collective
du département 75 en 2023, puis on compare au chiffre produit par le pipeline
(`out/agg_mois_dept.parquet`).

Usage : python src/verify.py
"""
from __future__ import annotations

import json
import sys

import duckdb

from common import RAW

DEPT, ANNEE = "75", 2023


def recompte_python_pur() -> int:
    total = 0
    for rec in json.loads(RAW.read_text(encoding="utf-8")):
        if str(rec.get("numerodepartement")) != DEPT:
            continue
        if not str(rec.get("dateparution", "")).startswith(str(ANNEE)):
            continue
        jugement = rec.get("jugement")
        if not isinstance(jugement, str):
            continue
        nature = json.loads(jugement).get("nature", "").lower()
        if "ouverture" in nature and ("liquidation" in nature or "redressement" in nature or "sauvegarde" in nature):
            total += 1
    return total


def main() -> None:
    attendu = recompte_python_pur()
    obtenu = duckdb.connect().execute(
        f"""SELECT coalesce(sum(nb), 0) FROM 'out/agg_mois_dept.parquet'
            WHERE departement = '{DEPT}' AND annee = {ANNEE}
              AND procedure IN ('liquidation', 'redressement', 'sauvegarde')"""
    ).fetchone()[0]

    print(f"Python pur (recalcul) : {attendu} ouvertures en {DEPT} / {ANNEE}")
    print(f"Pipeline DuckDB       : {obtenu}")
    if attendu != obtenu:
        print("ECART : les deux méthodes divergent")
        sys.exit(1)
    print("OK : résultats identiques")


if __name__ == "__main__":
    main()
