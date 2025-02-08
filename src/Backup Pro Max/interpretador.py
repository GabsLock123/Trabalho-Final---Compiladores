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

    def visitStructDef(self, ctx):
        """
        structDef: 'struct' Identifier '{' varDecl* '}' ';'
        Armazena os campos da struct em self.tabela_simbolos.
        """
        nome_struct = ctx.Identifier().getText()

        # Dicionário local para armazenar campos: { nomeCampo: tipoCampo, ... }
        campos = {}

        # Percorre cada varDecl interno
        for vd in ctx.varDecl():
            tipo_campo = vd.type_().getText()        # ex: "int"
            nome_campo = vd.Identifier().getText()   # ex: "idade"
            if nome_campo in campos:
                raise Exception(f"Campo '{nome_campo}' duplicado na struct '{nome_struct}'.")
            campos[nome_campo] = tipo_campo

            # OBS: Não chamamos self.visitVarDecl(vd) porque não queremos criar
            #      variáveis "globais"; aqui, só definimos o tipo do campo.

        # Armazena a definição da struct
        self.tabela_simbolos.adicionar_struct(nome_struct, campos)
        print(f"Struct '{nome_struct}' definida com campos: {campos}")

    def visitVarDecl(self, ctx):
        """
        varDecl: type Identifier arraySize? ('=' expression)? ';'
        ...
        """
        tipo = ctx.type_().getText()  # ex: "structPessoa"
        nome = ctx.Identifier().getText()

        # Verifica duplicata
        if nome in self.tabela_simbolos.variaveis:
            raise Exception(f"Variável '{nome}' já foi declarada.")

        # Checa se é array (arraySize)
        tam_array = None
        if ctx.arraySize():
            size_text = ctx.arraySize().Number().getText()
            tam_array = int(size_text)

        # Se houver expressão de inicialização
        valor_inicial = None
        inicializada = False
        if ctx.expression():
            valor_inicial = self.visit(ctx.expression())
            inicializada = True

        # ==============
        # 1) Se for Array
        if tam_array is not None:
            # ... (código para array, se quiser)
            # Exemplo: int v[5];
            # Monta "tipo_base[]"
            tipo_array = tipo + "[]"
            if valor_inicial is not None:
                valor_convertido = self._verificar_tipo_e_converter(tipo, valor_inicial, f"{nome}[all]")
                array_val = [valor_convertido for _ in range(tam_array)]
            else:
                array_val = [None]*tam_array

            self.tabela_simbolos.adicionar_variavel(nome, tipo_array, array_val)
            status = "inicializada" if inicializada else "não inicializada"
            print(f"Array declarado -> Nome: {nome}, Tipo: {tipo_array}, Tamanho: {tam_array}, Status: {status}")

        # ==============
        # 2) Se for struct
        elif tipo.startswith("struct"):
            # Exemplo: "structPessoa" => "Pessoa"
            nome_struct = tipo[len("struct"):].strip()

            definicao_struct = self.tabela_simbolos.obter_struct(nome_struct)
            if definicao_struct is None:
                raise Exception(f"Struct '{nome_struct}' não foi definida antes de criar '{nome}'.")

            # Cria o dicionário de campos, todos None
            campos_iniciais = {}
            for campo, tipo_campo in definicao_struct.items():
                campos_iniciais[campo] = {"tipo": tipo_campo, "valor": None}

            # Monta valor (independente de haver expressão ou não)
            struct_valor = {
                "__struct_name__": nome_struct,
                "campos": campos_iniciais
            }
            # Em C, por padrão, `struct Pessoa p;` “cria” a struct.
            # Então podemos marcar como inicializada = True.
            inicializada = True

            # Se HOUVE um valor_inicial numérico ou algo assim, normalmente ignoramos
            # (A não ser que você queira suportar algo como `struct Pessoa p = 0;`, mas não é padrão.)
            # Então sempre sobrescrevemos com o struct_inicial.
            self.tabela_simbolos.adicionar_variavel(nome, tipo, struct_valor)
            status = "inicializada" if inicializada else "não inicializada"
            print(f"Variável declarada -> Nome: {nome}, Tipo: {tipo}, Status: {status}")

        # ==============
        # 3) Se for tipo primitivo normal (int, float, ...)
        else:
            valor = None
            if valor_inicial is not None:
                valor = self._verificar_tipo_e_converter(tipo, valor_inicial, nome)
                inicializada = True
            self.tabela_simbolos.adicionar_variavel(nome, tipo, valor)
            status = "inicializada" if inicializada else "não inicializada"
            print(f"Variável declarada -> Nome: {nome}, Tipo: {tipo}, Status: {status}")


    def _verificar_tipo_e_converter(self, tipo_variavel, valor, nome_alvo):
        """
        Faz a verificação de tipo (int, float, char, string, etc.) e converte se necessário.
        'nome_alvo' é uma string descritiva para usar em mensagens de erro ou aviso.
        Retorna o valor convertido, se for válido.
        """
        # Se for int
        if tipo_variavel == "int":
            if isinstance(valor, int):
                return valor
            elif isinstance(valor, float):
                print(f"Aviso: Conversão implícita de FLOAT para INT ao atribuir '{valor}' à '{nome_alvo}'.")
                return int(valor)
            else:
                raise Exception(f"Erro: Valor '{valor}' incompatível com o tipo INT de '{nome_alvo}'.")

        # Se for float/double
        elif tipo_variavel in ["float", "double"]:
            if isinstance(valor, (int, float)):
                return float(valor)
            else:
                raise Exception(f"Erro: Valor '{valor}' incompatível com o tipo {tipo_variavel.upper()} de '{nome_alvo}'.")

        # Se for char
        elif tipo_variavel == "char":
            if isinstance(valor, str) and len(valor) == 1:
                return valor
            else:
                raise Exception(f"Erro: Valor '{valor}' incompatível com o tipo CHAR de '{nome_alvo}'.")

        # Se for string (novo)
        elif tipo_variavel == "string":
            if isinstance(valor, str):
                return valor
            else:
                raise Exception(f"Erro: Valor '{valor}' incompatível com o tipo STRING de '{nome_alvo}'.")

        # Demais tipos (short, long, unsigned, etc.). Simplificado aqui:
        elif tipo_variavel in ["short", "long", "unsigned", "unsigned int", "unsigned long", "long long"]:
            if isinstance(valor, int):
                return valor
            elif isinstance(valor, float):
                print(f"Aviso: Conversão implícita de FLOAT para INT ao atribuir '{valor}' à '{nome_alvo}'.")
                return int(valor)
            else:
                raise Exception(f"Erro: Valor '{valor}' incompatível com o tipo {tipo_variavel.upper()} de '{nome_alvo}'.")

        # Caso seja struct (ex: "struct Pessoa") ou algo que não esteja contemplado acima, não convertemos
        elif tipo_variavel.startswith("struct"):
            if isinstance(valor, dict) and "campos" in valor:
                return valor
            else:
                raise Exception(f"Erro: Tentando atribuir valor não-struct a um struct '{nome_alvo}'.")
        else:
            # Se nenhum dos casos foi atendido, retorna o valor sem conversão.
            return valor


    def visitAssignment(self, ctx):
        """
        Atribuição de valor a:
        1) variável simples:          Identifier = expression ;
        2) campo de struct:           (Identifier ('.' Identifier)*) = expression ;
        3) elemento de array:         Identifier '[' expression ']' = expression ;

        """
        child_count = ctx.getChildCount()

        # 1) Detecta se é do formato "array[index] = expression"
        #    (Identifier '[' expression ']' '=' expression ';')
        if (child_count >= 6 
            and ctx.getChild(1).getText() == '[' 
            and ctx.getChild(3).getText() == ']' 
            and ctx.getChild(4).getText() == '='):
            
            array_name = ctx.getChild(0).getText()
            index_expr_ctx = ctx.getChild(2)
            # O valor a atribuir está no child(5) (a expressão à direita do '=')
            valor_expr_ctx = ctx.getChild(5)

            # Avalia índice e valor
            index_value = self.visit(index_expr_ctx)
            valor = self.visit(valor_expr_ctx)

            # Obtém a variável (array) da tabela
            arr_var = self.tabela_simbolos.obter_variavel(array_name, verificar_inicializacao=True)
            if not arr_var["tipo"].endswith("[]"):
                raise Exception(f"Variável '{array_name}' não é um array, mas foi usada como array.")
            
            # Verifica se o índice é inteiro
            if not isinstance(index_value, int):
                raise Exception(f"Índice do array '{array_name}' não é inteiro: {index_value}")

            # Checa limites
            array_data = arr_var["valor"]
            if index_value < 0 or index_value >= len(array_data):
                raise Exception(f"Índice {index_value} fora dos limites do array '{array_name}'.")

            # Extrai o tipo base: ex "int[]" -> "int"
            tipo_base = arr_var["tipo"][:-2]
            valor_convertido = self._verificar_tipo_e_converter(tipo_base, valor, f"{array_name}[{index_value}]")

            # Atribui
            array_data[index_value] = valor_convertido
            self.tabela_simbolos.atualizar_variavel(array_name, array_data)
            print(f"Array '{array_name}' na posição [{index_value}] atualizado -> Valor: {valor_convertido}")
            return

        # 2) Se não for array assignment, localiza '=' para separar o lado esquerdo
        left_side_tokens = []
        i = 0
        while ctx.getChild(i).getText() != '=':
            left_side_tokens.append(ctx.getChild(i).getText())
            i += 1

        # 3) Avalia o valor (lado direito do '='): pegue a 1ª expressão
        #    Substituindo ctx.expression() por ctx.expression(0)
        valor = self.visit(ctx.expression(0))

        # 4) Verifica se é um identificador simples (ex.: x = expr)
        if len(left_side_tokens) == 1:
            nome_var = left_side_tokens[0]
            variavel = self.tabela_simbolos.obter_variavel(nome_var, verificar_inicializacao=False)
            tipo_variavel = variavel["tipo"]

            valor_convertido = self._verificar_tipo_e_converter(tipo_variavel, valor, nome_var)
            self.tabela_simbolos.atualizar_variavel(nome_var, valor_convertido)
            print(f"Variável '{nome_var}' atualizada -> Tipo: {tipo_variavel}, Novo Valor: {valor_convertido}")

        else:
            # 5) Caso seja acesso a campo de struct (p.idade, p.endereco.rua, etc.)
            identifiers = []
            for token in left_side_tokens:
                if token != '.':
                    identifiers.append(token)

            nome_var = identifiers[0]
            variavel = self.tabela_simbolos.obter_variavel(nome_var, verificar_inicializacao=True)

            struct_value = variavel["valor"]
            if not isinstance(struct_value, dict) or "campos" not in struct_value:
                raise Exception(f"Tentando acessar campo de algo que não é struct: '{nome_var}'.")

            campos = struct_value["campos"]
            for idx in range(1, len(identifiers)):
                nome_campo = identifiers[idx]
                if idx == len(identifiers) - 1:
                    # Último campo
                    if nome_campo not in campos:
                        raise Exception(f"O campo '{nome_campo}' não existe na struct '{struct_value['__struct_name__']}'.")
                    
                    tipo_campo = campos[nome_campo]["tipo"]
                    valor_convertido = self._verificar_tipo_e_converter(tipo_campo, valor, f"{nome_var}.{nome_campo}")
                    campos[nome_campo]["valor"] = valor_convertido
                    print(f"Campo '{nome_campo}' da struct '{nome_var}' atualizado -> Tipo: {tipo_campo}, Valor: {valor_convertido}")
                else:
                    # Sub-struct
                    if nome_campo not in campos:
                        raise Exception(f"O campo '{nome_campo}' não existe na struct '{struct_value['__struct_name__']}'.")
                    subvalor = campos[nome_campo]["valor"]
                    if not (isinstance(subvalor, dict) and "campos" in subvalor):
                        raise Exception(f"O campo '{nome_campo}' não é um sub-struct.")
                    struct_value = subvalor
                    campos = subvalor["campos"]




    def visitExpression(self, ctx):
        """
        Interpreta expressões, incluindo:
        - Acesso a campo de struct: expression '.' Identifier
        - Acesso a índice de array: Identifier '[' expression ']'
        - Literais: Number, StringLiteral, CharLiteral
        - Identificadores simples
        - Parênteses, operadores binários e unários, etc.
        """
        child_count = ctx.getChildCount()

        # 1) Se for acesso a campo de struct: expression '.' Identifier
        if child_count == 3 and ctx.getChild(1).getText() == '.':
            left_value = self.visit(ctx.getChild(0))
            field_name = ctx.getChild(2).getText()
            if not (isinstance(left_value, dict) and "campos" in left_value):
                raise Exception(f"Tentando acessar campo '{field_name}' de algo que não é struct.")
            campos = left_value["campos"]
            if field_name not in campos:
                raise Exception(f"O campo '{field_name}' não existe na struct '{left_value['__struct_name__']}'.")
            return campos[field_name]["valor"]

        # 2) Se for acesso a array: Identifier '[' expression ']'
        if (child_count == 4
            and ctx.getChild(0).getSymbol() is not None
            and ctx.getChild(1).getText() == '['
            and ctx.getChild(3).getText() == ']'):
            array_name = ctx.getChild(0).getText()
            index_expr_ctx = ctx.getChild(2)
            index_value = self.visit(index_expr_ctx)
            arr_var = self.tabela_simbolos.obter_variavel(array_name, verificar_inicializacao=True)
            if not arr_var["tipo"].endswith("[]"):
                raise Exception(f"Variável '{array_name}' não é um array, mas foi usada como array.")
            if not isinstance(index_value, int):
                raise Exception(f"Índice do array '{array_name}' não é inteiro: {index_value}")
            array_data = arr_var["valor"]
            if index_value < 0 or index_value >= len(array_data):
                raise Exception(f"Índice {index_value} fora dos limites do array '{array_name}'.")
            return array_data[index_value]

        # 3) Se for literal numérico (Number)
        if ctx.Number():
            valor = ctx.Number().getText()
            return float(valor) if '.' in valor else int(valor)

        # 4) Se for literal de string (StringLiteral)
        if ctx.StringLiteral():
            s = ctx.StringLiteral().getText().strip('"')
            s = bytes(s, "utf-8").decode("unicode_escape")
            return s

        # 5) Se for identificador simples (ex.: x)
        if ctx.Identifier():
            var = self.tabela_simbolos.obter_variavel(ctx.Identifier().getText(), verificar_inicializacao=True)
            return var["valor"]

        # 6) Se for literal de caractere (CharLiteral)
        if ctx.CharLiteral():
            return ctx.CharLiteral().getText().strip("'")

        # 7) Se for expressão entre parênteses: ( expression )
        if child_count == 3 and ctx.getChild(0).getText() == '(' and ctx.getChild(2).getText() == ')':
            return self.visit(ctx.getChild(1))

        # 8) Se for operador binário: (expression op expression)
        if child_count == 3:
            op_esq = self.visit(ctx.expression(0))
            operador = ctx.getChild(1).getText()
            op_dir = self.visit(ctx.expression(1))
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

        # 9) Se for operador unário: ! expression ou - expression
        if child_count == 2:
            first_char = ctx.getChild(0).getText()
            if first_char == '!':
                return not self.visit(ctx.getChild(1))
            elif first_char == '-':
                return -self.visit(ctx.getChild(1))

        # 10) Caso nada bata, retorna None
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
        Interpreta declarações de entrada e saída, incluindo:
        - printf: formatação de string com argumentos.
        - scanf: leitura de valores e conversão para variáveis.
        - gets: lê uma linha da entrada padrão e armazena em uma variável do tipo string.
        - puts: exibe uma string seguida de nova linha.
        """
        comando = ctx.getChild(0).getText()
        
        if comando == "printf":
            string_literal = ctx.StringLiteral()
            if string_literal is None:
                raise Exception("Erro: Nenhum literal de string encontrado no printf.")
            
            formato = string_literal.getText().strip('"')
            formato = bytes(formato, "utf-8").decode("unicode_escape")
            
            argumentos = [self.visit(expr_ctx) for expr_ctx in ctx.expression()]
            try:
                mensagem = formato % tuple(argumentos)
            except TypeError as e:
                raise Exception(f"Erro: {e} - Verifique os argumentos do printf.")
            
            print(mensagem, end="")
        
        elif comando == "scanf":
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
                    elif tipo == "string":
                        valor = entrada
                    else:
                        raise Exception(f"Tipo '{tipo}' não suportado para entrada.")
                    self.tabela_simbolos.atualizar_variavel(nome, valor)
                except ValueError:
                    raise Exception(f"Erro: Valor '{entrada}' incompatível com o tipo '{tipo}'.")
        
        elif comando == "gets":
            # gets: gets '(' Identifier ')'
            # Use ctx.Identifier(0) para obter o identificador (pois ctx.Identifier() retorna uma lista)
            nome = ctx.Identifier(0).getText()
            var = self.tabela_simbolos.obter_variavel(nome, verificar_inicializacao=False)
            if var["tipo"] != "string":
                raise Exception(f"Erro: Variável '{nome}' não é do tipo string para o comando gets.")
            entrada = input()  # Lê uma linha completa
            self.tabela_simbolos.atualizar_variavel(nome, entrada)
        
        elif comando == "puts":
            # Trata o comando puts '(' (StringLiteral | expression) ')'
            # Como a gramática agora aceita ambos, usamos:
            s = self.visit(ctx.expression(0))
            if not isinstance(s, str):
                raise Exception("Erro: Valor passado para puts não é uma string.")
            print(s)

        





    

