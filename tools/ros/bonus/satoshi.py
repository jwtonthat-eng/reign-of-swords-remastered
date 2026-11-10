"""Satoshi — three story battles and two raids in the island realm of the far north-east (ours; see build_bonus.py)."""
from build_bonus import U  # noqa: F401

LEVELS = []

KINGDOM = {
    "id": "satoshi",
    "short": "Satoshi",
    "name": "The Isles of Satoshi",
    "order": 14,
    "theme": "green",
    "unlock_after": ["The Mirror Sea"],
    "heraldry": {"E": ("gules", "sable", 33, 5), "A": ("argent", "gules", 14, 3)},
    "brief": [],
    "levels": LEVELS,
}
