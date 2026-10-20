"""Provider-neutral contracts for embedding, generation, and verification.

Retrieval sends chunk text to an embedding implementation; answer generation
receives only policy-approved evidence; claim verification independently checks
claims against evidence. Implementations must enforce outbound-data policy and
must not let vendor-specific types leak into domain or API code.
"""

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
