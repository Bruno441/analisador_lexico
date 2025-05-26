from analisador_lexico import tokenizar, Token
#from analisador_sintatico import analisar_sintatico  # Descomente quando implementar

def imprimir_tokens(tokens):
    for token in tokens:
        print(token)

def main():
    codigo_exemplo = 'fnc soma (a, b) { var: res -> a + b; back res; }'
    tokens = list(tokenizar(codigo_exemplo))
    imprimir_tokens(tokens)
    # Quando implementar o sintático:
    # arvore = analisar_sintatico(tokens)
    # print(arvore)

if __name__ == '__main__':
    main()
