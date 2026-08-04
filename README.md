# CatWeb

LLM-powered classification, extraction, and summarization for web content.

Part of the [CatLLM ecosystem](https://github.com/chrissoria/cat-llm). Thin wrapper around [cat-stack](https://github.com/chrissoria/cat-stack) that adds URL fetching and web-specific context injection.

## Installation

```bash
pip install cat-web        # pulls in cat-stack automatically
pip install cat-web[pdf]   # with PDF support
```

## Quick Start

```python
import catweb as cat

# Classify web pages by topic
results = cat.classify(
    categories=["News", "Opinion", "Tutorial", "Reference"],
    input_data=[
        "https://example.com/article1",
        "https://example.com/article2",
    ],
    api_key="your-api-key",
)

# Extract categories from web content
extracted = cat.extract(
    input_data=["https://example.com/page1", "https://example.com/page2"],
    description="Blog posts about technology",
    api_key="your-api-key",
)

# Summarize web pages
summaries = cat.summarize(
    input_data=["https://example.com/article1"],
    description="News articles",
    api_key="your-api-key",
)
```

## How It Works

CatWeb accepts URLs as input, fetches the web content, strips HTML to plain text, and passes the text through cat-stack's classification/extraction/summarization pipeline. Original URLs are preserved in the output DataFrame's `survey_input` column.

You can also pass pre-fetched text directly — CatWeb auto-detects whether input is URLs or plain text.

## API Reference

### `classify(categories, input_data, api_key, ...)`

Classify web content into predefined categories.

| Parameter | Type | Description |
|-----------|------|-------------|
| `categories` | list | Category names for classification |
| `input_data` | list/Series | URLs or text strings to classify |
| `api_key` | str | API key for the model provider |
| `source_domain` | str | Source domain (injected as prompt context) |
| `content_type` | str | Content type, e.g. "news article", "blog post" |
| `web_metadata` | dict | Additional key-value context for the prompt |
| `timeout` | int | URL fetch timeout in seconds (default 30) |
| `**kwargs` | | All cat-stack classify() parameters (models, creativity, batch_mode, etc.) |

### `extract(input_data, api_key, ...)`

Discover categories from web content.

| Parameter | Type | Description |
|-----------|------|-------------|
| `input_data` | list/Series | URLs or text strings |
| `api_key` | str | API key |
| `source_domain` | str | Source domain context |
| `content_type` | str | Content type context |
| `web_metadata` | dict | Additional context |
| `timeout` | int | URL fetch timeout (default 30) |
| `**kwargs` | | All cat-stack extract() parameters |

### `explore(input_data, api_key, ...)`

Raw category extraction (with duplicates) for saturation analysis.

Same parameters as `extract()`, plus all cat-stack `explore()` parameters.

### `collapse_themes(input_data, api_key, ...)`

Consolidate the raw label inventory from `explore()` into a smaller, deduplicated taxonomy (re-exported from the shared cat-stack engine): Jaro-Winkler dedup and embedding pre-merge, quality-controlled LLM merge passes, and an optional count-guided reduction to the `top_n` most common categories. This is the same consolidation `extract()` runs internally since cat-stack 2.5.0. See the [cat-stack README](https://github.com/chrissoria/cat-stack#collapse_themes) for the full parameter table.

### `summarize(input_data, ...)`

Summarize web content.

| Parameter | Type | Description |
|-----------|------|-------------|
| `input_data` | list/Series | URLs or text strings |
| `source_domain` | str | Source domain context |
| `content_type` | str | Content type context |
| `web_metadata` | dict | Additional context |
| `timeout` | int | URL fetch timeout (default 30) |
| `**kwargs` | | All cat-stack summarize() parameters (api_key, description, models, etc.) |

### Web Utilities

```python
from catweb import is_url, fetch_url_text, fetch_urls

# Check if a string is a URL
is_url("https://example.com")  # True
is_url("just text")            # False

# Fetch a single URL
text, error = fetch_url_text("https://example.com")

# Fetch multiple URLs
results = fetch_urls(["https://a.com", "https://b.com"])
# Returns: [(url, text, error), ...]
```

## Multi-Model Ensemble

All cat-stack ensemble features work through `**kwargs`:

```python
results = cat.classify(
    categories=["Positive", "Negative", "Neutral"],
    input_data=urls,
    models=[
        ("gpt-4o", "openai", "sk-..."),
        ("claude-sonnet-4-5-20250929", "anthropic", "sk-ant-..."),
    ],
    consensus_threshold="majority",
)
```

## License

GPL-3.0-or-later
