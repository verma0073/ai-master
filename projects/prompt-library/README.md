# Prompt Library

The first hands-on deliverable of **AI Master**, Sprint 1.

A validated, versioned, testable collection of reusable prompt templates —
built as a reusable engine (`shared/prompts/`) plus a content library that
uses it (this folder). Every other AI Master project (RAG, agents, chatbots)
is expected to import from `shared.prompts` rather than hardcoding prompt
strings inline.

## Why this exists (and why it's not just a folder of .txt files)

Prompt strings scattered through application code have three problems that
show up the moment a project grows past a demo:

1. **No metadata.** You can't tell what inputs a prompt needs without reading
   the code that calls it.
2. **No versioning.** If you tweak a prompt, you have no record of what
   changed or a way to pin a known-good version for reproducible evals.
3. **No validation.** A typo'd variable name silently renders a broken
   prompt instead of failing loudly.

This library solves all three: prompts are YAML records validated against a
Pydantic schema (`shared/prompts/schema.py`), rendered with Jinja2 in strict
mode (missing/misspelled variables raise instead of failing silently), and
addressed by `(id, version)` so behavior is pinnable.

## Structure

```
shared/prompts/          <- reusable engine (import this from any project)
    schema.py             Pydantic models: PromptTemplate, PromptVariable
    loader.py              PromptLibrary: load, validate, get, list, search, render

projects/prompt-library/  <- this project: content + demo + tests
    prompts/
        coding/
        writing/
        rag/
    cli.py                 CLI demo (list / show / render / search)
    tests/
        test_loader.py      11 tests covering happy path + failure modes
```

## Usage

```python
from shared.prompts import PromptLibrary

lib = PromptLibrary("projects/prompt-library/prompts")

lib.list(category="coding")

lib.render(
    "code-review-strict",
    language="python",
    code_snippet="def f(x): return x/0",
)

# pin a version for reproducible evals
lib.get("qa-with-context", version="1.0.0")
```

CLI:

```bash
python projects/prompt-library/cli.py list
python projects/prompt-library/cli.py show code-review-strict
python projects/prompt-library/cli.py render bug-explainer \
    --var language=python --var code_snippet="x=1/0" --var error_message="ZeroDivisionError"
python projects/prompt-library/cli.py search hallucination
```

## Adding a new prompt

1. Add a YAML file under the right category folder in `prompts/`.
2. It must satisfy `PromptTemplate` (see `shared/prompts/schema.py`):
   `id` (kebab-case), `name`, `version`, `category`, `description`, `template`,
   and any `variables` the template references.
3. Add at least one `examples` entry — not asserted at runtime, but used as
   the seed for a regression test when you add one.
4. Run `pytest projects/prompt-library/tests/` — a malformed prompt fails
   the whole suite (fail-fast, on purpose).

## Tests

```bash
pip install -r requirements/dev.txt
pytest projects/prompt-library/tests/ -v
```

11 tests, covering: real prompts load correctly, category/tag filtering,
search, successful render, default-variable fallback, missing-required-variable
error, unknown-id error, version pinning, StrictUndefined catching a
typo'd template variable, duplicate id+version rejection, and invalid
id-casing rejection.

## Deliberately deferred (and why)

Per `docs/03-Architecture.md`, "every project should include Docker
support." This project **intentionally has no Dockerfile yet.** A pure
Python library with no runtime service has nothing to containerize —
adding Docker now would be cargo-culting the checklist rather than
following its intent. Docker support lands when this library gets wrapped
in the Sprint 2 FastAPI service that serves prompts over HTTP.

## Status

| Item | Status |
|---|---|
| Schema + loader (`shared/prompts`) | ✅ Done |
| 4 seed prompts across 3 categories | ✅ Done |
| CLI | ✅ Done |
| Tests (11 passing) | ✅ Done |
| requirements/base.txt, requirements/dev.txt | ✅ Done |
| FastAPI wrapper | ⏳ Sprint 2 |
| Docker | ⏳ Sprint 2 (see note above) |
