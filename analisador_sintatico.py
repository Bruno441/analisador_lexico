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
            elif self.token_atual.valor == 'var':
                self.arvore_sintatica.append(self.declaracao_variavel())
            elif self.token_atual.valor == 'Imp':
                self.arvore_sintatica.append(self.impressao())
            elif self.token_atual.valor == 'dum':
                self.arvore_sintatica.append(self.repeticao())
            elif self.token_atual.tipo == 'ID' and self.verificar_proximo('ATRIB'):
                self.arvore_sintatica.append(self.atribuicao())
            else:
                # Permitir chamadas de função no escopo global
                self.arvore_sintatica.append(self.expressao())
                if self.token_atual and self.token_atual.tipo == 'PONTO_VIRG':
                    self.consumir('PONTO_VIRG')
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
            if self.token_atual.valor == 'var':
                corpo.append(self.declaracao_variavel())
            elif self.token_atual.valor == 'back':
                corpo.append(self.retorno())
            elif self.token_atual.valor == 'Imp':
                corpo.append(self.impressao())
            elif self.token_atual.valor == 'dum':
                corpo.append(self.repeticao())
            elif self.token_atual.tipo == 'ID' and self.verificar_proximo('ATRIB'):
                corpo.append(self.atribuicao())
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
        self.consumir('DOIS_PTS')
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
    
    def atribuicao(self) -> dict:
        identificador = self.consumir('ID')
        self.consumir('ATRIB')
        valor = self.expressao()
        self.consumir('PONTO_VIRG')
        return {
            'tipo': 'atribuicao',
            'variavel': identificador.valor,
            'valor': valor
        }
    
    def verificar_proximo(self, tipo: str) -> bool:
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1].tipo == tipo
        return False
    
    def repeticao(self) -> dict:
        self.consumir('PALAVRACHAVE')         # Consome a palavra-chave "dum"
        self.consumir('ABRE_PAREN')           # Consome "("
        condicao = self.expressao()           # Analisa a expressão condicional
        self.consumir('FECHA_PAREN')          # Consome ")"
        self.consumir('ABRE_CHAVE')           # Consome "{"

        corpo = []
        while self.token_atual and self.token_atual.tipo != 'FECHA_CHAVE':
            if self.token_atual.valor == 'var':
                corpo.append(self.declaracao_variavel())
            elif self.token_atual.valor == 'Imp':
                corpo.append(self.impressao())
            elif self.token_atual.valor == 'dum':
                corpo.append(self.repeticao())  # Permite dum aninhado
            elif self.token_atual.tipo == 'ID' and self.verificar_proximo('ATRIB'):
                corpo.append(self.atribuicao())
            else:
                self.erro(f"Expressão inválida iniciada com '{self.token_atual.valor}'")

        self.consumir('FECHA_CHAVE')          # Consome "}"

        return {'tipo': 'repeticao', 'condicao': condicao, 'corpo': corpo}
    
    def expressao(self) -> dict:
        return self.expressao_relacional()

    def expressao_relacional(self) -> dict:
        esquerda = self.expressao_aritmetica()
        while self.token_atual and self.token_atual.tipo == 'OP_REL':
            operador = self.consumir('OP_REL')
            direita = self.expressao_aritmetica()
            esquerda = {
                'tipo': 'operacao_relacional',
                'esquerda': esquerda,
                'operador': operador.valor,
                'direita': direita
            }
        return esquerda

    def expressao_aritmetica(self) -> dict:
        esquerda = self.expressao_primaria()
        while self.token_atual and self.token_atual.tipo == 'OP_ARIT':
            operador = self.consumir('OP_ARIT')
            direita = self.expressao_primaria()
            esquerda = {
                'tipo': 'operacao_binaria',
                'esquerda': esquerda,
                'operador': operador.valor,
                'direita': direita
            }
        return esquerda

    def expressao_primaria(self) -> dict:
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
                return {'tipo': 'variavel', 'nome': nome.valor}
        else:
            self.erro(f"Expressão inválida iniciada com '{self.token_atual.valor}'")