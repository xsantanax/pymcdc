# Extração de decisões
import ast

def extrair_decisoes(codigo: str):
    arvore = ast.parse(codigo)
    decisoes = []

    class VisitanteDecisao(ast.NodeVisitor):
        def visit_If(self, node):
            decisoes.append(ast.unparse(node.test))
            self.generic_visit(node)

    VisitanteDecisao().visit(arvore)
    print( "Decisões: ", decisoes)
    return decisoes

# Import code and test cases
from example import codigo

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
