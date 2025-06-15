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
    return decisoes

# Import code
from example import codigo

# Extract and print decisions
decisoes = extrair_decisoes(codigo)
for i, d in enumerate(decisoes, 1):
    print(f"Decisão {i}: {d}")
