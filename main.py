from analisador_lexico import tokenizar, Token
from analisador_sintatico import Parser

def imprimir_tokens(tokens):
    print("=" * 60)
    print("ANÁLISE LÉXICA")
    print("=" * 60)
    print(f"{'TIPO':<15} {'VALOR':<15} {'LINHA':<6} {'COLUNA':<6}")
    print("-" * 60)
    for token in tokens:
        print(f"{token.tipo:<15} {token.valor:<15} {token.linha:<6} {token.coluna:<6}")
    print("=" * 60)

def main():
    codigo_exemplo = '''
    fnc soma(a, b) {
        var: res -> a + b;
        back res;
    }
    
    fnc principal() {
        var: x -> 10;
        var: y -> 20.5;
        var: resultado -> soma(x, y);
        Imp resultado;
    }

    fnc mult (a, b) {
        var: resultado -> a * b;
        back resultado;
    }

    Imp mult(5, 3); // Imprime: 15

    var: soma -> 0;
    var: i -> 1;
    dum (i <= 10) {
        soma -> soma + i;
        i -> i + 1;
    }
    Imp soma; // Imprime: 55
    '''
    
    try:
        tokens = list(tokenizar(codigo_exemplo))
        imprimir_tokens(tokens)
        
        print("\nANÁLISE SINTÁTICA")
        print("=" * 60)
        parser = Parser(tokens)
        arvore = parser.analisar()
        print("✓ Análise sintática concluída com sucesso!")
        print(f"✓ {len(arvore)} declarações encontradas")
        
    except SyntaxError as e:
        print(f"❌ Erro de sintaxe: {e}")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == '__main__':
    main()
