import sys
import os

# Adiciona o diretório 'gramatica' ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../gramatica")))

# Imports ajustados para os arquivos gerados pelo ANTLR
from CLexer import CLexer
from CParser import CParser
from antlr4 import FileStream, CommonTokenStream
from interpretador import Interpretador, ReturnException  # Certifique-se de que ReturnException está exportada

def verifica_main(tree):
    """
    Percorre a árvore sintática para verificar se a função main existe.
    Retorna True se encontrar, False caso contrário.
    """
    for i in range(tree.getChildCount()):
        child = tree.getChild(i)
        if child.__class__.__name__ == "FunctionDefContext":
            tipo = child.getChild(0).getText()  # tipo de retorno da função
            nome = child.getChild(1).getText()  # nome da função
            if nome == "main":
                return True
    return False

def main(argv):
    if len(argv) < 2:
        print("Uso: python main.py <source_file.c>")
        return

    input_file = argv[1]
    input_stream = FileStream(input_file, encoding='utf-8')
    lexer = CLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = CParser(stream)
    tree = parser.program()

    print("\n=== Árvore de Análise Sintática ===")
    print(tree.toStringTree(recog=parser))

    if not verifica_main(tree):
        print("Erro: O código não possui a função main(). Execução interrompida.")
        return

    interpretador = Interpretador()
    interpretador.visit(tree)  # Registra definições, variáveis, etc.
    
    # Executa a função main e captura o retorno (ocultando a exceção de return)
    if "main" in interpretador.funcoes:
        print("Executando a função main:")
        mainDefCtx = interpretador.funcoes["main"]
        try:
            interpretador.visit(mainDefCtx.block())
        except ReturnException:
            # Apenas capturamos a exceção para "ocultar" o retorno
            pass
    else:
        print("Erro: Função main não definida.")

    print("\nTabela de Símbolos:")
    for nome, props in interpretador.tabela_simbolos.variaveis.items():
        print(f"{nome}: {props}")

if __name__ == "__main__":
    main(sys.argv)
