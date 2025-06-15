codigo = '''
# def eh_bissexto(ano: int) -> bool:
#     if ano < 1 or ano > 9999:
#         raise ValueError("Ano inválido: deve estar entre 1 e 9999.")
#     if ano <= 1752:
#         return ano % 4 == 0
#     if ano % 400 == 0:
#         return True
#     if ano % 100 == 0:
#         return False
#     return ano % 4 == 0

def isValidPosition(x, y, z):
    if (x > 10 or y > 20) and z > 0:
        return True
    else:
        return False
''' 