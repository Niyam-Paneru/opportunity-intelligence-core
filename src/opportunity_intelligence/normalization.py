from __future__ import annotations

import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from .models import Opportunity


_TRACKING_QUERY_KEYS = frozenset(
    {
        "utm",
        "gclid",
        "fbclid",
        "msclkid",
        "mc_cid",
        "mc_eid",
    }
)


def _is_tracking_query_key(key: str) -> bool:
    normalized = key.lower()
    return normalized in _TRACKING_QUERY_KEYS or normalized.startswith("utm_")


def canonical_url(url: str) -> str:
    parts = urlsplit(url.strip())
    scheme = parts.scheme.lower()

    if scheme not in {"http", "https"} or not parts.hostname:
        raise ValueError("invalid_source_url")
    if parts.username or parts.password:
        raise ValueError("credentials_not_allowed_in_source_url")

    host = parts.hostname.lower()
    if parts.port is not None:
        default_port = (scheme == "http" and parts.port == 80) or (
            scheme == "https" and parts.port == 443
        )
        if not default_port:
            host = f"{host}:{parts.port}"

    path = re.sub(r"/+$", "", parts.path or "/") or "/"

    kept_query = [
        (key, value)
        for key, value in parse_qsl(parts.query, keep_blank_values=True)
        if not _is_tracking_query_key(key)
    ]
    # Repeated-key value order can identify different sources (e.g. last ID wins).
    query = urlencode(sorted(kept_query, key=lambda pair: pair[0]), doseq=True)

    # Fragments are client-side navigation state and do not identify the source.
    return urlunsplit((scheme, host, path, query, ""))


def normalized_title(title: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", title.lower()))


def duplicate_key(opportunity: Opportunity) -> tuple[str, str]:
    return canonical_url(opportunity.source_url), normalized_title(opportunity.title)
