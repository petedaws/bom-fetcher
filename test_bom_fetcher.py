import tempfile
import unittest
from unittest import mock
from pathlib import Path

from bom_fetcher import BOM_ROOT, parse_image_paths, fetch_radar_frames

SAMPLE_HTML = """
<script type="text/javascript">
var theImageNames = new Array();
theImageNames[0] = "/radar/IDR663.20240522-0000.png";
theImageNames[1] = "/radar/IDR663.20240522-0030.png";
theImageNames[2] = "/radar/IDR663.20240522-0100.png";
</script>
"""

class ParseImagePathsTests(unittest.TestCase):
    def test_extracts_all_radar_frames(self):
        self.assertEqual(
            [
                "/radar/IDR663.20240522-0000.png",
                "/radar/IDR663.20240522-0030.png",
                "/radar/IDR663.20240522-0100.png",
            ],
            parse_image_paths(SAMPLE_HTML),
        )

    def test_bom_root_points_to_reg_domain(self):
        self.assertEqual("https://reg.bom.gov.au", BOM_ROOT)


class FetchRadarFramesTests(unittest.TestCase):
    def test_limit_stops_after_requested_number(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            download_log = []

            def fake_download(url: str, timeout: float):
                download_log.append(url)
                if url.endswith(".shtml"):
                    return SAMPLE_HTML.encode()
                return b"image-bytes"

            with mock.patch("bom_fetcher._download", side_effect=fake_download):
                frame_count = fetch_radar_frames(Path(tmp_dir), limit=2)

        self.assertEqual(frame_count, 2)
        self.assertEqual(len(download_log), 3)


if __name__ == "__main__":
    unittest.main()
