"""
Category exploration functions for CatWeb.

Thin wrapper around cat_stack.explore() that adds web-specific features:
- URL fetching (accepts list of URLs as input_data)
- Web context injection
"""

import cat_stack

from ._web_fetch import fetch_urls, detect_url_input

__all__ = [
    "explore",
]


def explore(
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
    Explore categories in web content, returning the raw extracted list.

    Wraps cat_stack.explore() and adds:
    - Automatic URL fetching (pass a list of URLs as input_data)
    - Web context injection into the exploration prompt

    Unlike extract(), which normalizes and merges categories, explore()
    returns every category string from every chunk across every iteration
    — with duplicates intact.

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
        **kwargs: All other parameters passed through to cat_stack.explore()
            (e.g. max_categories, categories_per_chunk, divisions, user_model,
            creativity, specificity, research_question, filename, model_source,
            iterations, random_state, focus, etc.)

    Returns:
        list[str]: Every category string extracted from every chunk across
        every iteration.

    Examples:
        >>> import catweb as cat
        >>>
        >>> raw_categories = cat.explore(
        ...     input_data=["https://example.com/page1", "https://example.com/page2"],
        ...     description="News articles",
        ...     api_key="your-api-key",
        ...     iterations=3,
        ... )
        >>> print(raw_categories[:5])
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

        print(f"[CatWeb] Fetching content from {len(url_list)} URLs for exploration...")
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

    return cat_stack.explore(
        input_data=input_data,
        api_key=api_key,
        description=description,
        **kwargs,
    )
