import gzip
import io
import tarfile

import pytest

from scripts.media_archive import verify


def archive(name="ai-media/photo.webp", kind=tarfile.REGTYPE):
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode="w:gz") as output:
        entry = tarfile.TarInfo(name)
        entry.type = kind
        entry.size = 10000 if kind == tarfile.REGTYPE else 0
        output.addfile(entry, io.BytesIO(b"a" * entry.size))
    return stream.getvalue()


def test_valid_archive_verifies_without_extracting_files():
    verify(io.BytesIO(archive()))


@pytest.mark.parametrize("broken", ["truncated", "bad_crc", "payload_truncated"])
def test_reject_corruption_even_when_tar_listing_looks_valid(broken):
    payload = archive()
    if broken == "truncated":
        payload = payload[:-5]
    elif broken == "bad_crc":
        payload = payload[:-8] + b"\x00\x00\x00\x00" + payload[-4:]
    else:
        payload = gzip.compress(gzip.decompress(payload)[:2000])
    with pytest.raises((EOFError, OSError, tarfile.TarError)):
        verify(io.BytesIO(payload))


@pytest.mark.parametrize(
    "name,kind",
    [
        ("../outside", tarfile.REGTYPE),
        ("ai-media/../../outside", tarfile.REGTYPE),
        ("/ai-media/file", tarfile.REGTYPE),
        ("another-root/file", tarfile.REGTYPE),
        ("ai-media/link", tarfile.SYMTYPE),
    ],
)
def test_reject_unsafe_members(name, kind):
    with pytest.raises(ValueError, match="Unsafe"):
        verify(io.BytesIO(archive(name, kind)))
