"""
PromptLibrary: loads, validates, versions, and renders prompt templates.

Design decisions (why, not just how):

1. Fail fast at load time, not render time.
   Every YAML file is parsed and validated against `PromptTemplate` when the
   library is constructed. A malformed prompt breaks startup, not a random
   production request three weeks from now.

2. StrictUndefined rendering.
   The naive approach is `template.format(**kwargs)` or Jinja2 with default
   (silent) undefined handling. Both quietly render blank/garbage text if a
   variable is missing or misspelled — the worst possible failure mode for
   a prompt, because the LLM will confidently answer a broken instruction
   and nobody notices until output quality degrades. This library uses
   Jinja2's StrictUndefined so a missing variable raises immediately.

3. (id, version) is the real primary key, not just id.
   Prompts change behavior over time. Pinning a specific version is how you
   get reproducible outputs — the same guarantee you'd want from a pinned
   package dependency. `get()` without a version returns the latest by
   semantic version, but callers that care about reproducibility (e.g. an
   eval suite) should always pin a version explicitly.
"""

from __future__ import annotations

from pathlib import Path

import yaml
from jinja2 import Environment, StrictUndefined, UndefinedError
from pydantic import ValidationError

from .schema import PromptTemplate


class PromptNotFoundError(KeyError):
    pass


class PromptValidationError(ValueError):
    pass


class PromptRenderError(ValueError):
    pass


def _version_key(version: str) -> tuple[int, ...]:
    """Sort semantic versions ('1.10.0' > '1.9.0'), falling back gracefully."""
    parts = []
    for p in version.split("."):
        try:
            parts.append(int(p))
        except ValueError:
            parts.append(0)
    return tuple(parts)


class PromptLibrary:
    def __init__(self, root_dir: str | Path):
        self.root_dir = Path(root_dir)
        if not self.root_dir.exists():
            raise FileNotFoundError(f"Prompt directory does not exist: {self.root_dir}")

        self._env = Environment(undefined=StrictUndefined, autoescape=False)
        # keyed by id -> {version: PromptTemplate}
        self._prompts: dict[str, dict[str, PromptTemplate]] = {}
        self._load_all()

    # ------------------------------------------------------------------ #
    # Loading
    # ------------------------------------------------------------------ #
    def _load_all(self) -> None:
        yaml_files = sorted(self.root_dir.rglob("*.yaml")) + sorted(self.root_dir.rglob("*.yml"))
        if not yaml_files:
            raise FileNotFoundError(f"No prompt YAML files found under {self.root_dir}")

        for path in yaml_files:
            raw = yaml.safe_load(path.read_text(encoding="utf-8"))
            try:
                prompt = PromptTemplate(**raw)
            except ValidationError as e:
                raise PromptValidationError(f"Invalid prompt file {path}:\n{e}") from e

            versions = self._prompts.setdefault(prompt.id, {})
            if prompt.version in versions:
                raise PromptValidationError(
                    f"Duplicate id+version '{prompt.id}@{prompt.version}' "
                    f"(conflict: {path} vs an already-loaded file)"
                )
            versions[prompt.version] = prompt

    def reload(self) -> None:
        self._prompts.clear()
        self._load_all()

    # ------------------------------------------------------------------ #
    # Retrieval
    # ------------------------------------------------------------------ #
    def get(self, prompt_id: str, version: str | None = None) -> PromptTemplate:
        versions = self._prompts.get(prompt_id)
        if not versions:
            raise PromptNotFoundError(f"No prompt with id '{prompt_id}'")

        if version is not None:
            if version not in versions:
                available = ", ".join(sorted(versions, key=_version_key))
                raise PromptNotFoundError(
                    f"Prompt '{prompt_id}' has no version '{version}'. Available: {available}"
                )
            return versions[version]

        latest_version = max(versions, key=_version_key)
        return versions[latest_version]

    def list(self, category: str | None = None, tag: str | None = None) -> list[PromptTemplate]:
        results = [self.get(pid) for pid in self._prompts]  # latest version of each
        if category:
            results = [p for p in results if p.category == category]
        if tag:
            results = [p for p in results if tag in p.tags]
        return sorted(results, key=lambda p: p.id)

    def search(self, query: str) -> list[PromptTemplate]:
        q = query.lower()
        return [
            p
            for p in self.list()
            if q in p.name.lower() or q in p.description.lower() or any(q in t.lower() for t in p.tags)
        ]

    # ------------------------------------------------------------------ #
    # Rendering
    # ------------------------------------------------------------------ #
    def render(self, prompt_id: str, version: str | None = None, **kwargs) -> str:
        prompt = self.get(prompt_id, version)

        provided = set(kwargs)
        required = {v.name for v in prompt.variables if v.required}
        missing = required - provided
        if missing:
            raise PromptRenderError(
                f"Missing required variable(s) for '{prompt_id}': {sorted(missing)}"
            )

        # apply defaults for optional variables the caller didn't supply
        render_vars = dict(kwargs)
        for var in prompt.variables:
            if var.name not in render_vars and var.default is not None:
                render_vars[var.name] = var.default

        try:
            template = self._env.from_string(prompt.template)
            return template.render(**render_vars).strip()
        except UndefinedError as e:
            raise PromptRenderError(f"Template for '{prompt_id}' references an undefined variable: {e}") from e
