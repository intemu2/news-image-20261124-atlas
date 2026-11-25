#!/usr/bin/env python3
"""news-image-20261124-atlas entry point.

Copies the pre-rendered entry.png into the output directory required
by the make.fun harness. Standard library only.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    if not os.path.isfile(SRC):
        print("entry.png missing next to main.py", file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    src_size = os.path.getsize(SRC)
    dst_size = os.path.getsize(dst)
    if src_size != dst_size:
        print(f"size mismatch: src={src_size} dst={dst_size}", file=sys.stderr)
        return 1
    if sha256_of(SRC) != sha256_of(dst):
        print("sha256 mismatch after copy", file=sys.stderr)
        return 1
    print(f"wrote {dst} ({dst_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
