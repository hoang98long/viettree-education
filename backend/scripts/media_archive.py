"""Streaming private-media backup helpers. Verification never extracts files."""

import argparse
import gzip
import os
import sys
import tarfile
from pathlib import PurePosixPath

CHUNK_SIZE = 1024 * 1024


def verify(source):
    # Drain every payload and the gzip trailer: tar's member listing alone
    # does not verify the compressed stream CRC or the end of the last file.
    with gzip.GzipFile(fileobj=source) as stream:
        with tarfile.open(fileobj=stream, mode="r|") as archive:
            count = 0
            for member in archive:
                path = PurePosixPath(member.name)
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or not path.parts
                    or path.parts[0] != "ai-media"
                    or not (member.isdir() or member.isfile())
                ):
                    raise ValueError("Unsafe media archive member")
                if member.isfile():
                    with archive.extractfile(member) as payload:
                        while payload.read(CHUNK_SIZE):
                            pass
                count += 1
            if not count:
                raise ValueError("Media archive is empty")
        while stream.read(CHUNK_SIZE):
            pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("create", "verify"))
    args = parser.parse_args()
    if args.action == "create":
        with tarfile.open(fileobj=sys.stdout.buffer, mode="w|gz") as archive:
            archive.add(
                os.environ.get("AI_MEDIA_ROOT", "/workspace/var/ai-media"), arcname="ai-media"
            )
    else:
        verify(sys.stdin.buffer)


if __name__ == "__main__":
    main()
