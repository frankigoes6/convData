#!/usr/bin/env python3
"""
Télécharge les annonces BODACC (data.gouv.fr / DILA) filtrées sur :
  - date de parution : 2022-01-01 -> 2025-12-31
  - publicationavis  : A (avis initial)
  - familleavis      : collective, vente, conciliation
  - région           : Île-de-France (region_code = 11)

L'ensemble complet représente ~171 755 annonces (~360 Mo de JSON).
Le script en extrait un échantillon systématique régulier (même pas sur
toute la période, ordre chronologique) dont la taille est calibrée pour
tenir dans la fourchette 3,0 - 4,5 Mo (cible ~4,2 Mo).

Sortie : data/bodacc_idf_2022_2025.json (+ manifeste .json)
Usage  : python3 src/fetch_bodacc.py
"""
import datetime
import gzip
import hashlib
import json
import os
import sys
import time
import urllib.parse
import urllib.request

BASE = ("https://bodacc-datadila.opendatasoft.com/api/explore/v2.1/"
        "catalog/datasets/annonces-commerciales/exports/json")

WHERE_BASE = (
    "dateparution>='2022-01-01' AND dateparution<'2026-01-01' "
    "AND publicationavis='A' "
    "AND familleavis IN ('collective','vente','conciliation') "
    "AND region_code=11"
)

UA = "convData-bodacc-fetch/1.0 (projet etudiant)"
KEEP_EVERY = 20          # on conserve 1 enregistrement sur 20 pendant le download
TARGET_BYTES = 4_200_000  # cible ~4,2 Mo
MIN_BYTES = 3_000_000
MAX_BYTES = 4_500_000

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "data")
OUT_JSON = os.path.join(OUT_DIR, "bodacc_idf_2022_2025.json")
OUT_MANIFEST = os.path.join(OUT_DIR, "bodacc_idf_2022_2025.manifest.json")


def fetch(where, limit=10000, offset=0, retries=4):
    """GET l'export JSON Opendatasoft, avec réessais."""
    query = urllib.parse.urlencode({
        "where": where,
        "order_by": "dateparution asc,id asc",
        "limit": limit,
        "offset": offset,
    })
    req = urllib.request.Request(
        BASE + "?" + query,
        headers={"Accept-Encoding": "gzip", "User-Agent": UA},
    )
    last = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                raw = resp.read()
                if resp.headers.get("Content-Encoding") == "gzip":
                    raw = gzip.decompress(raw)
                return json.loads(raw)
        except Exception as exc:  # noqa: BLE001 - on relance après backoff
            last = exc
            if attempt < retries - 1:
                time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"Échec après {retries} tentatives: {last}")


def month_ranges():
    for year in range(2022, 2026):
        for month in range(1, 13):
            start = f"{year}-{month:02d}-01"
            if month == 12:
                end = f"{year + 1}-01-01"
            else:
                end = f"{year}-{month + 1:02d}-01"
            yield year, month, start, end


def fetch_month(start, end):
    """Récupère un mois entier, en découpant par jour si > 10 000 lignes."""
    where = f"{WHERE_BASE} AND dateparution>='{start}' AND dateparution<'{end}'"
    batch = fetch(where)
    if len(batch) < 10000:
        return batch
    # Cas rare : découpage jour par jour
    out = []
    day = datetime.date.fromisoformat(start)
    last = datetime.date.fromisoformat(end)
    while day < last:
        w = f"{WHERE_BASE} AND dateparution='{day.isoformat()}'"
        out.extend(fetch(w))
        day += datetime.timedelta(days=1)
    return out


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    kept = []
    seen = 0
    total_api = 0
    t0 = time.time()

    for year, month, start, end in month_ranges():
        batch = fetch_month(start, end)
        total_api += len(batch)
        for rec in batch:
            if seen % KEEP_EVERY == 0:
                kept.append(rec)
            seen += 1
        print(f"{year}-{month:02d}: {len(batch):5d} annonces "
              f"(cumul {total_api}, conservées {len(kept)})", flush=True)

    print(f"\nTéléchargé {total_api} annonces en {time.time() - t0:.0f}s, "
          f"{len(kept)} candidates conservées.")

    if not kept:
        sys.exit("Aucun enregistrement récupéré.")

    def dump(records):
        return json.dumps(records, ensure_ascii=False).encode("utf-8")

    # Sélection régulière de N enregistrements parmi les candidates
    n = len(kept)

    def pick(count):
        if count <= 0:
            return []
        if count == 1:
            return [kept[0]]
        step = (n - 1) / (count - 1)
        return [kept[round(i * step)] for i in range(count)]

    lo, hi, best = 1, n, None
    while lo <= hi:
        mid = (lo + hi) // 2
        size = len(dump(pick(mid)))
        if size <= MAX_BYTES:
            best = (mid, size)
            lo = mid + 1
        else:
            hi = mid - 1

    count, size = best
    selected = pick(count)
    payload = dump(selected)
    size = len(payload)

    if size < MIN_BYTES:
        print(f"Attention : taille {size/1e6:.2f} Mo < minimum {MIN_BYTES/1e6} Mo")

    with open(OUT_JSON, "wb") as fh:
        fh.write(payload)

    manifest = {
        "fichier": os.path.basename(OUT_JSON),
        "taille_octets": size,
        "taille_mo": round(size / 1e6, 2),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "nombre_annonces": count,
        "source": "BODACC - Annonces commerciales (DILA, data.gouv.fr)",
        "api": BASE,
        "licence": "Licence Ouverte / Open Licence Etalab 2.0",
        "filtres": {
            "periode": "2022-01-01 -> 2025-12-31",
            "publicationavis": "A",
            "familleavis": ["collective", "vente", "conciliation"],
            "region_code": 11,
            "region": "Île-de-France",
        },
        "univers_disponible": total_api,
        "methode_echantillonnage": (
            f"1 enregistrement conservé sur {KEEP_EVERY} dans l'ordre "
            "(dateparution, id), puis sélection régulière de "
            f"{count} enregistrements répartis uniformément sur la période."
        ),
        "script": "src/fetch_bodacc.py",
        "genere_le": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }
    with open(OUT_MANIFEST, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=2)

    print(f"\nOK -> {OUT_JSON}")
    print(f"   {count} annonces, {size/1e6:.2f} Mo")
    print(f"   manifeste -> {OUT_MANIFEST}")


if __name__ == "__main__":
    main()
