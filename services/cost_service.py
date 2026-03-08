def estimate_cost(tokens: int) -> float:
    """
    Estimate cost for OpenAI API usage based on tokens.
    
    GPT-4o-mini pricing (as of 2024):
    - Input: $0.150 per 1M tokens
    - Output: $0.600 per 1M tokens
    - Average: ~$0.150 per 1M tokens (simplified calculation)
    
    Args:
        tokens: Total number of tokens used (input + output)
        
    Returns:
        Estimated cost in USD
    """
    cost_per_1k_tokens = 0.00015  # $0.15 per 1M tokens = $0.00015 per 1K tokens
    cost = (tokens / 1000) * cost_per_1k_tokens
    return round(cost, 6)  # Round to 6 decimal places
