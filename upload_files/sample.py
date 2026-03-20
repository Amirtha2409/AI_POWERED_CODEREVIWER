def square(n):
    '''Take a number n and return the square of n.'''
    return n**2

print(square.__doc__)



def add_binary(a, b):
    '''
    Return the sum of two decimal numbers in binary digits.

            Parameters:
                    a (int): A decimal integer
                    b (int): Another decimal integer

            Returns:
                    binary_sum (str): Binary string of the sum of a and b
    '''
    binary_sum = bin(a+b)[2:]
    return binary_sum


print(add_binary.__doc__)