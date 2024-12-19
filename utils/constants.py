from enum import Enum

# Define token prices for each model (USD per 1 million tokens)
TOKEN_PRICES = {
    "gpt-4o": {"input": 2.50 / 1_000_000, "output": 10.00 / 1_000_000},
    "gpt-4o-mini": {"input": 0.15 / 1_000_000, "output": 0.60 / 1_000_000},
    "gpt-3.5-turbo": {"input": 0.002 / 1_000_000, "output": 0.002 / 1_000_000},
    "o1-preview": {"input": 15.00 / 1_000_000, "output": 60.00 / 1_000_000},
    "o1-mini": {"input": 3.00 / 1_000_000, "output": 12.00 / 1_000_000},
}


class ModelProviders(Enum):
    OPEN_AI = ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo", "o1-preview", "o1-mini"]
    ANTHROPIC = [
        "claude-3-5-sonnet-20240620",
        "claude-3-5-sonnet-20240229",
        "claude-3-5-sonnet-20240229",
    ]
    GOOGLE = ["gemini-1.5-flash-002", "gemini-1.5-pro-002"]
