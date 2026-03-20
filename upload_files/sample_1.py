def greet(name):
    """This function greets the user by their name."""
    return f"Hello, {name}!"


def multiply(a, b):
    """
    Multiply two numbers.

    Args:
        a (int): First number.
        b (int): Second number.

    Returns:
        int: Product of a and b.
    """
    return a * b
print(multiply(3, 5))




import math

def calculate_area(radius):
    # Calculate area without docstrings
    return math.pi * (radius ** 2)

# User input
r = float(input("Enter radius: "))
area = calculate_area(r)

print(f"Area: {round(area, 2)}")
