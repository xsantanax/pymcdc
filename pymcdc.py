# Extração de decisões
import ast

def extrair_decisoes(codigo: str):
    arvore = ast.parse(codigo)
    print(ast.dump(arvore, indent=4))

    decisoes = []

    class VisitanteDecisao(ast.NodeVisitor):
        def visit_If(self, node):
            decisoes.append(ast.unparse(node.test))
            self.generic_visit(node)

    VisitanteDecisao().visit(arvore)
    return decisoes

# Import code
from example import codigo

# Extract and print decisions
decisoes = extrair_decisoes(codigo)
for i, d in enumerate(decisoes, 1):
    print(f"Decisão {i}: {d}")



# Geração de combinações MC/DC
import itertools

def gerar_mcdc(decisao):
    # Parse the decision into an AST to handle complex conditions
    try:
        tree = ast.parse(decisao, mode='eval')
    except SyntaxError:
        # If it's a simple condition without operators, return it as is
        return [decisao], [((True,), True), ((False,), False)]

    print(ast.dump(tree, indent=4))

    # Extract all atomic conditions
    termos = []
    operadores = []
    
#     class VisitanteCondicao(ast.NodeVisitor):
#         def visit_BoolOp(self, node):
#             # Record the operator
#             if isinstance(node.op, ast.And):
#                 operadores.append('and')
#             elif isinstance(node.op, ast.Or):
#                 operadores.append('or')
#             self.generic_visit(node)
            
#         def visit_Compare(self, node):
#             # Extract the comparison as a single condition
#             termos.append(ast.unparse(node))
            
#         def visit_Name(self, node):
#             # Handle simple boolean variables
#             if node.id not in termos:
#                 termos.append(node.id)

#     VisitanteCondicao().visit(tree)
    
#     if not termos:
#         # If no terms were found, treat the whole expression as one term
#         return [decisao], [((True,) * len(termos), True), ((False,) * len(termos), False)]

#     # Generate all possible combinations
#     combinacoes = list(itertools.product([True, False], repeat=len(termos)))
#     validas = []

#     # For each term, find pairs where only that term changes and the result changes
#     for i in range(len(termos)):
#         for c1 in combinacoes:
#             for c2 in combinacoes:
#                 # Check if only one term changed
#                 if sum(1 for a, b in zip(c1, c2) if a != b) != 1:
#                     continue
#                 # Check if the changed term is the one we're testing
#                 if c1[i] == c2[i]:
#                     continue
                
#                 # Create a namespace with the values
#                 namespace = dict(zip(termos, c1))
#                 try:
#                     # Create a safe evaluation environment
#                     safe_dict = {"__builtins__": {}}
#                     safe_dict.update(namespace)
#                     r1 = eval(decisao, safe_dict)
#                 except:
#                     continue
                    
#                 namespace = dict(zip(termos, c2))
#                 try:
#                     safe_dict = {"__builtins__": {}}
#                     safe_dict.update(namespace)
#                     r2 = eval(decisao, safe_dict)
#                 except:
#                     continue
                
#                 # Check if the result changed
#                 if r1 != r2:
#                     validas.append((c1, r1))
#                     validas.append((c2, r2))

#     # Remove duplicates while preserving order
    unicos = []
#     for entrada in validas:
#         if entrada not in unicos:
#             unicos.append(entrada)

#     # If no valid combinations were found, return basic True/False cases
#     if not unicos:
#         return termos, [((True,) * len(termos), True), ((False,) * len(termos), False)]

    return termos, unicos

# Print the MC/DC combinations in a more readable format
decisionIndex = 1
for decisao in decisoes:
    termos, entradas = gerar_mcdc(decisao)
    print(f"\nDecisão {decisionIndex}: {decisao}")
    print("Termos:", ", ".join(termos))
    print("Combinações MC/DC (entrada -> saída):")
    for entrada, resultado in entradas:
        # Create a mapping of terms to their values for better readability
        term_values = dict(zip(termos, entrada))
        print(f"  {term_values} -> {resultado}")
    print()
    decisionIndex+=1




# def avaliar_entrada(args, termos, operador):
#     # Create a namespace with the function parameters
#     namespace = dict(zip(function_params, args))
#     valores = [eval(t, {}, namespace) for t in termos]
#     if operador:
#         resultado = eval(f" {operador} ".join(str(v) for v in valores))
#     else:
#         resultado = valores[0]
#     return tuple(valores), resultado

# def extrair_termos_operador(decisao):
#     if " and " in decisao:
#         return [t.strip() for t in decisao.split("and")], "and"
#     elif " or " in decisao:
#         return [t.strip() for t in decisao.split("or")], "or"
#     else:
#         return [decisao.strip()], None
