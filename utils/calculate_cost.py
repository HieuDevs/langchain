from utils.constants import TOKEN_PRICES


# Function to calculate cost based on token usage and model
def calculate_cost(model_name, input_tokens, output_tokens):
    if model_name not in TOKEN_PRICES:
        raise ValueError(f"Model '{model_name}' is not supported.")
    input_cost = input_tokens * TOKEN_PRICES[model_name]["input"]
    output_cost = output_tokens * TOKEN_PRICES[model_name]["output"]
    total_cost = input_cost + output_cost
    return total_cost
