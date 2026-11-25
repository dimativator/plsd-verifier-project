"""Explicit, source-dated API prices and candidates from a live model inventory.

The models endpoint establishes availability, not capability or price. Prices
must be supplied from a saved official source; this module has no guessed rates.
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable, Mapping


@dataclass(frozen=True)
class FrozenPrice:
    model: str
    input_per_million: str
    cached_input_per_million: str | None
    output_per_million: str
    source_url: str
    checked_at: str
    cache_write_per_million: str | None = None

    def __post_init__(self) -> None:
        if not self.model or not self.source_url.startswith("https://") or not self.checked_at:
            raise ValueError("A model and dated HTTPS pricing source are required")
        if Decimal(self.input_per_million) <= 0 or Decimal(self.output_per_million) <= 0:
            raise ValueError("Input and output prices must be positive")
        if self.cached_input_per_million is not None and Decimal(self.cached_input_per_million) < 0:
            raise ValueError("Cached input price must be nonnegative")
        if self.cached_input_per_million is not None and Decimal(
            self.cached_input_per_million
        ) > Decimal(self.input_per_million):
            raise ValueError("Cached input cannot exceed the uncached reservation rate")
        if self.cache_write_per_million is not None and Decimal(
            self.cache_write_per_million
        ) < Decimal(self.input_per_million):
            raise ValueError("Cache-write reservation rate cannot be below uncached input")

    def maximum_cost(self, input_tokens: int, output_tokens: int) -> Decimal:
        if input_tokens < 0 or output_tokens < 0:
            raise ValueError("Token counts must be nonnegative")
        return (
            Decimal(input_tokens) * Decimal(self.cache_write_per_million or self.input_per_million)
            + Decimal(output_tokens) * Decimal(self.output_per_million)
        ) / Decimal(1_000_000)

    def actual_cost(self, usage: Mapping) -> Decimal:
        given, generated = usage.get("input_tokens"), usage.get("output_tokens")
        cached = (usage.get("input_tokens_details") or {}).get("cached_tokens", 0)
        if any(
            not isinstance(n, int) or isinstance(n, bool) or n < 0
            for n in (given, generated, cached)
        ):
            raise ValueError("Response must include nonnegative input/output/cache token counts")
        if cached > given:
            raise ValueError("Cached tokens exceed input tokens")
        if cached and self.cached_input_per_million is None:
            raise ValueError("Official cached-input pricing is missing")
        details = usage.get("input_tokens_details") or {}
        write_counts = [
            details[key]
            for key in ("cache_write_tokens", "cache_creation_tokens")
            if key in details
        ]
        if write_counts and any(value != write_counts[0] for value in write_counts):
            raise ValueError("Conflicting cache-write token counts")
        if self.cache_write_per_million is not None and not write_counts:
            raise ValueError("Response omits cache-write usage required for exact pricing")
        written = write_counts[0] if write_counts else 0
        if (
            not isinstance(written, int)
            or isinstance(written, bool)
            or written < 0
            or written + cached > given
        ):
            raise ValueError("Invalid cache-write token count")
        if written and self.cache_write_per_million is None:
            raise ValueError("Official cache-write pricing is missing")
        cached_rate = Decimal(self.cached_input_per_million or "0")
        return (
            Decimal(given - cached - written) * Decimal(self.input_per_million)
            + Decimal(cached) * cached_rate
            + Decimal(written) * Decimal(self.cache_write_per_million or self.input_per_million)
            + Decimal(generated) * Decimal(self.output_per_million)
        ) / Decimal(1_000_000)

    def accounted_cost(self, usage: Mapping) -> tuple[Decimal, str]:
        """Use a labelled upper bound if cache-write counts are not reported."""
        details = usage.get("input_tokens_details") or {}
        if self.cache_write_per_million is not None and not any(
            key in details for key in ("cache_write_tokens", "cache_creation_tokens")
        ):
            bounded = dict(usage)
            copied = dict(details)
            given, cached = usage.get("input_tokens"), details.get("cached_tokens", 0)
            if (
                not isinstance(given, int)
                or isinstance(given, bool)
                or not isinstance(cached, int)
                or isinstance(cached, bool)
            ):
                raise ValueError("Response omits valid input/cache usage")
            copied["cache_write_tokens"] = given - cached
            bounded["input_tokens_details"] = copied
            return self.actual_cost(bounded), "upper_bound_unreported_cache_writes"
        return self.actual_cost(usage), "usage_derived"


# Frozen standard-service prices verified from saved official pages on this date.
# Long-context requests are rejected by the transport, so their multipliers do
# not apply. Cache-write reservations use the documented 1.25x input rate.
CALIBRATION_PRICES = {
    "gpt-5.6-luna": FrozenPrice(
        "gpt-5.6-luna",
        ".20",
        ".02",
        "1.20",
        "https://developers.openai.com/api/docs/models/gpt-5.6-luna",
        "2026-11-23",
        ".25",
    ),
    "gpt-6-luna": FrozenPrice(
        "gpt-6-luna",
        ".10",
        ".01",
        ".50",
        "https://developers.openai.com/api/docs/models/gpt-6-luna",
        "2026-11-23",
        ".125",
    ),
    "gpt-6.1-sol": FrozenPrice(
        "gpt-6.1-sol",
        "2",
        ".10",
        "10",
        "https://developers.openai.com/api/docs/pricing",
        "2026-11-23",
        "2.5",
    ),
}


def model_ids(payload: Mapping) -> list[str]:
    """Return only IDs actually present in a /v1/models response."""
    return sorted(
        {
            row["id"]
            for row in payload.get("data", [])
            if isinstance(row, dict) and isinstance(row.get("id"), str)
        }
    )


def economical_candidates(
    available: Iterable[str],
    prices: Mapping[str, FrozenPrice],
    limit: int = 6,
    input_tokens: int = 10_000,
    output_tokens: int = 4_000,
) -> list[str]:
    """Rank available, explicitly priced IDs by a stated screening workload.

    A caller must separately confirm Responses/text/reasoning compatibility.
    In particular, membership of /models is not a capability test.
    """
    if limit < 1:
        raise ValueError("limit must be positive")
    return sorted(
        set(available) & prices.keys(),
        key=lambda name: (prices[name].maximum_cost(input_tokens, output_tokens), name),
    )[:limit]
