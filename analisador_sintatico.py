# Futuro analisador sintático
# Aqui você vai implementar as funções para análise sintática

from analisador_lexico import tokenizar

def analisar_sintatico(tokens):
    # Exemplo de função vazia para o futuro
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = list(tokens)
        self.pos = 0
        self.token_atual = self.tokens[self.pos] if self.tokens else None

    def consumir(self, tipo_esperado):
        if self.token_atual and self.token_atual.tipo == tipo_esperado:
            self.avancar()
        else:
            self.erro(f"Esperado token {tipo_esperado}, mas encontrado {self.token_atual.tipo}")

    def avancar(self):
        self.pos += 1
        self.token_atual = self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def erro(self, mensagem):
        raise SyntaxError(f"[Linha {self.token_atual.linha}] Erro: {mensagem}")

    def analisar(self):
        while self.token_atual:
            if self.token_atual.valor == 'fnc':
                self.funcao()
            elif self.token_atual.valor == 'var:':
                self.declaracao_variavel()
            else:
                self.erro("Início de declaração inválido")

    def funcao(self):
        self.consumir('PALAVRA_CHAVE')  # função; fnc
        self.consumir('ID')
        self.consumir('ABRE_PAREN')
        self.consumir('FECHA_PAREN')
        self.consumir('ABRE_CHAVE')
        while self.token_atual and self.token_atual.tipo != 'FECHA_CHAVE':
            if self.token_atual.valor == 'var:':
                self.declaracao_variavel()
            else:
                self.avancar()  # Placeholder
        self.consumir('FECHA_CHAVE')

    def declaracao_variavel(self):
        self.consumir('PALAVRA_CHAVE')  # var; variavel
        self.consumir('ID')
        self.consumir('ATRIB')
        if self.token_atual.tipo in ('INT', 'FLOAT', 'STRING', 'ID'):
            self.avancar()
        else:
            self.erro("Valor inválido na atribuição")
        self.consumir('PONTO_VIRG')
