# Define token prices for each model (USD per 1 million tokens)
token_prices = {
    "gpt-4o": {"input": 2.50 / 1_000_000, "output": 10.00 / 1_000_000},
    "gpt-4o-mini": {"input": 0.15 / 1_000_000, "output": 0.60 / 1_000_000},
    "gpt-3.5-turbo": {"input": 0.002 / 1_000_000, "output": 0.002 / 1_000_000},
    "o1-preview": {"input": 15.00 / 1_000_000, "output": 60.00 / 1_000_000},
    "o1-mini": {"input": 3.00 / 1_000_000, "output": 12.00 / 1_000_000},
}


# Function to calculate cost based on token usage and model
def calculate_cost(model_name, input_tokens, output_tokens):
    if model_name not in token_prices:
        raise ValueError(f"Model '{model_name}' is not supported.")
    input_cost = input_tokens * token_prices[model_name]["input"]
    output_cost = output_tokens * token_prices[model_name]["output"]
    total_cost = input_cost + output_cost
    return total_cost
