import unittest

from opportunity_intelligence.models import Opportunity
from opportunity_intelligence.normalization import canonical_url, duplicate_key


class NormalizationTests(unittest.TestCase):
    def test_url_drops_query_fragment_and_trailing_slash(self):
        self.assertEqual(
            canonical_url("HTTPS://Example.COM/request/1/?utm=x#top"),
            "https://example.com/request/1",
        )

    def test_duplicate_key_normalizes_title(self):
        a = Opportunity("Need   API-Fix!", "https://example.test/a")
        b = Opportunity("need api fix", "https://example.test/a/")
        self.assertEqual(duplicate_key(a), duplicate_key(b))


if __name__ == "__main__":
    unittest.main()
