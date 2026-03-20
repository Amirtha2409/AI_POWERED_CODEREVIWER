def calculate_area(length, width):
    """
    Calculates the area of a rectangle.

    This function takes the length and the width of a rectangle
    as input and returns the calculated area.

    Args:
        length (float): The length of the rectangle.
        width (float): The width of the rectangle.

    Returns:
        float: The area of the rectangle.
    """
    return length * width

def evenOdd(x):
    if (x % 2 == 0):
        return "Even"
    else:
        return "Odd"

print(evenOdd(16))
print(evenOdd(7))

def cube(x): return x*x*x   # without lambda
cube_l = lambda x : x*x*x  # with lambda

print(cube(7))
print(cube_l(7))



def factorial(n):
    if n == 0:  
        return 1
    else:
        return n * factorial(n - 1) 
      
print(factorial(4))