#!/usr/bin/env python3
import os, shutil

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app", "entry.png")

def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    print(f"Copied {SRC} -> {dst} ({os.path.getsize(dst)} bytes)")

if __name__ == "__main__":
    main()
