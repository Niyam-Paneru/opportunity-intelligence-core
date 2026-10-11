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

    def test_repeated_identity_parameter_order_is_preserved(self):
        # A last-value consumer resolves these to different opportunity IDs.
        a = Opportunity("Need API fix", "https://example.test/request?id=42&id=43")
        b = Opportunity("Need API fix", "https://example.test/request?id=43&id=42")
        self.assertNotEqual(duplicate_key(a), duplicate_key(b))

    def test_default_https_port_normalizes_away(self):
        self.assertEqual(
            canonical_url("https://Example.COM:443/request/1/"),
            "https://example.com/request/1",
        )

    def test_ipv6_source_preserves_valid_bracketed_authority(self):
        self.assertEqual(
            canonical_url("HTTPS://[2001:DB8::1]:443/request/42/?utm_source=mail#top"),
            "https://[2001:db8::1]/request/42",
        )
        self.assertEqual(
            canonical_url("https://[2001:db8::1]:8443/request/42"),
            "https://[2001:db8::1]:8443/request/42",
        )

    def test_unicode_only_titles_do_not_collapse_to_one_identity(self):
        url = "https://example.test/request/42"
        a = Opportunity("नेपाली बैकएन्ड", url)
        b = Opportunity("हिन्दी सहायता", url)
        self.assertNotEqual(duplicate_key(a), duplicate_key(b))
        self.assertEqual(duplicate_key(a)[1], "नेपाली बैकएन्ड")
        self.assertEqual(duplicate_key(b)[1], "हिन्दी सहायता")

    def test_unicode_casefold_nfkc_and_combining_marks_are_preserved(self):
        url = "https://example.test/request/42"
        self.assertEqual(
            duplicate_key(Opportunity("ＣＡＦＥ́ API-Fix!", url)),
            duplicate_key(Opportunity("café api fix", url)),
        )
        self.assertNotEqual(
            duplicate_key(Opportunity("中文修复", url)),
            duplicate_key(Opportunity("中文测试", url)),
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
