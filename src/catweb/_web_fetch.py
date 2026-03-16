"""
Re-export web fetching utilities from cat_stack.

These functions now live in cat_stack._web_fetch. This module re-exports
them for backward compatibility within cat-web.
"""

from cat_stack._web_fetch import (
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
