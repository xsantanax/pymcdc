# Example test cases for position validation

# Static test cases
static_test_cases = [
    (5, 15, 1),    # Valid position
    (15, 10, 1),   # Valid position (x > 10)
    (5, 25, 1),    # Valid position (y > 20)
    (15, 25, 1),   # Valid position (both x > 10 and y > 20)
    (5, 15, 0),    # Invalid position (z <= 0)
    (15, 25, 0),   # Invalid position (z <= 0)
    (5, 15, -1),   # Invalid position (z <= 0)
]

# Random test cases
import random
random_test_cases = [
    (random.randint(0, 20), random.randint(0, 30), random.randint(-5, 5))
    for _ in range(100)
]

# Example code for testing
codigo = '''
def isValidPosition(x, y, z):
    if (x > 10 or y > 20) and z > 0:
        return True
    else:
        return False
''' 