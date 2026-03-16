# SPDX-FileCopyrightText: 2025-present Christopher Soria <chrissoria@berkeley.edu>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from .__about__ import (
    __version__,
    __author__,
    __description__,
    __title__,
    __url__,
    __license__,
)

# =============================================================================
# Public API — catweb entry points (thin wrappers around cat_stack)
# =============================================================================
from .classify import classify
from .extract import extract
from .explore import explore
from .summarize import summarize

# =============================================================================
# Web fetching utilities (catweb-specific)
# =============================================================================
from ._web_fetch import (
    is_url,
    fetch_url_text,
    fetch_urls,
    detect_url_input,
    strip_html_tags,
)

# =============================================================================
# Re-exports from cat_stack (backward compatibility + provider utilities)
# =============================================================================
from cat_stack import (
    # Category analysis
    has_other_category,
    check_category_verbosity,
    # Batch exceptions
    BatchJobExpiredError,
    BatchJobFailedError,
    # Provider utilities
    UnifiedLLMClient,
    detect_provider,
    set_ollama_endpoint,
    check_ollama_running,
    list_ollama_models,
    check_ollama_model,
    pull_ollama_model,
    PROVIDER_CONFIG,
    # Deprecated backward-compat functions
    explore_common_categories,
    explore_corpus,
    explore_image_categories,
    explore_pdf_categories,
    classify_ensemble,
    multi_class,
    image_multi_class,
    pdf_multi_class,
    summarize_ensemble,
    # Utilities
    build_json_schema,
    extract_json,
    validate_classification_json,
    image_score_drawing,
    image_features,
)

# Define public API
__all__ = [
    # Main entry points (catweb wrappers)
    "classify",
    "extract",
    "explore",
    "summarize",
    # Web fetching utilities
    "is_url",
    "fetch_url_text",
    "fetch_urls",
    "detect_url_input",
    "strip_html_tags",
    # Category analysis (from cat_stack)
    "has_other_category",
    "check_category_verbosity",
    # Batch exceptions (from cat_stack)
    "BatchJobExpiredError",
    "BatchJobFailedError",
    # Provider utilities (from cat_stack)
    "UnifiedLLMClient",
    "detect_provider",
    "set_ollama_endpoint",
    "check_ollama_running",
    "list_ollama_models",
    "check_ollama_model",
    "pull_ollama_model",
    "PROVIDER_CONFIG",
    # Deprecated backward-compat (from cat_stack)
    "explore_common_categories",
    "explore_corpus",
    "explore_image_categories",
    "explore_pdf_categories",
    "classify_ensemble",
    "summarize_ensemble",
    "multi_class",
    "image_multi_class",
    "pdf_multi_class",
    "image_score_drawing",
    "image_features",
    "build_json_schema",
    "extract_json",
    "validate_classification_json",
]
