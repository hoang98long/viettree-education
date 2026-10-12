from fastapi import HTTPException
from sqlalchemy import select, text, update
from sqlalchemy.dialects.postgresql import insert

from app.classroom.service import audit
from app.core.security import now
from app.db import db
from app.services.accounts import authenticate_actor


def catalog(conn):
    options, promotions, references = (
        db.table(n) for n in ("vip_price_options", "vip_promotions", "vip_market_references")
    )
    at = now()
    live = list(
        conn.execute(
            select(promotions)
            .where(
                promotions.c.is_active.is_(True),
                promotions.c.starts_at <= at,
                promotions.c.ends_at > at,
            )
            .order_by(promotions.c.sale_price_vnd, promotions.c.code)
        ).mappings()
    )
    result = []
    for price in conn.execute(
        select(options).where(options.c.is_active.is_(True)).order_by(options.c.duration_days)
    ).mappings():
        sale = next(
            (
                r
                for r in live
                if r["price_code"] == price["code"]
                and r["sale_price_vnd"] < price["reference_price_vnd"]
            ),
            None,
        )
        effective = sale["sale_price_vnd"] if sale else price["reference_price_vnd"]
        result.append(
            {
                **{
                    k: v
                    for k, v in dict(price).items()
                    if k not in {"updated_by", "updated_at", "revision", "is_active"}
                },
                "effective_price_vnd": effective,
                "saving_vnd": price["reference_price_vnd"] - effective,
                "discount_percent": round(
                    (price["reference_price_vnd"] - effective) * 100 / price["reference_price_vnd"],
                    1,
                ),
                "promotion": {
                    k: v
                    for k, v in dict(sale).items()
                    if k not in {"updated_by", "revision", "is_active"}
                }
                if sale
                else None,
            }
        )
    return {
        "currency": "VND",
        "reference_only": True,
        "checked_at": at,
        "offers": result,
        "market_references": [
            dict(r)
            for r in conn.execute(
                select(references).order_by(references.c.provider, references.c.code)
            ).mappings()
        ],
        "notice": "Giá đề xuất để tham khảo với phụ huynh. Chưa có thanh toán trực tuyến; quản trị xác nhận và cấp/gia hạn riêng. Không tự gia hạn, không cộng dồn ưu đãi.",
    }


def save_price(conn, user, code, payload):
    authenticate_actor(conn, user, payload.actor_password)
    table = db.table("vip_price_options")
    row = (
        conn.execute(select(table).where(table.c.code == code).with_for_update()).mappings().first()
    )
    if not row:
        raise HTTPException(404, "Không có gói giá")
    if row["revision"] != payload.revision:
        raise HTTPException(409, "Giá đã được sửa, tải lại trước khi lưu")
    conn.execute(
        update(table)
        .where(table.c.code == code)
        .values(
            label=payload.label,
            reference_price_vnd=payload.reference_price_vnd,
            is_active=payload.is_active,
            revision=row["revision"] + 1,
            updated_by=user["id"],
            updated_at=now(),
        )
    )
    audit(
        conn,
        user,
        "vip.price_updated",
        details={"code": code, "price": payload.reference_price_vnd, "reason": payload.reason},
    )
    return {"revision": row["revision"] + 1}


def save_promotion(conn, user, payload):
    authenticate_actor(conn, user, payload.actor_password)
    conn.execute(
        text("SELECT pg_advisory_xact_lock(hashtextextended(:key,0))"),
        {"key": "vip-promotion:" + payload.code},
    )
    options, table = db.table("vip_price_options"), db.table("vip_promotions")
    price = (
        conn.execute(select(options).where(options.c.code == payload.price_code).with_for_update())
        .mappings()
        .first()
    )
    if not price or payload.sale_price_vnd >= price["reference_price_vnd"]:
        raise HTTPException(422, "Giá ưu đãi phải nhỏ hơn giá tham khảo của gói")
    old = (
        conn.execute(select(table).where(table.c.code == payload.code).with_for_update())
        .mappings()
        .first()
    )
    if old and payload.revision != old["revision"]:
        raise HTTPException(409, "Ưu đãi đã thay đổi, tải lại trước khi lưu")
    if not old and payload.revision:
        raise HTTPException(404, "Không tìm thấy ưu đãi cần sửa")
    values = {
        **payload.model_dump(exclude={"actor_password", "reason", "revision"}),
        "updated_by": user["id"],
        "revision": old["revision"] + 1 if old else 1,
    }
    conn.execute(
        insert(table)
        .values(**values)
        .on_conflict_do_update(
            index_elements=[table.c.code], set_={k: v for k, v in values.items() if k != "code"}
        )
    )
    audit(
        conn,
        user,
        "vip.promotion_saved",
        details={
            "code": payload.code,
            "sale_price": payload.sale_price_vnd,
            "reason": payload.reason,
        },
    )
    return {"revision": values["revision"]}
