import re
from dataclasses import dataclass

@dataclass
class Token:
    tipo: str      
    valor: str     
    linha: int     
    coluna: int    

token_specification = [
    ('COMENTARIO',   r'//[^\n]*'),                        # Comentário de linha
    ('STRING',       r'"[^"\n]*"'),                       # Strings entre aspas
    ('FLOAT',        r'\d+\.\d+'),                        # Números decimais
    ('INT',          r'\d+'),                             # Números inteiros
    ('ATRIB',        r'->'),                              # Atribuição
    ('OP_REL',       r'==|!=|<=|>=|<|>'),                 # Operadores relacionais
    ('OP_ARIT',      r'\+|-|\*|/'),                       # Operadores aritméticos
    ('PONTO_VIRG',   r';'),                               # Ponto e vírgula
    ('VIRGULA',      r','),                               # Vírgula
    ('ABRE_PAREN',   r'\('),                              # (
    ('FECHA_PAREN',  r'\)'),                              # )
    ('PALAVRA_CHAVE', r'\b(fnc|var:|back|si|velsi|nisi|dum|per|Imp|fin)\b'),  # Palavras-chave
    ('ID',           r'[a-zA-Z_][a-zA-Z0-9_]*'),          # Identificadores
    ('NOVA_LINHA',   r'\n'),                              # Quebra de linha
    ('ESPACO',       r'[ \t]+'),                          # Espaços e tabs
    ('MISMATCH',     r'.'),                               # Qualquer coisa inválida
]

regex_geral = '|'.join(f'(?P<{nome}>{padrao})' for nome, padrao in token_specification)

def analisar_codigo(codigo):
    linha = 1
    coluna = 1
    for match in re.finditer(regex_geral, codigo):
        tipo = match.lastgroup
        valor = match.group()
        if tipo == 'NOVA_LINHA':
            linha += 1
            coluna = 1
        elif tipo in ('ESPACO', 'COMENTARIO'):
            coluna += len(valor)
            continue
        elif tipo == 'MISMATCH':
            raise SyntaxError(f'Token inválido "{valor}" na linha {linha}, coluna {coluna}')
        else:
            yield Token(tipo, valor, linha, coluna)
            coluna += len(valor)

# Teste básico
if __name__ == '__main__':
    codigo_exemplo = 'fnc soma (a, b) { var: res -> a + b; back res; }'
    for token in analisar_codigo(codigo_exemplo):
        print(token)
