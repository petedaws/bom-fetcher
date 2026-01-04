#!/usr/bin/env python3
"""Download the latest Mt Stapylton radar frames from the BOM website."""

import argparse
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BOM_ROOT = "https://reg.bom.gov.au"
MT_STAPYLTON_RADAR = "/products/IDR663.loop.shtml"
USER_AGENT = "bom-fetcher/2.0"
IMAGE_REGEXP = re.compile(r'theImageNames\[\d+\]\s*=\s*"(/radar/)([^"\\]+\.png)"')


def parse_image_paths(html: str) -> list[str]:
    """Return relative image paths embedded in the BOM HTML page."""

    return [prefix + filename for prefix, filename in IMAGE_REGEXP.findall(html)]

def _download(url: str, *, timeout: float) -> bytes:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=timeout) as response:
            return response.read()
    except (HTTPError, URLError) as exc:
        raise RuntimeError(f"Unable to download {url}: {exc}") from exc


def fetch_radar_frames(
    output_directory: Path, *, limit: int | None = None, timeout: float = 10.0
) -> int:
    """Fetch radar frames into ``output_directory``.

    The BOM HTML lists image names in a JavaScript array; this function parses
    those entries and downloads each referenced PNG.
    """

    html = _download(BOM_ROOT + MT_STAPYLTON_RADAR, timeout=timeout).decode("utf-8")
    image_paths: list[str] = parse_image_paths(html)
    if limit is not None:
        image_paths = image_paths[:limit]

    output_directory.mkdir(parents=True, exist_ok=True)

    for image_path in image_paths:
        filename = Path(image_path).name
        destination = output_directory / filename
        try:
            destination.write_bytes(
                _download(BOM_ROOT + image_path, timeout=timeout)
            )
        except RuntimeError as exc:
            raise RuntimeError(f"Unable to download {filename}: {exc}") from exc

    return len(image_paths)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Download the latest Mt Stapylton radar frames from the BOM website."
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("."),
        help="Directory where the radar frames will be saved (default: current directory)",
    )
    parser.add_argument(
        "-n",
        "--max-frames",
        type=int,
        default=None,
        help="Limit how many frames are downloaded. Defaults to all available frames.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=10.0,
        help="Maximum time to wait for network responses in seconds (default: 10).",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)

    try:
        frame_count = fetch_radar_frames(
            args.output, limit=args.max_frames, timeout=args.timeout
        )
    except RuntimeError as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)

    print(f"Downloaded {frame_count} frame(s) to {args.output}")


if __name__ == "__main__":
    main()
