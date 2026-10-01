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

    def test_default_https_port_normalizes_away(self):
        self.assertEqual(
            canonical_url("https://Example.COM:443/request/1/"),
            "https://example.com/request/1",
        )

    def test_relative_source_url_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "invalid_source_url"):
            canonical_url("/request/1")

    def test_credentials_in_source_url_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "credentials_not_allowed"):
            canonical_url("https://user:pass@example.com/request/1")

    def test_blank_opportunity_identity_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "title_required"):
            Opportunity("   ", "https://example.test/a")
        with self.assertRaisesRegex(ValueError, "source_url_required"):
            Opportunity("Need API help", "   ")


if __name__ == "__main__":
    unittest.main()
