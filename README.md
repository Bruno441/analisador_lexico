# Documentação da Linguagem Nexon

## Visão Geral
Nexon é uma linguagem de programação leve, projetada com uma sintaxe inspirada em raízes latinas, buscando clareza e simplicidade. Ela suporta construções essenciais de programação, como variáveis, funções, condicionais, loops e operações aritméticas básicas. Este documento detalha os tokens principais do Nexon, seus propósitos e fornece exemplos para demonstrar seu uso.

## Elementos da Sintaxe

### Tokens
As tabelas a seguir descrevem os tokens do Nexon, categorizados por sua finalidade.

#### Palavras-chave
| Token    | Finalidade                          | Descrição                                       |
|----------|-------------------------------------|------------------------------------------------|
| `fnc`    | Definição de Função                | Declara uma função com nome e parâmetros.      |
| `var:`   | Declaração de Variável             | Declara uma variável.                          |
| `back`   | Retorno de Função                  | Retorna um valor de uma função.                |
| `si`     | Condicional (se)                   | Inicia uma condição "se".                      |
| `velsi`  | Condicional (senão se)             | Especifica uma condição "senão se".            |
| `nisi`   | Condicional (senão)                | Especifica uma condição "senão".               |
| `dum`    | Loop Enquanto                      | Inicia um loop "enquanto".                     |
| `per`    | Loop Para                          | Inicia um loop "para".                         |
| `Imp`    | Impressão                          | Exibe um valor no console.                     |
| `fin`    | Fim de Bloco                       | Marca o fim de um bloco (alternativa a `}`).   |

#### Operadores
| Token    | Finalidade                          | Descrição                                       |
|----------|-------------------------------------|------------------------------------------------|
| `->`     | Atribuição                         | Atribui um valor a uma variável.               |
| `+`      | Adição                             | Soma dois valores.                             |
| `-`      | Subtração                          | Subtrai um valor de outro.                     |
| `*`      | Multiplicação                      | Multiplica dois valores.                       |
| `/`      | Divisão                            | Divide um valor por outro.                     |
| `==`     | Igualdade                          | Verifica se dois valores são iguais.           |
| `!=`     | Desigualdade                       | Verifica se dois valores são diferentes.       |
| `<`      | Menor que                          | Verifica se um valor é menor que outro.        |
| `>`      | Maior que                          | Verifica se um valor é maior que outro.        |
| `<=`     | Menor ou Igual                     | Verifica se um valor é menor ou igual a outro. |
| `>=`     | Maior ou Igual                     | Verifica se um valor é maior ou igual a outro. |

#### Símbolos
| Token    | Finalidade                          | Descrição                                       |
|----------|-------------------------------------|------------------------------------------------|
| `(` `)`  | Parênteses                         | Agrupa expressões ou define parâmetros de função. |
| `{` `}`  | Chaves                             | Delimita blocos (opcional, pode usar `fin`).    |
| `;`      | Ponto e Vírgula                    | Separa instruções.                             |
| `,`      | Vírgula                            | Separa argumentos ou elementos.                |

#### Identificadores e Literais
| Tipo de Token      | Padrão                              | Descrição                                       |
|--------------------|-------------------------------------|------------------------------------------------|
| Identificador      | `[a-zA-Z_][a-zA-Z0-9_]*`           | Nomes para variáveis e funções.                |
| Literal Inteiro    | `[0-9]+`                           | Números inteiros (ex.: `42`).                  |
| Literal Flutuante  | `[0-9]+\.[0-9]+`                   | Números decimais (ex.: `3.14`).                |
| Literal String     | `"[^"]*"`                          | Texto entre aspas duplas (ex.: `"ola"`).       |

#### Comentários
| Token    | Finalidade                          | Descrição                                       |
|----------|-------------------------------------|------------------------------------------------|
| `//`     | Comentário de Linha                | Ignora o texto até o final da linha.           |

## Regras da Sintaxe
- **Instruções** terminam com ponto e vírgula (`;`).
- **Blocos** são delimitados por chaves (`{}`) ou finalizados com a palavra-chave `fin`.
- **Funções** são declaradas com `fnc`, seguidas pelo nome da função, parâmetros entre parênteses e um bloco.
- **Variáveis** são declaradas com `var:` seguido do nome da variável e uma atribuição opcional usando `->`.
- **Expressões** suportam operações aritméticas (`+`, `-`, `*`, `/`) e comparações (`==`, `!=`, `<`, `>`, `<=`, `>=`).

## Exemplos

### Exemplo 1: Função para Multiplicar Dois Números
Este exemplo define uma função que multiplica dois números e imprime o resultado.

```nexon
fnc mult (a, b) {
    var: resultado -> a * b;
    back resultado;
}

Imp mult(5, 3); // Imprime: 15
```

### Explicação:

- `fnc mult (a, b)`: Declara uma função chamada `mult` com parâmetros `a` e `b`.
- `var: resultado -> a * b`: Declara resultado e atribui o produto de `a` e `b`.
- `back resultado`: Retorna o valor de `resultado`.
- `Imp mult(5, 3)`: Chama `mult` com os argumentos `5` e `3`, imprimindo o resultado.

### Exemplo 2: Somando Números com um Loop Enquanto

Este programa soma números de 1 a 10 usando um loop `dum` (enquanto).
```nexon
var: soma -> 0;
var: i -> 1;
dum (i <= 10) {
    soma -> soma + i;
    i -> i + 1;
}
Imp soma; // Imprime: 55
```

### Explicação:

- `var: soma -> 0`: Inicializa `soma` com 0.
- `var: i -> 1`: Inicializa `i` com 1.
- `dum (i <= 10)`: Executa o loop enquanto `i` for menor ou igual a 10.
- `soma -> soma + i`: Adiciona `i` a `soma`.
- `i -> i + 1`: Incrementa `i`.
- `Imp soma`: Imprime o valor final de `soma` (55).

### Exemplo 3: Instruções Condicionais
Este programa verifica o valor de uma variável e imprime uma mensagem com base em condições.

```nexon
var: x -> 7;
si (x > 5) {
    Imp "x maior que 5";
} velsi (x == 5) {
    Imp "x igual a 5";
} nisi {
    Imp "x menor que 5";
}
```

### Explicação:

- `var: x -> 7`: Declara `x` e atribui o valor 7.
- `si (x > 5)`: Verifica se `x` é maior que 5.
- `Imp "x maior que 5"`: Imprime se a condição for verdadeira (executada neste caso).
- `velsi` e `nisi`: Lidam com condições alternativas, ignoradas aqui, pois a primeira condição é verdadeira.

### Exemplo 4: Loop Para Imprimir Números

Este exemplo usa um loop `per` (para) para imprimir números de 1 a 5.

```nexon
per (var: i -> 1; i <= 5; i -> i + 1) {
    Imp i;
}
```

### Explicação:

- `per (var: i -> 1; i <= 5; i -> i + 1)`: Inicializa `i` com 1, executa o loop enquanto `i <= 5` e incrementa `i` a cada iteração.
- `Imp i`: Imprime o valor de `i` (1, 2, 3, 4, 5).

## Observações

- Nexon diferencia maiúsculas de minúsculas para identificadores e palavras-chave.
- Strings devem ser delimitadas por aspas duplas (`"`).
- A palavra-chave `fin` pode substituir chaves de fechamento (`}`) para consistência estética, mas chaves são suportadas para familiaridade com outras linguagens.
- Versões futuras podem incluir recursos como arrays, declarações de tipos e comentários de múltiplas linhas.

## Primeiros Passos
Para começar a escrever programas em Nexon:

1. Escreva seu código em um arquivo `.nexon`.
2. Use um analisador léxico (ex.: construído com Flex) para tokenizar a entrada.
3. Estenda a linguagem com um analisador sintático e interpretador/compilador para execução.