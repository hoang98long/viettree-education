"""Stable entry points for the published explorers release."""

from app.curriculum.supplements.builders import cards, pick
from app.curriculum.supplements.builders import unit as build_unit

__all__ = ["cards", "pick", "unit"]


def unit(*args, **kwargs):
    return build_unit(*args, release="explorers-2026-01", **kwargs)
