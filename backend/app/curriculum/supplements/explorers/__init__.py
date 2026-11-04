"""Release-specific defaults; shared authoring behavior lives in supplements.builders."""

from functools import partial

from app.curriculum.supplements.builders import cards, pick
from app.curriculum.supplements.builders import unit as build_unit

__all__ = ["cards", "pick", "unit"]

unit = partial(build_unit, release="explorers-2026-01", sort_order=220)
