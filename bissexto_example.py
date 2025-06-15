# Example test cases for leap year calculation

# Static test cases
static_test_cases = [-1, 1600, 1700, 1752, 1800, 1900, 2000, 2020, 2023, 10000]

# Random test cases
import random
random_test_cases = [random.randint(1, 9999) for _ in range(100)]

# Example code for testing
codigo = '''
def eh_bissexto(ano: int) -> bool:
    if ano < 1 or ano > 9999:
        raise ValueError("Ano inválido: deve estar entre 1 e 9999.")
    if ano <= 1752:
        return ano % 4 == 0
    if ano % 400 == 0:
        return True
    if ano % 100 == 0:
        return False
    return ano % 4 == 0
''' 