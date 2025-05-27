from analisador_lexico import Token
from typing import List, Optional, Dict, Any

class Parser:
    
    def __init__(self, tokens: List[Token]):
        self.tokens = [t for t in tokens if t.tipo != 'NOVA_LINHA'] 
        self.pos = 0
        self.token_atual = self.tokens[self.pos] if self.tokens else None
        self.arvore_sintatica = []
    
    def consumir(self, tipo_esperado: str) -> Token:
        if self.token_atual and self.token_atual.tipo == tipo_esperado:
            token = self.token_atual
            self.avancar()
            return token
        else:
            tipo_atual = self.token_atual.tipo if self.token_atual else "EOF"
            self.erro(f"Esperado token '{tipo_esperado}', mas encontrado '{tipo_atual}'")
    
    def avancar(self):
        self.pos += 1
        self.token_atual = self.tokens[self.pos] if self.pos < len(self.tokens) else None
    
    def erro(self, mensagem: str):
        if self.token_atual:
            raise SyntaxError(f"[Linha {self.token_atual.linha}] {mensagem}")
        else:
            raise SyntaxError(f"[Fim do arquivo] {mensagem}")
    
    def analisar(self) -> List[Dict[str, Any]]:
        while self.token_atual:
            if self.token_atual.valor == 'fnc':
                self.arvore_sintatica.append(self.funcao())
            elif self.token_atual.valor == 'var:':
                self.arvore_sintatica.append(self.declaracao_variavel())
            else:
                self.erro(f"Declaração inválida iniciada com '{self.token_atual.valor}'")
        
        return self.arvore_sintatica
    
    def funcao(self) -> Dict[str, Any]:
        self.consumir('PALAVRACHAVE')  
        nome = self.consumir('ID')
        self.consumir('ABRE_PAREN')
        
        parametros = []
        while self.token_atual and self.token_atual.tipo != 'FECHA_PAREN':
            parametros.append(self.consumir('ID').valor)
            if self.token_atual and self.token_atual.tipo == 'VIRGULA':
                self.consumir('VIRGULA')
        
        self.consumir('FECHA_PAREN')
        self.consumir('ABRE_CHAVE')
        
        corpo = []
        while self.token_atual and self.token_atual.tipo != 'FECHA_CHAVE':
            if self.token_atual.valor == 'var:':
                corpo.append(self.declaracao_variavel())
            elif self.token_atual.valor == 'back':
                corpo.append(self.retorno())
            elif self.token_atual.valor == 'Imp':
                corpo.append(self.impressao())
            else:
                corpo.append(self.expressao())
                if self.token_atual and self.token_atual.tipo == 'PONTO_VIRG':
                    self.consumir('PONTO_VIRG')
        
        self.consumir('FECHA_CHAVE')
        
        return {
            'tipo': 'funcao',
            'nome': nome.valor,
            'parametros': parametros,
            'corpo': corpo
        }
    
    def declaracao_variavel(self) -> Dict[str, Any]:
        self.consumir('PALAVRACHAVE')
        nome = self.consumir('ID')
        self.consumir('ATRIB')
        valor = self.expressao()
        self.consumir('PONTO_VIRG')
        
        return {
            'tipo': 'declaracao_variavel',
            'nome': nome.valor,
            'valor': valor
        }
    
    def retorno(self) -> Dict[str, Any]:
        self.consumir('PALAVRACHAVE') 
        valor = self.expressao()
        self.consumir('PONTO_VIRG')
        
        return {
            'tipo': 'retorno',
            'valor': valor
        }
    
    def impressao(self) -> Dict[str, Any]:
        self.consumir('PALAVRACHAVE')
        valor = self.expressao()
        self.consumir('PONTO_VIRG')
        
        return {
            'tipo': 'impressao',
            'valor': valor
        }
    
    def expressao(self) -> Dict[str, Any]:
        if self.token_atual.tipo == 'INT':
            token = self.consumir('INT')
            return {'tipo': 'literal', 'valor': int(token.valor)}
        elif self.token_atual.tipo == 'FLOAT':
            token = self.consumir('FLOAT')
            return {'tipo': 'literal', 'valor': float(token.valor)}
        elif self.token_atual.tipo == 'STRING':
            token = self.consumir('STRING')
            return {'tipo': 'literal', 'valor': token.valor[1:-1]}
        elif self.token_atual.tipo == 'ID':
            nome = self.consumir('ID')
            
            if self.token_atual and self.token_atual.tipo == 'ABRE_PAREN':
                self.consumir('ABRE_PAREN')
                argumentos = []
                while self.token_atual and self.token_atual.tipo != 'FECHA_PAREN':
                    argumentos.append(self.expressao())
                    if self.token_atual and self.token_atual.tipo == 'VIRGULA':
                        self.consumir('VIRGULA')
                self.consumir('FECHA_PAREN')
                
                return {
                    'tipo': 'chamada_funcao',
                    'nome': nome.valor,
                    'argumentos': argumentos
                }
            else:
                if self.token_atual and self.token_atual.tipo == 'OP_ARIT':
                    operador = self.consumir('OP_ARIT')
                    direita = self.expressao()
                    return {
                        'tipo': 'operacao_binaria',
                        'esquerda': {'tipo': 'variavel', 'nome': nome.valor},
                        'operador': operador.valor,
                        'direita': direita
                    }
                else:
                    return {'tipo': 'variavel', 'nome': nome.valor}
        else:
            self.erro(f"Expressão inválida iniciada com '{self.token_atual.valor}'")
