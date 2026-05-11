"""
Summarization functions for CatWeb.

Thin wrapper around catstack.summarize() that adds web-specific features:
- URL fetching (accepts list of URLs as input_data)
- Web context injection
- Original URLs preserved in output
"""

import catstack

from ._web_fetch import fetch_urls, detect_url_input

__all__ = [
    "summarize",
]


def summarize(
    input_data=None,
    # Web context fields
    source_domain: str = None,
    content_type: str = None,
    web_metadata: dict = None,
    timeout: int = 30,
    **kwargs,
):
    """
    Summarize web content (URLs or text) using LLMs.

    Wraps catstack.summarize() and adds:
    - Automatic URL fetching (pass a list of URLs as input_data)
    - Web context injection into the summarization prompt
    - Original URLs preserved in the input_data column

    Args:
        input_data: Data to summarize. Can be:
            - List of URLs (auto-fetched and summarized as text)
            - List of text strings, pandas Series, or single string
        source_domain (str): Source domain — injected into the prompt as context.
        content_type (str): Content type (e.g., "news article", "blog post").
        web_metadata (dict): Additional context injected into the prompt.
        timeout (int): Timeout in seconds for URL fetching. Default 30.
        **kwargs: All parameters passed through to catstack.summarize()
            (e.g. api_key, description, instructions, max_length, focus,
            user_model, models, mode, creativity, batch_mode, etc.)

    Returns:
        pd.DataFrame: Results with summary column(s). When URLs are
        provided, the input_data column contains the original URLs.

    Examples:
        >>> import catweb as cat
        >>>
        >>> results = cat.summarize(
        ...     input_data=["https://example.com/article1", "https://example.com/article2"],
        ...     description="News articles",
        ...     api_key="your-api-key",
        ... )
    """
    if input_data is None:
        raise ValueError("[CatWeb] input_data is required.")

    # Check if input is URLs — fetch content if so
    _url_originals = None
    if detect_url_input(input_data):
        if isinstance(input_data, str):
            url_list = [input_data]
        elif hasattr(input_data, 'tolist'):
            url_list = input_data.tolist()
        else:
            url_list = list(input_data)

        print(f"[CatWeb] Fetching content from {len(url_list)} URLs for summarization...")
        url_results = fetch_urls(url_list, timeout=timeout)

        _url_originals = []
        fetched_texts = []
        success_count = 0
        for url, text, error in url_results:
            _url_originals.append(url)
            if error:
                print(f"  Warning: {error}")
                fetched_texts.append("")
            else:
                fetched_texts.append(text)
                success_count += 1

        print(f"[CatWeb] Successfully fetched {success_count}/{len(url_list)} URLs")
        input_data = fetched_texts

    # Build web context and inject into description
    parts = []
    if source_domain:
        parts.append(f"Source domain: {source_domain}")
    if content_type:
        parts.append(f"Content type: {content_type}")
    if web_metadata:
        for k, v in web_metadata.items():
            parts.append(f"{k.capitalize()}: {v}")
    web_context = "\n".join(parts)

    if web_context:
        desc = kwargs.get("description", "")
        kwargs["description"] = f"{web_context}\n{desc}".strip() if desc else web_context

    result = catstack.summarize(
        input_data=input_data,
        **kwargs,
    )

    # Replace fetched text with original URLs in input_data column
    if _url_originals is not None:
        result = result.reset_index(drop=True)
        if "input_data" in result.columns:
            result["input_data"] = _url_originals

    return result
