"""Short original investigations, with one Free and one VIP lesson per subject."""

from functools import partial

from app.curriculum.supplements.builders import cards, pick
from app.curriculum.supplements.builders import unit as build_unit

CODE = "discovery-2026-04"
TITLE = "Khám phá cùng bạn"
unit = partial(build_unit, release=CODE, sort_order=250)

__all__ = ["CODE", "TITLE", "cards", "pick", "unit"]
