import unittest

from bom_fetcher import BOM_ROOT, parse_image_paths

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


if __name__ == "__main__":
    unittest.main()
