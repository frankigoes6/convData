"""Extrait retiré de `src/common.py` : la fonction `naf_section` et sa table.

À replacer dans `src/common.py`, à l'identique ou pas, du moment que les résultats
restent les mêmes (voir les contrôles dans le README de ce dossier).
"""

# NAF rév. 2 : division (2 premiers chiffres) -> section
_SECTIONS = [
    ("A", 1, 3, "Agriculture, sylviculture et pêche"),
    ("B", 5, 9, "Industries extractives"),
    ("C", 10, 33, "Industrie manufacturière"),
    ("D", 35, 35, "Production et distribution d'électricité, de gaz"),
    ("E", 36, 39, "Eau, assainissement, déchets"),
    ("F", 41, 43, "Construction"),
    ("G", 45, 47, "Commerce, réparation d'automobiles"),
    ("H", 49, 53, "Transports et entreposage"),
    ("I", 55, 56, "Hébergement et restauration"),
    ("J", 58, 63, "Information et communication"),
    ("K", 64, 66, "Activités financières et d'assurance"),
    ("L", 68, 68, "Activités immobilières"),
    ("M", 69, 75, "Activités spécialisées, scientifiques et techniques"),
    ("N", 77, 82, "Activités de services administratifs et de soutien"),
    ("O", 84, 84, "Administration publique"),
    ("P", 85, 85, "Enseignement"),
    ("Q", 86, 88, "Santé humaine et action sociale"),
    ("R", 90, 93, "Arts, spectacles et activités récréatives"),
    ("S", 94, 96, "Autres activités de services"),
    ("T", 97, 98, "Activités des ménages en tant qu'employeurs"),
    ("U", 99, 99, "Activités extra-territoriales"),
]


def naf_section(code: str | None) -> tuple[str, str] | tuple[None, None]:
    """Code NAF ("43.21A") -> (section, libellé)."""
    if not code:
        return None, None
    digits = "".join(c for c in code[:2] if c.isdigit())
    if not digits:
        return None, None
    division = int(digits)
    for section, lo, hi, label in _SECTIONS:
        if lo <= division <= hi:
            return section, label
    return None, None
