from enum import Enum

# Define token prices for each model (USD per 1K tokens)
TOKEN_PRICES = {
    # OpenAI Models
    "o1-preview": {"input": 0.015, "output": 0.06},
    "o1-mini": {"input": 0.003, "output": 0.012},
    "o1-preview-completion": {"input": 0.0006, "output": 0.0024},
    "gpt-4o": {"input": 0.0025, "output": 0.01},
    "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
    "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
    "gpt-3.5-turbo-16k": {"input": 0.003, "output": 0.004},
    "gpt-3.5-turbo-instruct": {"input": 0.0015, "output": 0.002},
    # Gemini Models
    "gemini-1.5-flash": {"input": 0.000075, "output": 0.00030},
    "gemini-1.5-flash-8b": {"input": 0.00004, "output": 0.00015},
    "gemini-1.5-pro": {"input": 0.00035, "output": 0.00105},
    "gemini-1.0-pro": {"input": 0.00005, "output": 0.00015},
    # Claude Models
    "claude-3-5-sonnet-20241022": {"input": 0.003, "output": 0.015},
    "claude-3-opus-20240229": {"input": 0.015, "output": 0.075},
    "claude-3-sonnet-20240229": {"input": 0.003, "output": 0.015},
    "claude-3-haiku-20240307": {"input": 0.00025, "output": 0.00125},
}


class ModelProviders(Enum):
    OPEN_AI = [
        # "o1-preview",
        # "o1-mini",
        # "o1-preview-completion",
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-16k",
        "gpt-3.5-turbo-instruct",
    ]
    GOOGLE = [
        "gemini-1.5-flash",
        "gemini-1.5-flash-8b",
        "gemini-1.5-pro",
        "gemini-1.0-pro",
    ]
    ANTHROPIC = [
        "claude-3-5-sonnet-20241022",
        "claude-3-opus-20240229",
        "claude-3-sonnet-20240229",
        "claude-3-haiku-20240307",
    ]
