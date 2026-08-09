"""Typed result object shared by Lite analytics."""

from dataclasses import dataclass, field
from typing import Final

MODEL_VERSION: Final[str] = "ta35-lite-1.5"


@dataclass(frozen=True, slots=True)
class ScalarResult:
    value: float | None
    model_version: str = MODEL_VERSION
    quality_flags: tuple[str, ...] = field(default_factory=tuple)

    @property
    def is_valid(self) -> bool:
        return self.value is not None and not any(
            flag.startswith(("invalid_", "insufficient_"))
            for flag in self.quality_flags
        )
