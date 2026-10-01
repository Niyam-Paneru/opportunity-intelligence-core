from __future__ import annotations

import re
from urllib.parse import urlsplit, urlunsplit

from .models import Opportunity


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
    return urlunsplit((scheme, host, path, "", ""))


def normalized_title(title: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", title.lower()))


def duplicate_key(opportunity: Opportunity) -> tuple[str, str]:
    return canonical_url(opportunity.source_url), normalized_title(opportunity.title)
