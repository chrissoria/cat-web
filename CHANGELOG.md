# Changelog

All notable changes to cat-web will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
