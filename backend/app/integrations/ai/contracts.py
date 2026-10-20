"""Provider-neutral contracts; no vendor SDK is selected here."""

from typing import Protocol, Sequence


class EmbeddingProvider(Protocol):
    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        """Return one vector per input text."""
        ...


class GenerationProvider(Protocol):
    def generate(self, prompt: str, *, context: Sequence[str]) -> str:
        """Generate from an already policy-approved prompt and context."""
        ...


class ClaimVerifier(Protocol):
    def verify(self, claim: str, *, evidence: Sequence[str]) -> str:
        """Return a domain verdict; execution errors must be raised separately."""
        ...
