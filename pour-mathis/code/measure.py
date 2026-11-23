#!/usr/bin/env python3
"""Mesures pour le rapport : CSV vs Parquet, DuckDB vs pandas.

Usage : python src/measure.py
"""
from __future__ import annotations

import time

import duckdb
import pandas as pd

from common import OUT

SRC = OUT / "clean.parquet"


def chrono(fn) -> tuple[float, object]:
    t0 = time.perf_counter()
    out = fn()
    return time.perf_counter() - t0, out


def main() -> None:
    con = duckdb.connect()

    csv_path = OUT / "clean.csv"
    t_csv, _ = chrono(lambda: con.execute(f"COPY (SELECT * FROM '{SRC}') TO '{csv_path}' (HEADER)"))
    t_pq, _ = chrono(
        lambda: con.execute(f"COPY (SELECT * FROM '{SRC}') TO '{OUT / 'clean_copy.parquet'}' (FORMAT PARQUET)")
    )

    def read_csv():
        return con.execute(f"SELECT count(*) FROM read_csv_auto('{csv_path}')").fetchone()[0]

    def read_parquet():
        return con.execute(f"SELECT count(*) FROM '{SRC}'").fetchone()[0]

    t_read_csv, _ = chrono(read_csv)
    t_read_pq, _ = chrono(read_parquet)

    taille_csv = csv_path.stat().st_size
    taille_pq = SRC.stat().st_size

    df = pd.read_parquet(SRC)
    t_pandas, _ = chrono(
        lambda: df[df["est_ouverture"]].groupby(["departement", "annee"]).size()
    )
    t_duckdb, _ = chrono(
        lambda: con.execute(
            f"SELECT departement, annee, count(*) FROM '{SRC}' "
            "WHERE est_ouverture GROUP BY 1, 2"
        ).fetchall()
    )

    print(f"CSV     : {taille_csv / 1e6:6.2f} Mo, écriture {t_csv * 1000:7.1f} ms, lecture {t_read_csv * 1000:7.1f} ms")
    print(f"Parquet : {taille_pq / 1e6:6.2f} Mo, écriture {t_pq * 1000:7.1f} ms, lecture {t_read_pq * 1000:7.1f} ms")
    print(f"Ratio taille CSV/Parquet : {taille_csv / taille_pq:.1f}x")
    print(f"Agrégation pandas : {t_pandas * 1000:7.1f} ms")
    print(f"Agrégation DuckDB : {t_duckdb * 1000:7.1f} ms")


if __name__ == "__main__":
    main()
