import base64
import hashlib
from io import BytesIO
from uuid import uuid4

from fastapi import HTTPException
from PIL import Image, UnidentifiedImageError, features

from app.academy.learning import audit
from app.core.config import settings
from app.db import db

Image.MAX_IMAGE_PIXELS = 8_000_000
UPLOAD_SCANNER = None  # Hook local antivirus: Callable[[bytes], bool], never a cloud upload.


def upload(conn, user, payload):
    try:
        raw = base64.b64decode(payload["data"], validate=True)
        if len(raw) > 512000:
            raise ValueError("size")
        if UPLOAD_SCANNER is not None and not UPLOAD_SCANNER(raw):
            raise ValueError("scan")
        image = Image.open(BytesIO(raw))
        if (
            image.format not in {"PNG", "JPEG", "WEBP", "AVIF"}
            or image.width * image.height > 8_000_000
        ):
            raise ValueError("type")
        image.load()
        # Fresh pixels remove EXIF/location and ancillary input metadata.
        clean = Image.new("RGB", image.size, "white")
        if image.mode == "RGBA":
            clean.paste(image, mask=image.getchannel("A"))
        else:
            clean.paste(image.convert("RGB"))
    except (
        ValueError,
        KeyError,
        UnidentifiedImageError,
        OSError,
        Image.DecompressionBombError,
        Image.DecompressionBombWarning,
    ):
        raise HTTPException(
            422, "Chỉ nhận ảnh raster hợp lệ dưới 512 KB, tối đa 8 triệu pixel"
        ) from None
    identifier = uuid4()
    root = settings().ai_media_root
    root.mkdir(parents=True, exist_ok=True)
    variants = []
    for kind, size in [("original", 1280), ("responsive", 768), ("thumbnail", 256)]:
        output = clean.copy()
        output.thumbnail((size, size))
        buffer = BytesIO()
        encoding = "WEBP" if features.check("webp") else "PNG"
        output.save(buffer, format=encoding, quality=85)
        data = buffer.getvalue()
        key = str(identifier) + "-" + kind + (".webp" if encoding == "WEBP" else ".png")
        (root / key).write_bytes(data)
        variants.append(
            dict(
                asset_id=identifier,
                kind=kind,
                object_key=key,
                mime_type="image/webp" if encoding == "WEBP" else "image/png",
                sha256=hashlib.sha256(data).hexdigest(),
                width=output.width,
                height=output.height,
                file_size_bytes=len(data),
            )
        )
    original = variants[0]
    conn.execute(
        db.table("media_assets")
        .insert()
        .values(
            id=identifier,
            bucket_name="ai-academy-local",
            object_key=original["object_key"],
            mime_type=original["mime_type"],
            file_size_bytes=original["file_size_bytes"],
            sha256=original["sha256"],
            uploaded_by=user["id"],
            visibility="private",
        )
    )
    conn.execute(
        db.table("ai_media_assets")
        .insert()
        .values(
            id=identifier,
            code="upload-" + str(identifier),
            category="upload",
            alt=payload["alt"],
            license=payload["license"],
            source=payload["source"],
            status="review",
            width=original["width"],
            height=original["height"],
            bundled=False,
        )
    )
    conn.execute(db.table("ai_media_variants").insert(), variants)
    audit(conn, user["id"], "academy.media_uploaded", identifier)
    return {"id": identifier, "code": "upload-" + str(identifier), "status": "review"}
