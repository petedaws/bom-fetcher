#!/usr/bin/env python3
"""Download the latest Mt Stapylton radar frames from the BOM website."""

from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BOM_ROOT = "https://reg.bom.gov.au"
MT_STAPYLTON_RADAR = "/products/IDR663.loop.shtml"
IMAGE_REGEXP = re.compile(r'theImageNames\[\d+\]\s*=\s*"(/radar/)([^"\\]+\.png)"')


def parse_image_paths(html: str) -> list[str]:
    """Return relative image paths embedded in the BOM HTML page."""

    return [prefix + filename for prefix, filename in IMAGE_REGEXP.findall(html)]

def fetch_radar_frames(output_directory: Path) -> None:
    """Fetch radar frames into ``output_directory``.

    The BOM HTML lists image names in a JavaScript array; this function parses
    those entries and downloads each referenced PNG.
    """

    request = Request(
        BOM_ROOT + MT_STAPYLTON_RADAR,
        headers={"User-Agent": "bom-fetcher/1.0"},
    )

    try:
        with urlopen(request) as response:
            html = response.read().decode("utf-8")
    except (HTTPError, URLError) as exc:
        raise RuntimeError(f"Unable to download radar listing: {exc}") from exc

    output_directory.mkdir(parents=True, exist_ok=True)

    for image_path in parse_image_paths(html):
        filename = Path(image_path).name
        destination = output_directory / filename
        image_request = Request(
            BOM_ROOT + image_path, headers={"User-Agent": "bom-fetcher/1.0"}
        )
        try:
            with urlopen(image_request) as image_response:
                destination.write_bytes(image_response.read())
        except (HTTPError, URLError) as exc:
            raise RuntimeError(f"Unable to download {filename}: {exc}") from exc


def main() -> None:
    output_directory = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    try:
        fetch_radar_frames(output_directory)
    except RuntimeError as exc:
        print(exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
