# Changelog

All notable changes to cat-web will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-08-04

### Added
- **`collapse_themes` is now re-exported from the shared cat-stack engine**,
  completing the two-stage discovery workflow (`explore()` ->
  `collapse_themes()`) without a second import. Its prompts are
  self-contained rather than domain-keyed, so no web wrapping applies.
- **`[agent]` and `[codex-agent]` extras** — install the Claude- and
  ChatGPT-subscription backends (`pip install "cat-web[agent]"`), mirroring
  cat-stack's extras of the same names.

### Fixed
- `classify()`, `extract()`, and `explore()` no longer raise eagerly when
  `api_key` is `None` — the subscription/CLI backends (`claude-code`,
  `claude-agent`, `codex-agent`) and `ollama` need no key; HTTP providers
  still get a clear missing-key error from the engine's provider layer.

### Changed
- The `cat-stack` dependency floor is raised from `>=1.6.3` to `>=2.5.1`,
  required for the `collapse_themes` re-export (with `top_n`/`prune`) and
  for `extract()`'s explore -> collapse_themes consolidation engine.

## [0.2.3] - 2026-07-03

### Fixed
- **`extract()` no longer triggers a `DeprecationWarning` from cat-stack.**
  The wrapper forwarded the deprecated `survey_question=` parameter to
  `catstack.extract()`; it now passes the canonical `description=` (both
  land in the same resolved description, so behavior is unchanged).
  cat-stack 2.0.0 (stable) is out; the existing `cat-stack>=1.6.3` pin
  resolves to it automatically.

---

## [0.2.1] - 2026-05-16

### Changed
- **`extract()` and `explore()`** now pass `domain="web"` to `catstack.extract()`
  and `catstack.explore()`, selecting web-specific prompt templates (uses
  "web content" / "pages" language in the semantic merge step). Requires
  `cat-stack >= 1.0.20`.

---

## [0.2.0] - 2026-05-11

### Added
- **`cat_web` import alias**: `import cat_web` now works alongside the
  canonical `import catweb`; both resolve to the same module object,
  aligning the import name with the underscored convention used elsewhere
  in the cat-* family without breaking existing code.

### Changed
- **Internal imports** of `cat_stack` rewritten to `catstack`. Now requires
  `cat-stack>=1.0.19`.

---

## [0.1.0] - Initial release

- URL fetching, web-content classification, extraction, exploration, and
  summarization via the cat-stack engine.
