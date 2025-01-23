import sys
import os

# Adiciona o diretório 'gramatica' ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../gramatica")))

# Imports ajustados para os arquivos gerados pelo ANTLR
from CLexer import CLexer
from CParser import CParser
from antlr4 import FileStream, CommonTokenStream
from interpretador import Interpretador

def main(argv):
    # Verifica argumentos
    if len(argv) < 2:
        print("Usage: python main.py <source_file.c>")
        return

    # Lê o código-fonte
    input_file = argv[1]
    input_stream = FileStream(input_file, encoding='utf-8')

    # Gera tokens e árvore sintática
    lexer = CLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = CParser(stream)

    # Gera a árvore de análise
    tree = parser.program()  # O método 'program()' corresponde à regra inicial da gramática

    # Imprime a árvore de análise para depuração
    print("\n=== Árvore de Análise Sintática ===")
    print(tree.toStringTree(recog=parser))

    # Interpreta o código
    interpretador = Interpretador()
    interpretador.visit(tree)  # Visita a árvore gerada para interpretar o código

    # Mostra a tabela de símbolos no final
    print("\nTabela de Símbolos:")
    for nome, props in interpretador.tabela_simbolos.variaveis.items():
        print(f"{nome}: {props}")

if __name__ == "__main__":
    main(sys.argv)