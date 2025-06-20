#!/usr/bin/env python

import argparse
import logging
import mimetypes
import pathlib
import os
import subprocess
import sys

from typing import Optional

from PIL import Image
from PIL.ImageFile import ImageFile

SUPPORTED_FORMATS: dict[str, str] = {
    "image/jpeg": "jpeg",
    "image/png": "png",
    "application/pdf": "pdf",
}


def human_readable_size(size_in_bytes):
    for unit in ["B", "K", "M"]:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f}{unit}"
        size_in_bytes /= 1024


def parse_args() -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("-i", type=pathlib.Path, help="file to resize")
    parser.add_argument("-o", type=pathlib.Path, help="output file path")
    parser.add_argument("-s", type=ascii, help="maximum size")
    return parser.parse_args()


def convert_size_to_bytes(size_str: str) -> int:
    if size_str[-1].upper() == "K":
        return int(size_str[:-1]) * 1024
    elif size_str[-1].upper() == "M":
        return int(size_str[:-1]) * 1024**2
    else:
        raise ValueError("Unsupported size format. Use 'K' or 'M'.")


def determine_output_path(
    input_path: pathlib.Path, output_path: Optional[pathlib.Path]
) -> pathlib.Path:
    if output_path:
        return output_path.resolve()
    else:
        output_dir = pathlib.Path(os.path.expanduser("~/tbd/adapted"))
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir / input_path.name


def reduce_pdf(
    input_path: pathlib.Path, output_path: pathlib.Path, max_size: int
) -> None:
    """Reduce the size of a PDF file using Ghostscript."""
    input_size = human_readable_size(input_path.stat().st_size)

    for pdfsettings in ["/ebook", "/screen"]:
        gs_return = subprocess.call(
            [
                "gs",
                "-dNOPAUSE",
                "-dQUIET",
                "-dBATCH",
                "-sDEVICE=pdfwrite",
                f"-dPDFSETTINGS={pdfsettings}",
                f"-sOutputFile={output_path}",
                str(input_path),
            ]
        )

        if gs_return == 0 and output_path.stat().st_size < max_size:
            output_size = human_readable_size(output_path.stat().st_size)
            print(f"File resized successfully from {input_size} to {output_size}.")
            return

    raise Exception("Unable to lower PDF filesize below target size.")


def reduce_image(
    input_path: pathlib.Path, output_path: pathlib.Path, max_size: int, format: str
) -> None:
    """Reduce the size of an image file using PIL."""
    input_size = human_readable_size(input_path.stat().st_size)
    img: ImageFile = Image.open(input_path)

    size_reached: int = 0
    for quality in range(95, 4, -5):
        img.save(output_path, format=format.upper(), quality=quality)
        size_reached = output_path.stat().st_size
        logging.debug(f"{quality}")
        logging.debug(f"{size_reached=}")
        if size_reached < max_size:
            output_size = human_readable_size(output_path.stat().st_size)
            print(
                f"File resized successfully from {input_size} to {output_size} at {quality}% quality."
            )
            return

    raise Exception(
        f"Unable to lower image filesize below {human_readable_size(max_size)}. Lowest reached was {human_readable_size(size_reached)}",
    )


def main() -> None:
    logging.basicConfig(
        filename=os.path.expanduser("~/tbd/debug.log"),
        filemode="w",
        level=logging.DEBUG,
        format="%(lineno)d: %(message)s",
    )

    args: argparse.Namespace = parse_args()

    input_path = args.i.resolve()
    if not input_path.is_file():
        raise Exception(f"Error: Input file '{input_path}' does not exist.")

    mimetype = mimetypes.guess_type(input_path)[0] or ""
    format = SUPPORTED_FORMATS.get(mimetype)
    if not format:
        raise Exception(
            f"Unsupported file type: {mimetype}. Supported types are JPEG, PNG, and PDF.",
        )

    output_path: pathlib.Path = determine_output_path(input_path, args.o)
    max_size: int = convert_size_to_bytes(args.s.strip("'"))

    if input_path.stat().st_size < max_size:
        print("Only size reduction is supported.", file=sys.stderr)
        sys.exit(1)

    if format == "pdf":
        reduce_pdf(input_path, output_path, max_size)
    else:
        reduce_image(input_path, output_path, max_size, format)


if __name__ == "__main__":
    main()
