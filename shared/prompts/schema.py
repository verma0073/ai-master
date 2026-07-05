"""
Schema definitions for the AI Master Prompt Library.

Design decision (documented, not hidden):
    Every prompt is a structured record, not a raw .txt file. A raw string
    has no machine-readable metadata: no way to know what variables it
    needs, which models it was validated against, or what "correct" output
    looks like. That makes prompts impossible to test, version, or reuse
    safely across projects. Treating prompts as validated data (like an API
    contract) is what makes this a "library" instead of a folder of notes.

Every prompt file is a YAML document validated against `PromptTemplate`
before it can be loaded or rendered. Invalid prompts fail at load time,
not at call time in production.
"""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


class VariableType(str, Enum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    LIST = "list"


class PromptVariable(BaseModel):
    """A single input the prompt template expects."""

    name: str = Field(..., description="Variable name as used in the template, e.g. 'code_snippet'")
    type: VariableType = VariableType.STRING
    required: bool = True
    description: str = ""
    default: Optional[Any] = None

    @field_validator("name")
    @classmethod
    def name_must_be_identifier(cls, v: str) -> str:
        if not v.isidentifier():
            raise ValueError(
                f"Variable name '{v}' must be a valid identifier (used directly in Jinja2 templates)"
            )
        return v


class PromptExample(BaseModel):
    """A worked example: proves the prompt actually renders and is useful."""

    inputs: dict[str, Any] = Field(default_factory=dict)
    expected_output_notes: str = Field(
        default="",
        description="Not the literal model output (that's non-deterministic) — "
        "notes on what a correct response should contain, used in tests as a sanity check.",
    )


class PromptTemplate(BaseModel):
    """Full metadata + content contract for one prompt."""

    id: str = Field(..., description="kebab-case unique identifier, e.g. 'code-review-strict'")
    name: str
    version: str = Field(..., description="Semantic version, e.g. '1.0.0'")
    category: str = Field(..., description="e.g. coding, writing, rag, agents")
    description: str
    tags: list[str] = Field(default_factory=list)
    model_compatibility: list[str] = Field(
        default_factory=lambda: ["gpt-4o", "claude-sonnet-4-6"],
        description="Models this prompt has been validated against",
    )
    variables: list[PromptVariable] = Field(default_factory=list)
    template: str = Field(..., description="Jinja2 template body")
    examples: list[PromptExample] = Field(default_factory=list)
    author: str = "Ravi Verma"
    created: Optional[date] = None
    notes: str = ""

    @field_validator("id")
    @classmethod
    def id_must_be_kebab_case(cls, v: str) -> str:
        if not v.replace("-", "").isalnum() or v != v.lower():
            raise ValueError(f"id '{v}' must be lowercase kebab-case, e.g. 'code-review-strict'")
        return v
