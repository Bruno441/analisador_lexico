import re
from dataclasses import dataclass
from typing import Generator

@dataclass
class Token:
    tipo: str
    valor: str
    linha: int
    coluna: int
    
    def __str__(self):
        return f"Token({self.tipo}, '{self.valor}', {self.linha}:{self.coluna})"

TOKEN_SPECIFICATION = [
    ('COMENTARIO',   r'//[^\n]*'),           
    ('STRING',       r'"[^"\n]*"'),          
    ('FLOAT',        r'\d+\.\d+'),
    ('INT',          r'\d+'),
    ('ATRIB',        r'->'),
    ('OP_REL',       r'==|!=|<=|>=|<|>'),
    ('OP_ARIT',      r'\+|-|\*|/'),         
    ('PONTO_VIRG',   r';'),
    ('DOIS_PTS',     r':'),
    ('VIRGULA',      r','),
    ('ABRE_PAREN',   r'\('),
    ('FECHA_PAREN',  r'\)'),
    ('ABRE_CHAVE',   r'\{'),
    ('FECHA_CHAVE',  r'\}'),
    ('PALAVRACHAVE', r'\b(fnc|var|back|si|velsi|nisi|dum|per|Imp|fin)\b'),
    ('ID',           r'[a-zA-Z][a-zA-Z0-9_]*'), 
    ('NOVA_LINHA',   r'\n'),
    ('ESPACO',       r'[ \t]+'),
    ('MISMATCH',     r'.'),
]

REGEX_GERAL = '|'.join(f'(?P<{nome}>{padrao})' for nome, padrao in TOKEN_SPECIFICATION)

def tokenizar(codigo: str) -> Generator[Token, None, None]:
    linha = 1
    coluna = 1
    
    for match in re.finditer(REGEX_GERAL, codigo):
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
