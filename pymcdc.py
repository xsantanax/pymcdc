# -*- coding: utf-8 -*-
"""SSC5877_VV&T_trabalho_final.ipynb

# SSC5877 - Verificação, Validação e Teste de Software

## Trabalho final - Desafio

### Conceitos

#### O que é um ano bissexto?

Um ano bissexto é aquele que possui 366 dias ao invés de 365, com o dia extra sendo 29 de fevereiro. De acordo com as regras do calendário gregoriano (em vigor desde 1752), um ano é bissexto se:

*   For divisível por 4

*   Exceto se for divisível por 100

*   A menos que também seja divisível por 400

Além disso, anos anteriores a 1752 seguem uma lógica simplificada: são bissextos se forem divisíveis por 4.

#### O que é MC/DC?

MC/DC (Modified Condition/Decision Coverage) é um critério de teste que garante que:

*   Cada condição atômica em uma decisão (ex: a and b) foi avaliada como True e False;

*   Cada condição afeta isoladamente o resultado final da decisão.

### Funções

#### Bissexto
"""

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

"""#### Extração de decisões"""

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

codigo_eh_bissexto = '''
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

decisoes = extrair_decisoes(codigo_eh_bissexto)
for i, d in enumerate(decisoes, 1):
    print(f"Decisão {i}: {d}")

"""#### Geração de combinações MC/DC"""

import itertools

def gerar_mcdc(decisao):
    operadores_logicos = ["and", "or"]
    for operador in operadores_logicos:
        if operador in decisao:
            termos = [t.strip(" ()") for t in decisao.split(operador)]
            combinacoes = list(itertools.product([True, False], repeat=len(termos)))
            validas = []

            for i, c1 in enumerate(combinacoes):
                for j, c2 in enumerate(combinacoes):
                    if i >= j:
                        continue
                    difs = [k for k in range(len(c1)) if c1[k] != c2[k]]
                    if len(difs) == 1:
                        r1 = eval(f" {operador} ".join(str(v) for v in c1))
                        r2 = eval(f" {operador} ".join(str(v) for v in c2))
                        if r1 != r2:
                            validas.append((c1, r1))
                            validas.append((c2, r2))

            unicos = []
            for entrada in validas:
                if entrada not in unicos:
                    unicos.append(entrada)
            return termos, unicos

    return [decisao], [((True,), True), ((False,), False)]

for decisao in decisoes:
    termos, entradas = gerar_mcdc(decisao)
    print(f"Decisão: {decisao}")
    print("Combinações a validar (entrada -> saída):")
    for entrada, resultado in entradas:
        print(f"  {entrada} -> {resultado}")
    print()

"""#### Validação das combinações"""

def avaliar_entrada(ano, termos, operador):
    valores = [eval(t, {}, {"ano": ano}) for t in termos]
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

def verificar_cobertura_mcdc_real(decisoes, anos):
    print("Verificação da cobertura MC/DC com base nos anos testados:\n")

    for decisao in decisoes:
        termos, entradas_esperadas = gerar_mcdc(decisao)
        termos_completos, operador = extrair_termos_operador(decisao)

        entradas_reais = set()
        for ano in anos:
            try:
                valores, resultado = avaliar_entrada(ano, termos_completos, operador)
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

"""### Testes

#### Testes estáticos"""

anos = [-1, 1600, 1700, 1752, 1800, 1900, 2000, 2020, 2023, 10000]

print("Anos testados:")
print(anos)

print("-" * 40)

print("\nResultados dos testes:")
for ano in anos:
    try:
        resultado = eh_bissexto(ano)
        print(f"Ano {ano}: {'Bissexto' if resultado else 'Não bissexto'}")
    except ValueError as e:
        print(f"Ano {ano}: Erro - {e}")

print("-" * 40)

verificar_cobertura_mcdc_real(decisoes, anos)

"""#### Testes aleatórios"""

import random

anos = [random.randint(1, 9999) for _ in range(100)]

print("Anos testados:")
print(anos)

print("-" * 40)

print("\nResultados dos testes:")
for ano in anos:
    try:
        resultado = eh_bissexto(ano)
        print(f"Ano {ano}: {'Bissexto' if resultado else 'Não bissexto'}")
    except ValueError as e:
        print(f"Ano {ano}: Erro - {e}")

print("-" * 40)

verificar_cobertura_mcdc_real(decisoes, anos)

"""### Conclusões

***Adicionar as conclusões e as observações das implementações feitas***"""