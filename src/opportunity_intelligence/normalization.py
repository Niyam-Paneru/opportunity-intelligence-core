from __future__ import annotations

import re
from urllib.parse import urlsplit, urlunsplit

from .models import Opportunity


def canonical_url(url: str) -> str:
    parts = urlsplit(url.strip())
    host = parts.netloc.lower()
    path = re.sub(r"/+$", "", parts.path or "/")
    return urlunsplit((parts.scheme.lower(), host, path, "", ""))


def normalized_title(title: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", title.lower()))


def duplicate_key(opportunity: Opportunity) -> tuple[str, str]:
    return canonical_url(opportunity.source_url), normalized_title(opportunity.title)
