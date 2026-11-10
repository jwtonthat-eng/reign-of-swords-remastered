"""The Mirror Sea — three story battles and two raids fought ship to ship in Mare Nostra (ours; see build_bonus.py)."""
from build_bonus import U  # noqa: F401

LEVELS = []

KINGDOM = {
    "id": "mirror-sea",
    "short": "Mirror Sea",
    "name": "The Mirror Sea",
    "order": 13,
    "theme": "sand",
    "unlock_after": ["Isoluccia"],
    "heraldry": {"E": ("argent", "sable", 20, 5), "A": ("cyan", "azure", 8, 3)},
    "brief": [],
    "levels": LEVELS,
}
