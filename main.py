#!/usr/bin/env python3
"""make.fun entry: news-image-20261124.

Copies the bundled poster image (entry.png, stored beside this file) into
the output directory named by the MAKEFUN_OUTPUT_DIR environment
variable, defaulting to /output. A straight byte copy, so two runs always
produce identical bytes.
"""

import os
import shutil

OUTPUT_NAME = "entry.png"


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, OUTPUT_NAME)
    if not os.path.isfile(source):
        raise FileNotFoundError(f"bundled image missing: {source}")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(source, os.path.join(out_dir, OUTPUT_NAME))


if __name__ == "__main__":
    main()
