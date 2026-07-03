"""
Category extraction functions for CatWeb.

Thin wrapper around catstack.extract() that adds web-specific features:
- URL fetching (accepts list of URLs as input_data)
- Web context injection
"""

import catstack

from ._web_fetch import fetch_urls, detect_url_input

__all__ = [
    "extract",
]


def extract(
    input_data=None,
    api_key=None,
    # Web context fields
    source_domain: str = None,
    content_type: str = None,
    web_metadata: dict = None,
    description="",
    timeout: int = 30,
    **kwargs,
):
    """
    Extract categories from web content (URLs or text).

    Wraps catstack.extract() and adds:
    - Automatic URL fetching (pass a list of URLs as input_data)
    - Web context injection into the extraction prompt

    Args:
        input_data: The data to explore. Can be:
            - List of URLs (auto-fetched and processed as text)
            - List of text strings (processed directly)
            - pandas Series of URLs or text
        api_key (str): API key for the model provider.
        source_domain (str): Source domain — injected into the prompt as context.
        content_type (str): Content type (e.g., "news article", "blog post").
        web_metadata (dict): Additional context injected into the prompt.
        description (str): Description of the input data context.
        timeout (int): Timeout in seconds for URL fetching. Default 30.
        **kwargs: All other parameters passed through to catstack.extract()
            (e.g. max_categories, categories_per_chunk, divisions, user_model,
            creativity, specificity, research_question, filename, model_source,
            iterations, random_state, focus, etc.)

    Returns:
        dict with keys:
            - counts_df: DataFrame of categories with counts
            - top_categories: List of top category names
            - raw_top_text: Raw model output from final merge step

    Examples:
        >>> import catweb as cat
        >>>
        >>> # Extract categories from web pages
        >>> results = cat.extract(
        ...     input_data=["https://example.com/page1", "https://example.com/page2"],
        ...     description="News articles",
        ...     api_key="your-api-key",
        ... )
        >>> print(results['top_categories'])
    """
    if api_key is None:
        raise ValueError(
            "[CatWeb] api_key is required. Pass api_key='sk-...'."
        )

    if input_data is None:
        raise ValueError("[CatWeb] input_data is required.")

    # Check if input is URLs — fetch content if so
    if detect_url_input(input_data):
        if isinstance(input_data, str):
            url_list = [input_data]
        elif hasattr(input_data, 'tolist'):
            url_list = input_data.tolist()
        else:
            url_list = list(input_data)

        print(f"[CatWeb] Fetching content from {len(url_list)} URLs for extraction...")
        url_results = fetch_urls(url_list, timeout=timeout)

        input_data = [text if text else "" for _, text, error in url_results]
        success_count = sum(1 for _, _, e in url_results if not e)
        print(f"[CatWeb] Successfully fetched {success_count}/{len(url_list)} URLs")

    # Build web context
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
        description = f"{web_context}\n{description}".strip() if description else web_context

    return catstack.extract(
        input_data=input_data,
        api_key=api_key,
        description=description,
        domain="web",
        **kwargs,
    )
