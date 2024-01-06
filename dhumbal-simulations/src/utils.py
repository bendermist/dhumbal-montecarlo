def calculate_average(data):
    """Calculate the average of a list of numbers."""
    return sum(data) / len(data)

def calculate_variance(data):
    """Calculate the variance of a list of numbers."""
    mean = calculate_average(data)
    return sum((x - mean) ** 2 for x in data) / len(data)