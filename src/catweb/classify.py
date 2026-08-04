"""
Classification functions for CatWeb.

Thin wrapper around catstack.classify() that adds web-specific features:
- URL fetching (accepts list of URLs as input_data)
- Web context injection (source_domain, content_type)
- Post-classification URL preservation (original URLs in input_data column)
"""

import catstack

from ._web_fetch import fetch_urls, is_url

__all__ = [
    "classify",
]


def _normalize_url_list(input_data):
    """Normalize input_data to a list of URL strings."""
    if isinstance(input_data, str):
        return [input_data]
    elif hasattr(input_data, 'tolist'):
        return input_data.tolist()
    else:
        return list(input_data)


def _build_web_context(source_domain, content_type, web_metadata):
    """Build a context block string from web content metadata fields."""
    parts = []
    if source_domain:
        parts.append(f"Source domain: {source_domain}")
    if content_type:
        parts.append(f"Content type: {content_type}")
    if web_metadata:
        for k, v in web_metadata.items():
            parts.append(f"{k.capitalize()}: {v}")
    return "\n".join(parts)


def classify(
    categories,
    input_data=None,
    api_key=None,
    # Web context fields — injected into the classification prompt
    source_domain: str = None,
    content_type: str = None,
    web_metadata: dict = None,
    description="",
    filename=None,
    save_directory=None,
    timeout: int = 30,
    **kwargs,
):
    """
    Classify web content (URLs) with web-specific features.

    Wraps catstack.classify() and adds:
    - Automatic URL fetching (pass a list of URLs as input_data)
    - Web context injection into the classification prompt
    - Original URLs preserved in the input_data column

    Args:
        categories (list): List of category names for classification.
        input_data: The data to classify. Can be:
            - List of URLs (auto-fetched and classified as text)
            - List of text strings (classified directly, no fetching)
            - pandas Series of URLs or text
        api_key (str): API key for the model provider (single-model mode).
        source_domain (str): Source domain — injected into the prompt as context.
        content_type (str): Content type (e.g., "news article", "blog post").
        web_metadata (dict): Additional context injected into the prompt.
        description (str): Description of the input data context.
        filename (str): Output filename for CSV.
        save_directory (str): Directory to save results.
        timeout (int): Timeout in seconds for URL fetching. Default 30.
        **kwargs: All other parameters passed through to catstack.classify()
            (e.g. user_model, models, creativity, batch_mode, consensus_threshold,
            chain_of_thought, thinking_budget, embeddings, etc.)

    Returns:
        pd.DataFrame: Results with classification columns. When URLs are
        provided, the input_data column contains the original URLs
        (not the fetched content).

    Examples:
        >>> import catweb as cat
        >>>
        >>> # Classify web pages by topic
        >>> results = cat.classify(
        ...     categories=["News", "Opinion", "Tutorial", "Reference"],
        ...     input_data=["https://example.com/article1", "https://example.com/article2"],
        ...     api_key="your-api-key",
        ... )
        >>>
        >>> # Classify with web context
        >>> results = cat.classify(
        ...     input_data=urls,
        ...     categories=["Positive", "Negative", "Neutral"],
        ...     source_domain="news.ycombinator.com",
        ...     content_type="forum discussion",
        ...     api_key="your-api-key",
        ... )
        >>>
        >>> # Classify pre-fetched text (no URL fetching)
        >>> results = cat.classify(
        ...     input_data=["Some text content...", "More text..."],
        ...     categories=["Tech", "Science", "Politics"],
        ...     api_key="your-api-key",
        ... )
    """
    # api_key may be None: subscription/CLI backends (claude-code,
    # claude-agent, codex-agent) and ollama need no key; HTTP providers get
    # a clear missing-key error from the engine's provider layer.

    if input_data is None:
        raise ValueError("[CatWeb] input_data is required.")

    # Check if input is URLs — fetch content if so
    _url_originals = None
    from ._web_fetch import detect_url_input
    if detect_url_input(input_data):
        url_list = _normalize_url_list(input_data)
        print(f"[CatWeb] Fetching content from {len(url_list)} URLs...")
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

    # Prepend web context to description if any fields provided
    web_context = _build_web_context(source_domain, content_type, web_metadata)
    if web_context:
        description = f"{web_context}\n{description}".strip() if description else web_context

    # Remove keys we set explicitly to avoid "multiple values" if caller also passes them
    kwargs.pop("add_other", None)
    kwargs.pop("check_verbosity", None)

    result = catstack.classify(
        input_data=input_data,
        categories=categories,
        api_key=api_key,
        description=description,
        add_other=False,
        check_verbosity=False,
        filename=None if _url_originals else filename,
        save_directory=None if _url_originals else save_directory,
        **kwargs,
    )

    # Replace fetched text with original URLs in input_data column
    if _url_originals is not None:
        result = result.reset_index(drop=True)
        if "input_data" in result.columns:
            result["input_data"] = _url_originals
        # Save with URLs if filename was requested
        if filename or save_directory:
            import os as _os
            out = filename
            if save_directory and filename:
                out = _os.path.join(save_directory, _os.path.basename(filename))
            elif save_directory:
                out = _os.path.join(save_directory, "results.csv")
            if out:
                result.to_csv(out, index=False)
                print(f"Results saved to {out}")

    return result
