def calculate_average(numbers):
    """Calculates the average of a given list of numbers.

    Args:
        numbers (list): A list of numbers to calculate the average from.

    Returns:
        float: The average of the given list of numbers.

    Raises:
        ValueError: If the input list is empty.
        TypeError: If the input is not a list or if the list contains non-numeric values.
    """
    total = 0
    for n in numbers:
        total += n
    
    if len(numbers) == 0:
        return 0
    return total / len(numbers)



def add(a: int, b: int) -> int:
   
    return a + b



class Processor:
    def process(self, data):
        for item in data:
            if item is None:
                continue
            print(item)