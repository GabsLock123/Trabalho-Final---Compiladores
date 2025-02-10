# InterCptor - Interpretador C em Python com ANTLR4

Este projeto implementa um interpretador para uma linguagem semelhante a C, utilizando Python e ANTLR4. O interpretador suporta diversas funcionalidades da linguagem C, incluindo:

- Declaração de variáveis e arrays (inclusive arrays sem tamanho definido, com inicialização por lista ou literal)
- Structs e Unions
- Definição e chamada de funções (com e sem parâmetros, com e sem retorno)
- Controle de fluxo: if/else, switch/case e laços (while, do/while, for)
- Entrada e saída: printf, scanf, gets e puts  

> **Importante:** O código contém mensagens de depuração que mostram o fluxo de execução, mas, para que o interpretador exiba apenas as mensagens definidas nos `printf` do código C (e não mensagens de depuração internas), as chamadas de `print()` que emitem mensagens informativas foram removidas ou comentadas.

## Estrutura do Projeto

- **C.g4:** Gramática para a linguagem C (adaptada para suportar as funcionalidades implementadas).
- **Interpretador.py:** Implementação da classe `Interpretador` (baseada em `CVisitor`), contendo métodos de visita para cada construção da linguagem.
- **TabelaSimbolos.py:** Implementação da tabela de símbolos que armazena variáveis, funções, structs e unions.
- **main.py:** Programa principal que carrega um arquivo fonte C, gera a árvore de análise sintática e executa o interpretador.

## Principais Funções do Interpretador

A seguir, uma breve explicação de cada método importante da classe `Interpretador`:

### Inicialização e Expressões

- **`visitInitializerList(ctx)`**  
  Visita um nó de lista de inicializadores (ex.: `{ 1, 2, 3 }`) e retorna uma lista com os valores resultantes.

- **`visitInit(ctx)`**  
  Trata a produção `init`, que pode ser uma lista de inicializadores ou uma expressão simples. Chama o método apropriado conforme o nó presente.

- **`visitExpression(ctx)`**  
  Avalia expressões (literais, operações binárias, unárias, acesso a arrays, chamada de função, etc.) e retorna o valor resultante.

### Declaração e Atribuição de Variáveis

- **`visitVarDecl(ctx)`**  
  Trata a declaração de variáveis e arrays. Suporta:
  - Variáveis simples (ex.: `int x;`)
  - Arrays com tamanho explícito (ex.: `int arr[3];`)
  - Arrays sem tamanho definido, cujo tamanho é inferido a partir da inicialização (ex.: `char s[] = "Hello";`)
  - Conversão de literais string para vetores de `char` (preenchendo com `'\0'` se necessário).

- **`_verificar_tipo_e_converter(tipo_variavel, valor, nome_alvo)`**  
  Método auxiliar que verifica se o valor atribuído é compatível com o tipo da variável e, se necessário, converte-o.  
  _Exemplo:_ Converte um valor float para int ou garante que um valor para um `char` seja uma string de 1 caractere.

- **`visitAssignment(ctx)`**  
  Trata atribuições, distinguindo:
  - Atribuição simples (`x = expr;`)
  - Atribuição a elementos de array (`arr[expr] = expr;`)
  - Atribuição a campos de structs ou unions (`p.campo = expr;`)

### Funções e Controle de Fluxo

- **`visitFunctionDef(ctx)`**  
  Registra uma função (seu tipo de retorno e corpo) no interpretador, para que possa ser chamada posteriormente.

- **`visitFunctionCall(ctx)`**  
  Executa uma chamada de função. Avalia os argumentos, cria um novo escopo (tabela de símbolos), insere os parâmetros e executa o corpo da função, capturando seu valor de retorno.

- **`visitReturnStatement(ctx)`**  
  Avalia a expressão de retorno (se houver) e lança uma exceção `ReturnException` para interromper a execução do corpo da função e retornar o valor.

- **`visitIfStatement(ctx)`**  
  Avalia a condição de um `if-else` e executa o bloco correspondente.

- **`visitSwitchStatement(ctx)`**  
  Avalia a expressão do `switch` e executa o bloco de `case` correspondente, ou o `default` se nenhum case for igual.

- **`visitWhileStatement(ctx)`**, **`visitDoWhileStatement(ctx)`** e **`visitForStatement(ctx)`**  
  Implementam os laços de repetição `while`, `do-while` e `for`, respectivamente, avaliando condições e atualizando variáveis conforme necessário.

- **`visitForHeaderAssignment(ctx)`**  
  Trata as atribuições no cabeçalho do laço `for`, tanto na inicialização quanto na atualização.

### Entrada e Saída

- **`visitInputOutputStatement(ctx)`**  
  Trata as operações de entrada e saída:
  - **`printf`**: Formata e imprime a mensagem. Se um argumento for um array de `char`, converte-o em string usando `"".join(...)`.
  - **`scanf`**: Lê valores do input, convertendo-os conforme o tipo da variável. Para arrays de `char`, lê uma string.
  - **`gets`**: Lê uma linha inteira do input e armazena em um array de `char` (com preenchimento ou truncamento conforme o tamanho declarado).
  - **`puts`**: Imprime uma string. Se o valor for um array de `char`, converte-o em string antes de imprimir.

## Como Utilizar

1. **Gere a árvore de análise sintática:**  
   Utilize o ANTLR4 para gerar os arquivos do parser a partir da gramática `C.g4`.

2. **Execute o interpretador:**  
   Rode o script `main.py` passando como argumento o arquivo fonte C que deseja interpretar:
   ```bash
   python main.py exemplo.c
