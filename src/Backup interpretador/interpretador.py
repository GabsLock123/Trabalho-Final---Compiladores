from CVisitor import CVisitor
from CParser import CParser
from tabela_simbolos import TabelaSimbolos

# Exceção para sinalizar um break
class BreakException(Exception):
    """Exceção para sinalizar um break em estruturas de controle."""
    pass


class Interpretador(CVisitor):
    def __init__(self):
        self.tabela_simbolos = TabelaSimbolos()

    def visitDirective(self, ctx):
        """
        Trata diretivas de pré-processamento, como #include e #define.
        """
        directive_type = ctx.getChild(0).getText()  # Identifica o tipo da diretiva (#include ou #define)
        
        if directive_type == '#include':
            included_file = ctx.IncludeFile().getText()  # Captura o arquivo incluído
            included_file = included_file.strip('<>"')   # Remove os delimitadores (<>, "")
            print(f"Incluindo biblioteca: {included_file}")
            # Aqui, você pode simular a inclusão do arquivo, carregar conteúdo ou registrar a inclusão
            # Exemplo: self.included_files.add(included_file)

        elif directive_type == '#define':
            macro_name = ctx.Identifier().getText()
            macro_value = self.visit(ctx.expression()) if ctx.expression() else None
            self.tabela_simbolos.adicionar_macro(macro_name, macro_value)
            print(f"Macro definida -> Nome: {macro_name}, Valor: {macro_value}")

    def visitVarDecl(self, ctx):
        """
        Visita uma declaração de variável e adiciona à tabela de símbolos.
        Suporte para variáveis inicializadas e não inicializadas.
        """
        tipo = ctx.type_().getText()  # Tipo da variável
        nome = ctx.Identifier().getText()  # Nome da variável

        # Verifica se a variável já foi declarada
        if nome in self.tabela_simbolos.variaveis:
            raise Exception(f"Variável '{nome}' já foi declarada.")

        # Avalia o valor inicial, se houver
        valor = None
        inicializada = False
        if ctx.expression():
            try:
                valor = self.visit(ctx.expression())  # Avalia o valor da expressão
                inicializada = True  # Marca como inicializada se houver valor
            except Exception as e:
                # Exibe a mensagem de erro sem propagar exceções adicionais
                print(f"Erro ao inicializar a variável '{nome}': {str(e)}")
                return

        # Adiciona a variável à tabela de símbolos
        self.tabela_simbolos.adicionar_variavel(nome, tipo, valor)
        status = "inicializada" if inicializada else "não inicializada"
        print(f"Variável declarada -> Nome: {nome}, Tipo: {tipo}, Status: {status}")







    def visitAssignment(self, ctx):
        """
        Atribuição de valor a uma variável, com verificação de tipos.
        """
        nome = ctx.Identifier().getText()
        valor = self.visit(ctx.expression())  # Avalia o valor da expressão
        variavel = self.tabela_simbolos.obter_variavel(nome, verificar_inicializacao=False)  # Permite atribuição sem verificar inicialização

        tipo_variavel = variavel["tipo"]

        # Verifica compatibilidade de tipos
        if tipo_variavel == "int" and not isinstance(valor, int):
            if isinstance(valor, float):
                print(f"Aviso: Conversão implícita de FLOAT para INT ao atribuir '{valor}' à variável '{nome}'.")
                valor = int(valor)
            else:
                raise Exception(f"Erro: Valor '{valor}' incompatível com o tipo INT da variável '{nome}'.")

        elif tipo_variavel == "float" and not isinstance(valor, (int, float)):
            raise Exception(f"Erro: Valor '{valor}' incompatível com o tipo FLOAT da variável '{nome}'.")

        elif tipo_variavel == "char" and not (isinstance(valor, str) and len(valor) == 1):
            raise Exception(f"Erro: Valor '{valor}' incompatível com o tipo CHAR da variável '{nome}'.")

        # Caso de outros tipos (short, long, etc.)
        elif tipo_variavel in ["short", "long", "unsigned", "unsigned int", "unsigned long", "long long"]:
            if not isinstance(valor, int):
                raise Exception(f"Erro: Valor '{valor}' incompatível com o tipo {tipo_variavel.upper()} da variável '{nome}'.")

        # Atualiza o valor da variável
        self.tabela_simbolos.atualizar_variavel(nome, valor)
        print(f"Variável '{nome}' atualizada -> Tipo: {tipo_variavel}, Novo Valor: {valor}")




    def visitExpression(self, ctx):
        if ctx.Number():
            valor = ctx.Number().getText()
            return float(valor) if '.' in valor else int(valor)
        elif ctx.Identifier():
            # Verifica inicialização ao acessar uma variável
            var = self.tabela_simbolos.obter_variavel(ctx.Identifier().getText(), verificar_inicializacao=True)
            return var["valor"]
        elif ctx.CharLiteral():
            return ctx.CharLiteral().getText().strip("'")
        elif ctx.getChildCount() == 3:
            op_esq = self.visit(ctx.expression(0))
            op_dir = self.visit(ctx.expression(1))
            operador = ctx.getChild(1).getText()
            if operador == '+':
                return op_esq + op_dir
            elif operador == '-':
                return op_esq - op_dir
            elif operador == '*':
                return op_esq * op_dir
            elif operador == '/':
                return op_esq / op_dir
            elif operador == '%':
                return op_esq % op_dir
            elif operador == '&&':
                return bool(op_esq and op_dir)
            elif operador == '||':
                return bool(op_esq or op_dir)
            elif operador == '!':
                return not op_esq
            elif operador == '>':
                return op_esq > op_dir
            elif operador == '<':
                return op_esq < op_dir
            elif operador == '>=':
                return op_esq >= op_dir
            elif operador == '<=':
                return op_esq <= op_dir
            elif operador == '==':
                return op_esq == op_dir
            elif operador == '!=':
                return op_esq != op_dir

        return None




    def visitIfStatement(self, ctx):
        """
        Visita um nó if-else e avalia a condição.
        - ctx.expression() avalia a condição do if.
        - ctx.statement(0) é o bloco do if.
        - ctx.statement(1) (opcional) é o bloco do else.
        """
        condicao = self.visit(ctx.expression())  # Avalia a condição
        print(f"Avaliando condição do if: {condicao}")

        if condicao:
            print("Condição verdadeira, executando bloco if.")
            # Se a condição for verdadeira, executa o bloco do if
            self.visit(ctx.statement(0))
        elif ctx.statement(1):
            print("Condição falsa, executando bloco else.")
            # Se existir um bloco else, executa-o
            self.visit(ctx.statement(1))

    def visitSwitchStatement(self, ctx):
        """
        Visita um nó switch-case e avalia o valor do switch.
        - ctx.caseBlock(i) acessa cada case.
        - ctx.defaultBlock(i) acessa o bloco default.
        """
        valor_switch = self.visit(ctx.expression())  # Avalia a expressão do switch
        print(f"Avaliando switch com valor: {valor_switch}")

        # Flag para indicar se um case foi executado
        caso_executado = False

        # Processa os blocos de casos
        for case in ctx.caseBlock():
            case_expr = self.visit(case.caseLabel().expression())  # Avalia o valor do case
            if valor_switch == case_expr:
                print(f"Executando case: {case_expr}")
                caso_executado = True  # Marca que um caso foi executado

                try:
                    # Executa as instruções no case
                    for stmt in case.statement():
                        self.visit(stmt)
                except BreakException:
                    print("Encontrado break, interrompendo o switch.")
                    return  # Interrompe o switch sem levantar exceção global

        # Processa o bloco default apenas se nenhum caso foi executado
        if not caso_executado:
            for default in ctx.defaultBlock():
                print("Executando bloco default")
                for stmt in default.statement():
                    self.visit(stmt)

    def visitWhileStatement(self, ctx):
        """
        Visita e executa um loop while.
        - ctx.expression() avalia a condição do while.
        - ctx.statement() executa o corpo do loop.
        """
        while True:
            condicao = self.visit(ctx.expression())  # Avalia a condição do while
            print(f"Avaliando condição do while: {condicao}")

            if not condicao:  # Se a condição for falsa, sai do loop
                break

            # Executa o corpo do loop
            try:
                self.visit(ctx.statement())
            except BreakException:
                print("Encontrado break, interrompendo o while.")
                break

    def visitBreakStatement(self, ctx):
        """Interrompe a execução de um loop ou switch."""
        raise BreakException()
    

    def visitDoWhileStatement(self, ctx):
        """
        Visita e executa um loop do-while.
        - ctx.statement() é o bloco de instruções.
        - ctx.expression() é a condição do loop.
        """
        while True:
            # Executa o bloco do loop
            try:
                self.visit(ctx.statement())
            except BreakException:
                print("Encontrado break, interrompendo o do-while.")
                break

            # Avalia a condição após executar o bloco
            condicao = self.visit(ctx.expression())
            print(f"Avaliando condição do do-while: {condicao}")

            if not condicao:
                break

    def visitInputOutputStatement(self, ctx):
        """
        Interpreta declarações de entrada e saída, como printf e scanf.
        """
        if ctx.getChild(0).getText() == "printf":
            string_literal = ctx.StringLiteral()
            if string_literal is None:
                raise Exception("Erro: Nenhum literal de string encontrado no printf.")
            
            # Processa o literal de string
            formato = string_literal.getText().strip('"')
            formato = bytes(formato, "utf-8").decode("unicode_escape")

            # Processa os argumentos
            valores = [self.visit(expr_ctx) for expr_ctx in ctx.expression()]
            
            try:
                mensagem = formato % tuple(valores)
            except TypeError as e:
                raise Exception(f"Erro: {e} - Verifique os argumentos do printf.")
            
            print(mensagem, end="")

        elif ctx.getChild(0).getText() == "scanf":
            string_literal = ctx.StringLiteral()
            if string_literal is None:
                raise Exception("Erro: Nenhum literal de string encontrado no scanf.")
            
            formato = string_literal.getText().strip('"')
            variaveis = ctx.Identifier()
            
            if len(variaveis) != len(formato.split("%")) - 1:
                raise Exception("Erro: Número de variáveis não corresponde ao formato.")
            
            for i, var_ctx in enumerate(variaveis):
                nome = var_ctx.getText()
                var = self.tabela_simbolos.obter_variavel(nome, verificar_inicializacao=False)
                tipo = var["tipo"]
                
                entrada = input(f"Digite um valor para {nome} ({tipo}): ")
                
                try:
                    if tipo == "int":
                        valor = int(entrada)
                    elif tipo in ["float", "double"]:
                        valor = float(entrada)
                    elif tipo == "char":
                        valor = entrada[0]
                    else:
                        raise Exception(f"Tipo '{tipo}' não suportado para entrada.")
                    self.tabela_simbolos.atualizar_variavel(nome, valor)
                except ValueError:
                    raise Exception(f"Erro: Valor '{entrada}' incompatível com o tipo '{tipo}'.")
        





    

