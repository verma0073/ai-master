"""
Tests for shared.prompts.PromptLibrary.

Covers:
- Loading the real prompt-library content (regression test: every checked-in
  YAML file must stay valid).
- Rendering success and required-variable enforcement.
- StrictUndefined behavior (a template referencing an unknown variable must fail).
- Version resolution (get latest vs get pinned version).
- Failure modes: duplicate id+version, unknown prompt id.
"""

from __future__ import annotations

import sys
import textwrap
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from shared.prompts import (  # noqa: E402
    PromptLibrary,
    PromptNotFoundError,
    PromptRenderError,
    PromptValidationError,
)

REAL_PROMPTS_DIR = REPO_ROOT / "projects" / "prompt-library" / "prompts"


@pytest.fixture(scope="module")
def library() -> PromptLibrary:
    return PromptLibrary(REAL_PROMPTS_DIR)


def test_loads_real_prompt_library_without_error(library: PromptLibrary):
    prompts = library.list()
    assert len(prompts) >= 4
    ids = {p.id for p in prompts}
    assert "code-review-strict" in ids
    assert "qa-with-context" in ids


def test_filter_by_category(library: PromptLibrary):
    coding_prompts = library.list(category="coding")
    assert all(p.category == "coding" for p in coding_prompts)
    assert len(coding_prompts) >= 2


def test_search_matches_tags_and_description(library: PromptLibrary):
    results = library.search("hallucination")
    assert any(p.id == "qa-with-context" for p in results)


def test_render_success(library: PromptLibrary):
    rendered = library.render(
        "bug-explainer",
        language="python",
        code_snippet="x = 1/0",
        error_message="ZeroDivisionError",
    )
    assert "python" in rendered
    assert "ZeroDivisionError" in rendered


def test_render_uses_default_for_optional_variable(library: PromptLibrary):
    rendered = library.render(
        "code-review-strict",
        language="python",
        code_snippet="print('hi')",
        # context omitted deliberately -> should fall back to default
    )
    assert "No additional context provided." in rendered


def test_render_missing_required_variable_raises(library: PromptLibrary):
    with pytest.raises(PromptRenderError):
        library.render("code-review-strict", language="python")  # missing code_snippet


def test_unknown_prompt_id_raises(library: PromptLibrary):
    with pytest.raises(PromptNotFoundError):
        library.get("does-not-exist")


def test_pinned_version_resolution(library: PromptLibrary):
    latest = library.get("code-review-strict")
    pinned = library.get("code-review-strict", version="1.0.0")
    assert latest.version == pinned.version == "1.0.0"

    with pytest.raises(PromptNotFoundError):
        library.get("code-review-strict", version="9.9.9")


def test_strict_undefined_catches_template_typo(tmp_path):
    """
    A template referencing a variable that isn't declared/passed must raise,
    not silently render blank. This is the core guarantee of using
    StrictUndefined instead of Jinja2's default lenient mode.
    """
    prompt_file = tmp_path / "typo.yaml"
    prompt_file.write_text(
        textwrap.dedent(
            """
            id: typo-test
            name: Typo Test
            version: "1.0.0"
            category: coding
            description: test
            variables:
              - name: correct_variable
                required: true
            template: "Value is {{ correct_varaible }}"
            """
        ).strip()
    )
    lib = PromptLibrary(tmp_path)
    with pytest.raises(PromptRenderError):
        lib.render("typo-test", correct_variable="x")


def test_duplicate_id_and_version_raises(tmp_path):
    content = textwrap.dedent(
        """
        id: dupe
        name: Dupe
        version: "1.0.0"
        category: coding
        description: test
        template: "hello"
        """
    ).strip()
    (tmp_path / "a.yaml").write_text(content)
    (tmp_path / "b.yaml").write_text(content)

    with pytest.raises(PromptValidationError):
        PromptLibrary(tmp_path)


def test_invalid_id_case_rejected(tmp_path):
    (tmp_path / "bad.yaml").write_text(
        textwrap.dedent(
            """
            id: NotKebabCase
            name: Bad
            version: "1.0.0"
            category: coding
            description: test
            template: "hello"
            """
        ).strip()
    )
    with pytest.raises(PromptValidationError):
        PromptLibrary(tmp_path)
