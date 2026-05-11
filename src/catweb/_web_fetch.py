"""
Re-export web fetching utilities from catstack.

These functions now live in catstack._web_fetch. This module re-exports
them for backward compatibility within cat-web.
"""

from catstack._web_fetch import (
    is_url,
    fetch_url_text,
    fetch_urls,
    detect_url_input,
    strip_html_tags,
)

__all__ = [
    "is_url",
    "fetch_url_text",
    "fetch_urls",
    "detect_url_input",
    "strip_html_tags",
]
