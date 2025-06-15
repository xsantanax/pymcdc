# Test cases for various examples

# Position validation test cases
position_static_test_cases = [
    (5, 15, 1),    # Valid position
    (15, 10, 1),   # Valid position (x > 10)
    (5, 25, 1),    # Valid position (y > 20)
    (15, 25, 1),   # Valid position (both x > 10 and y > 20)
    (5, 15, 0),    # Invalid position (z <= 0)
    (15, 25, 0),   # Invalid position (z <= 0)
    (5, 15, -1),   # Invalid position (z <= 0)
]

# Random position test cases
import random
position_random_test_cases = [
    (random.randint(0, 20), random.randint(0, 30), random.randint(-5, 5))
    for _ in range(100)
]

# Leap year test cases
leap_year_static_test_cases = [-1, 1600, 1700, 1752, 1800, 1900, 2000, 2020, 2023, 10000]

# Random leap year test cases
leap_year_random_test_cases = [random.randint(1, 9999) for _ in range(100)] 