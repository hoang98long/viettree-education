"""Explicit release selection; adding packs does not change published baseline versions."""

from functools import lru_cache


@lru_cache(maxsize=1)
def releases():
    from app.curriculum.supplements.applied.pack import PACK as applied
    from app.curriculum.supplements.explorers.pack import PACK as explorers
    from app.curriculum.supplements.review.pack import PACK as review

    return {pack.code: pack for pack in (applied, explorers, review)}


def get_release(code):
    try:
        return releases()[code]
    except KeyError:
        raise ValueError("Chọn mã học liệu bổ sung hợp lệ") from None
