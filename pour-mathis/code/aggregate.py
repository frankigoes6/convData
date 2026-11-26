#!/usr/bin/env python3
"""Agrégations DuckDB sur `out/clean.parquet` (+ `out/naf.parquet` si présent).

Écrit dans `out/` :
  - agg_mois_dept.parquet   ouvertures par département, année, mois, procédure
  - agg_secteur.parquet     ouvertures par section NAF et part de liquidations
  - agg_saisonnalite.parquet  indice de saisonnalité mensuel

Usage : python src/aggregate.py
"""
from __future__ import annotations

import duckdb

from common import DATA, OUT, OUVERTURES

AGG = OUT


def main() -> None:
    AGG.mkdir(exist_ok=True)
    con = duckdb.connect()
    con.execute(f"CREATE VIEW clean AS SELECT * FROM '{OUT / 'clean.parquet'}'")
    naf = OUT / "naf.parquet"
    if naf.exists():
        con.execute(f"CREATE VIEW naf AS SELECT * FROM '{naf}'")
        con.execute(
            "CREATE TABLE joined AS SELECT c.*, n.section, n.section_libelle, n.naf "
            "FROM clean c LEFT JOIN naf n USING (siren)"
        )
    else:
        con.execute(
            "CREATE TABLE joined AS SELECT *, NULL::VARCHAR AS section, "
            "NULL::VARCHAR AS section_libelle, NULL::VARCHAR AS naf FROM clean"
        )
    con.execute("CREATE VIEW ouv AS SELECT * FROM joined WHERE est_ouverture")

    con.execute(
        f"""COPY (
            SELECT departement, any_value(departement_nom) AS departement_nom,
                   annee, mois, procedure, count(*) AS nb
            FROM ouv GROUP BY departement, annee, mois, procedure ORDER BY ALL
        ) TO '{AGG / 'agg_mois_dept.parquet'}' (FORMAT PARQUET)"""
    )
    con.execute(
        f"""COPY (
            SELECT section, any_value(section_libelle) AS section_libelle, procedure,
                   count(*) AS nb,
                   round(100.0 * count(*) FILTER (
                       WHERE procedure IN ('liquidation', 'conversion_liquidation')
                   ) / count(*), 1) AS part_liquidation_pct
            FROM ouv WHERE section IS NOT NULL
            GROUP BY section, procedure ORDER BY nb DESC
        ) TO '{AGG / 'agg_secteur.parquet'}' (FORMAT PARQUET)"""
    )
    con.execute(
        f"""COPY (
            WITH m AS (SELECT mois, count(*) AS nb FROM ouv GROUP BY mois)
            SELECT mois, nb, round(nb / (SELECT avg(nb) FROM m), 3) AS indice
            FROM m ORDER BY mois
        ) TO '{AGG / 'agg_saisonnalite.parquet'}' (FORMAT PARQUET)"""
    )

    print(f"Ouvertures analysées : {con.execute('SELECT count(*) FROM ouv').fetchone()[0]}")
    print("\nTop départements (ouvertures) :")
    for row in con.execute(
        "SELECT departement, any_value(departement_nom), count(*) nb FROM ouv "
        "GROUP BY 1 ORDER BY nb DESC"
    ).fetchall():
        print(f"  {row[0]} {row[1]:<12} {row[2]:>4}")
    print("\nTop sections NAF (ouvertures) :")
    for row in con.execute(
        "SELECT section, any_value(section_libelle), count(*) nb FROM ouv "
        "WHERE section IS NOT NULL GROUP BY 1 ORDER BY nb DESC LIMIT 8"
    ).fetchall():
        print(f"  {row[0]} {row[1][:44]:<44} {row[2]:>4}")
    print("\nIndice de saisonnalité (1.0 = mois moyen) :")
    for mois, nb, indice in con.execute("SELECT * FROM 'out/agg_saisonnalite.parquet'").fetchall():
        print(f"  {mois:>2} {nb:>4} {indice:>6}")
    print(f"\n-> {AGG}")


if __name__ == "__main__":
    main()
