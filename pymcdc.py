"""#### Extração de decisões"""
import ast
import inspect

def extrair_decisoes(codigo: str):
    arvore = ast.parse(codigo)
    decisoes = []

    class VisitanteDecisao(ast.NodeVisitor):
        def visit_If(self, node):
            decisoes.append(ast.unparse(node.test))
            self.generic_visit(node)

    VisitanteDecisao().visit(arvore)
    return decisoes

# Import test cases from example.py
from example import static_test_cases, random_test_cases, codigo

# Extract function name and parameters from the code
tree = ast.parse(codigo)
function_def = next(node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef))
function_name = function_def.name
function_params = [arg.arg for arg in function_def.args.args]

# Create a namespace to execute the code
namespace = {}
exec(codigo, namespace)
function = namespace[function_name]

decisoes = extrair_decisoes(codigo)
for i, d in enumerate(decisoes, 1):
    print(f"Decisão {i}: {d}")

"""#### Geração de combinações MC/DC"""

import itertools

def gerar_mcdc(decisao):
    # Parse the decision into an AST to handle complex conditions
    try:
        tree = ast.parse(decisao, mode='eval')
    except SyntaxError:
        # If it's a simple condition without operators, return it as is
        return [decisao], [((True,), True), ((False,), False)]

    # Extract all atomic conditions
    termos = []
    operadores = []
    
    class VisitanteCondicao(ast.NodeVisitor):
        def visit_BoolOp(self, node):
            # Record the operator
            if isinstance(node.op, ast.And):
                operadores.append('and')
            elif isinstance(node.op, ast.Or):
                operadores.append('or')
            self.generic_visit(node)
            
        def visit_Compare(self, node):
            # Extract the comparison as a single condition
            termos.append(ast.unparse(node))
            
        def visit_Name(self, node):
            # Handle simple boolean variables
            if node.id not in termos:
                termos.append(node.id)

    VisitanteCondicao().visit(tree)
    
    if not termos:
        # If no terms were found, treat the whole expression as one term
        return [decisao], [((True,), True), ((False,), False)]

    # Generate all possible combinations
    combinacoes = list(itertools.product([True, False], repeat=len(termos)))
    validas = []

    # For each term, find pairs where only that term changes and the result changes
    for i in range(len(termos)):
        for c1 in combinacoes:
            for c2 in combinacoes:
                # Check if only one term changed
                if sum(1 for a, b in zip(c1, c2) if a != b) != 1:
                    continue
                # Check if the changed term is the one we're testing
                if c1[i] == c2[i]:
                    continue
                
                # Create a namespace with the values
                namespace = dict(zip(termos, c1))
                try:
                    # Create a safe evaluation environment
                    safe_dict = {"__builtins__": {}}
                    safe_dict.update(namespace)
                    r1 = eval(decisao, safe_dict)
                except:
                    continue
                    
                namespace = dict(zip(termos, c2))
                try:
                    safe_dict = {"__builtins__": {}}
                    safe_dict.update(namespace)
                    r2 = eval(decisao, safe_dict)
                except:
                    continue
                
                # Check if the result changed
                if r1 != r2:
                    validas.append((c1, r1))
                    validas.append((c2, r2))

    # Remove duplicates while preserving order
    unicos = []
    for entrada in validas:
        if entrada not in unicos:
            unicos.append(entrada)

    # If no valid combinations were found, return basic True/False cases
    if not unicos:
        return termos, [((True,) * len(termos), True), ((False,) * len(termos), False)]

    return termos, unicos

# Print the MC/DC combinations in a more readable format
for decisao in decisoes:
    termos, entradas = gerar_mcdc(decisao)
    print(f"\nDecisão: {decisao}")
    print("Termos:", ", ".join(termos))
    print("Combinações MC/DC (entrada -> saída):")
    for entrada, resultado in entradas:
        # Create a mapping of terms to their values for better readability
        term_values = dict(zip(termos, entrada))
        print(f"  {term_values} -> {resultado}")
    print()

"""
# Commented out test-related code for now

def avaliar_entrada(args, termos, operador):
    # Create a namespace with the function parameters
    namespace = dict(zip(function_params, args))
    valores = [eval(t, {}, namespace) for t in termos]
    if operador:
        resultado = eval(f" {operador} ".join(str(v) for v in valores))
    else:
        resultado = valores[0]
    return tuple(valores), resultado

def extrair_termos_operador(decisao):
    if " and " in decisao:
        return [t.strip() for t in decisao.split("and")], "and"
    elif " or " in decisao:
        return [t.strip() for t in decisao.split("or")], "or"
    else:
        return [decisao.strip()], None

def verificar_cobertura_mcdc_real(decisoes, test_cases):
    print("Verificação da cobertura MC/DC com base nos casos testados:\n")

    for decisao in decisoes:
        termos, entradas_esperadas = gerar_mcdc(decisao)
        termos_completos, operador = extrair_termos_operador(decisao)

        entradas_reais = set()
        for args in test_cases:
            try:
                valores, resultado = avaliar_entrada(args, termos_completos, operador)
                entradas_reais.add((valores, resultado))
            except Exception:
                continue

        total = len(entradas_esperadas)
        cobertas = 0
        faltando = []

        for entrada, saida in entradas_esperadas:
            if (entrada, saida) in entradas_reais:
                cobertas += 1
            else:
                faltando.append((entrada, saida))

        print(f"Decisão: {decisao}")
        print("Combinações necessárias:")
        for e, r in entradas_esperadas:
            print(f"  {e} -> {r}")
        print(f"Cobertura atingida: {cobertas}/{total}")

        if cobertas == total:
            print("Cobertura MC/DC completa\n")
        else:
            print("Cobertura MC/DC incompleta")
            print("Faltando as combinações:")
            for e, r in faltando:
                print(f"  {e} -> {r}")
            print()

print("Casos de teste:")
for args in static_test_cases:
    print(f"{', '.join(f'{p}={v}' for p, v in zip(function_params, args))}")

print("-" * 40)

print("\nResultados dos testes:")
for args in static_test_cases:
    try:
        resultado = function(*args)
        print(f"{function_name}({', '.join(str(v) for v in args)}): {'Válido' if resultado else 'Inválido'}")
    except Exception as e:
        print(f"{function_name}({', '.join(str(v) for v in args)}): Erro - {e}")

print("-" * 40)

verificar_cobertura_mcdc_real(decisoes, static_test_cases)

print("Casos de teste:")
for args in random_test_cases:
    print(f"{', '.join(f'{p}={v}' for p, v in zip(function_params, args))}")

print("-" * 40)

print("\nResultados dos testes:")
for args in random_test_cases:
    try:
        resultado = function(*args)
        print(f"{function_name}({', '.join(str(v) for v in args)}): {'Válido' if resultado else 'Inválido'}")
    except Exception as e:
        print(f"{function_name}({', '.join(str(v) for v in args)}): Erro - {e}")

print("-" * 40)

verificar_cobertura_mcdc_real(decisoes, random_test_cases)
"""