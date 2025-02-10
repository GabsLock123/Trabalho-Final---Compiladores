from CVisitor import CVisitor
from CParser import CParser
from tabela_simbolos import TabelaSimbolos

class BreakException(Exception):
    pass

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class Interpretador(CVisitor):
    def __init__(self):
        self.tabela_simbolos = TabelaSimbolos()
        self.funcoes = {}  

    def visitInitializerList(self, ctx):
        valores = []
        for expr in ctx.expression():
            valores.append(self.visit(expr))
        return valores

    def visitInit(self, ctx):
        if ctx.initializerList() is not None:
            return self.visit(ctx.initializerList())
        elif ctx.expression() is not None:
            return self.visit(ctx.expression())
        else:
            return None

    def visitStatement(self, ctx):
        if ctx.getChild(0).getText() == "return":
            return self.visitReturnStatement(ctx)
        return self.visitChildren(ctx)

    def visitReturnStatement(self, ctx):
        expr = ctx.expression()
        if expr:
            if isinstance(expr, list):
                value = self.visit(expr[0])
            else:
                value = self.visit(expr)
        else:
            value = None
        raise ReturnException(value)

    def visitFunctionDef(self, ctx):
        tipo = ctx.type_().getText()         
        nome = ctx.Identifier().getText()
        self.funcoes[nome] = ctx
        return None

    def visitFunctionCall(self, ctx):
        nome = ctx.Identifier().getText()
        if nome not in self.funcoes:
            raise Exception(f"Função '{nome}' não foi definida.")
        funcDefCtx = self.funcoes[nome]

        arg_values = []
        if ctx.argumentList() is not None:
            expr_list = ctx.argumentList().expression()
            if not isinstance(expr_list, list):
                expr_list = [expr_list]
            for expr in expr_list:
                arg_values.append(self.visit(expr))
        
        param_names = []
        if funcDefCtx.paramList() is not None:
            id_list = funcDefCtx.paramList().Identifier()
            if not isinstance(id_list, list):
                id_list = [id_list]
            for token in id_list:
                param_names.append(token.getText())
        
        if len(param_names) != len(arg_values):
            raise Exception(f"Função '{nome}' espera {len(param_names)} parâmetros, mas {len(arg_values)} foram passados.")
        
        old_tabela = self.tabela_simbolos
        self.tabela_simbolos = TabelaSimbolos(parent=old_tabela)
        self.tabela_simbolos.structs = old_tabela.structs
        self.tabela_simbolos.unions = old_tabela.unions
        
        param_types = []
        if funcDefCtx.paramList() is not None:
            t = funcDefCtx.paramList().type_()
            if isinstance(t, list):
                param_types = [tipo.getText() for tipo in t]
            else:
                param_types = [t.getText()]
        
        for i, param in enumerate(param_names):
            param_type = param_types[i] if i < len(param_types) else "int"
            self.tabela_simbolos.adicionar_variavel(param, param_type, arg_values[i])

        try:
            self.visit(funcDefCtx.block())
            ret_value = None  
        except ReturnException as re:
            ret_value = re.value
        
        tipo_funcao = funcDefCtx.type_().getText()
        if ret_value is None and tipo_funcao != "void":
            if tipo_funcao == "int":
                ret_value = 0
            elif tipo_funcao in ["float", "double"]:
                ret_value = 0.0
            elif tipo_funcao == "char":
                ret_value = '\0'
            else:
                ret_value = None  
        
        self.tabela_simbolos = old_tabela
        return ret_value

    def visitDirective(self, ctx):
        directive_type = ctx.getChild(0).getText()  
        
        if directive_type == '#include':
            included_file = ctx.IncludeFile().getText()  
            included_file = included_file.strip('<>"')   

        elif directive_type == '#define':
            macro_name = ctx.Identifier().getText()
            macro_value = self.visit(ctx.expression()) if ctx.expression() else None
            self.tabela_simbolos.adicionar_macro(macro_name, macro_value)

    def visitStructDef(self, ctx):
        nome_struct = ctx.Identifier().getText()

        campos = {}

        for vd in ctx.varDecl():
            tipo_campo = vd.type_().getText()        
            nome_campo = vd.Identifier().getText()   
            if nome_campo in campos:
                raise Exception(f"Campo '{nome_campo}' duplicado na struct '{nome_struct}'.")
            campos[nome_campo] = tipo_campo

        self.tabela_simbolos.adicionar_struct(nome_struct, campos)

    def visitUnionDef(self, ctx):

        nome_union = ctx.Identifier().getText()
        campos = {}
        for vd in ctx.varDecl():
            tipo_campo = vd.type_().getText()        
            nome_campo = vd.Identifier().getText()    
            if nome_campo in campos:
                raise Exception(f"Campo '{nome_campo}' duplicado na union '{nome_union}'.")
            campos[nome_campo] = tipo_campo
        self.tabela_simbolos.adicionar_union(nome_union, campos)

    def visitVarDecl(self, ctx):
        tipo = ctx.type_().getText()  
        nome = ctx.Identifier().getText()

        if nome in self.tabela_simbolos.variaveis:
            raise Exception(f"Variável '{nome}' já foi declarada.")

        is_array = False
        tam_array = None
        if ctx.arraySize():
            is_array = True

            if ctx.arraySize().Number() is not None:
                size_text = ctx.arraySize().Number().getText()
                tam_array = int(size_text)

        valor_inicial = None
        inicializada = False
        if ctx.init():
            valor_inicial = self.visit(ctx.init())
            inicializada = True

        if is_array:
            tipo_array = tipo + "[]"

            if tipo == "char" and isinstance(valor_inicial, str):
                if tam_array is not None:
                    if len(valor_inicial) > tam_array:
                        raise Exception(f"A string fornecida para '{nome}' é maior que o tamanho do array ({tam_array}).")
                    array_val = list(valor_inicial) + ['\0'] * (tam_array - len(valor_inicial))
                else:
                    tam_array = len(valor_inicial) + 1
                    array_val = list(valor_inicial) + ['\0']
            elif valor_inicial is not None:
                if isinstance(valor_inicial, list):
                    if tam_array is not None and len(valor_inicial) != tam_array:
                        raise Exception(
                            f"O número de elementos na inicialização de '{nome}' ({len(valor_inicial)}) "
                            f"não corresponde ao tamanho declarado ({tam_array})."
                        )
                    if tam_array is None:
                        tam_array = len(valor_inicial)
                    array_val = []
                    for i, elem in enumerate(valor_inicial):
                        array_val.append(self._verificar_tipo_e_converter(tipo, elem, f"{nome}[{i}]"))
                else:
                    if tam_array is None:
                        raise Exception(f"Array '{nome}' sem tamanho definido deve ser inicializado com uma lista de valores.")
                    valor_convertido = self._verificar_tipo_e_converter(tipo, valor_inicial, f"{nome}[all]")
                    array_val = [valor_convertido for _ in range(tam_array)]
            else:
                if tam_array is None:
                    raise Exception(f"Array '{nome}' sem tamanho definido deve ser inicializado.")
                array_val = [None] * tam_array

            self.tabela_simbolos.adicionar_variavel(nome, tipo_array, array_val)
            status = "inicializada" if inicializada else "não inicializada"

        elif tipo.startswith("struct"):
            nome_struct = tipo[len("struct"):].strip()
            definicao_struct = self.tabela_simbolos.obter_struct(nome_struct)
            if definicao_struct is None:
                raise Exception(f"Struct '{nome_struct}' não foi definida antes de criar '{nome}'.")
            campos_iniciais = {}
            for campo, tipo_campo in definicao_struct.items():
                campos_iniciais[campo] = {"tipo": tipo_campo, "valor": None}
            struct_valor = {"__struct_name__": nome_struct, "campos": campos_iniciais}
            inicializada = True  
            self.tabela_simbolos.adicionar_variavel(nome, tipo, struct_valor)
            status = "inicializada"

        elif tipo.startswith("union"):
            nome_union = tipo[len("union"):].strip()
            definicao_union = self.tabela_simbolos.obter_union(nome_union)
            if definicao_union is None:
                raise Exception(f"Union '{nome_union}' não foi definida antes de criar '{nome}'.")
            campos_iniciais = {}
            for campo, tipo_campo in definicao_union.items():
                campos_iniciais[campo] = {"tipo": tipo_campo, "valor": None}
            union_val = {"__union_name__": nome_union, "active_field": None, "fields": campos_iniciais}
            if ctx.init():
                raise Exception("Inicialização de union não suportada diretamente; use a atribuição de campo (ex.: u.campo = valor).")
            self.tabela_simbolos.adicionar_variavel(nome, tipo, union_val)
        else:
            valor = None
            if valor_inicial is not None:
                valor = self._verificar_tipo_e_converter(tipo, valor_inicial, nome)
                inicializada = True
            self.tabela_simbolos.adicionar_variavel(nome, tipo, valor)
            status = "inicializada" if inicializada else "não inicializada"

    def _verificar_tipo_e_converter(self, tipo_variavel, valor, nome_alvo):
        if tipo_variavel == "int":
            if isinstance(valor, int):
                return valor
            elif isinstance(valor, float):
                print(f"Aviso: Conversão implícita de FLOAT para INT ao atribuir '{valor}' à '{nome_alvo}'.")
                return int(valor)
            else:
                raise Exception(f"Erro: Valor '{valor}' incompatível com o tipo INT de '{nome_alvo}'.")

        elif tipo_variavel in ["float", "double"]:
            if isinstance(valor, (int, float)):
                return float(valor)
            else:
                raise Exception(f"Erro: Valor '{valor}' incompatível com o tipo {tipo_variavel.upper()} de '{nome_alvo}'.")

        elif tipo_variavel == "char":
            if isinstance(valor, str) and len(valor) == 1:
                return valor
            else:
                raise Exception(f"Erro: Valor '{valor}' incompatível com o tipo CHAR de '{nome_alvo}'.")

        elif tipo_variavel in ["short", "long", "unsigned", "unsigned int", "unsigned long", "long long"]:
            if isinstance(valor, int):
                return valor
            elif isinstance(valor, float):
                print(f"Aviso: Conversão implícita de FLOAT para INT ao atribuir '{valor}' à '{nome_alvo}'.")
                return int(valor)
            else:
                raise Exception(f"Erro: Valor '{valor}' incompatível com o tipo {tipo_variavel.upper()} de '{nome_alvo}'.")

        elif tipo_variavel.startswith("struct"):
            if isinstance(valor, dict) and "campos" in valor:
                return valor
            else:
                raise Exception(f"Erro: Tentando atribuir valor não-struct a um struct '{nome_alvo}'.")
        else:
            return valor


    def visitAssignment(self, ctx):
        child_count = ctx.getChildCount()

        if (child_count >= 6 
            and ctx.getChild(1).getText() == '[' 
            and ctx.getChild(3).getText() == ']' 
            and ctx.getChild(4).getText() == '='):
            
            array_name = ctx.getChild(0).getText()
            index_expr_ctx = ctx.getChild(2)
            valor_expr_ctx = ctx.getChild(5)

            index_value = self.visit(index_expr_ctx)
            valor = self.visit(valor_expr_ctx)

            arr_var = self.tabela_simbolos.obter_variavel(array_name, verificar_inicializacao=True)
            if not arr_var["tipo"].endswith("[]"):
                raise Exception(f"Variável '{array_name}' não é um array, mas foi usada como array.")
            
            if not isinstance(index_value, int):
                raise Exception(f"Índice do array '{array_name}' não é inteiro: {index_value}")

            array_data = arr_var["valor"]
            if index_value < 0 or index_value >= len(array_data):
                raise Exception(f"Índice {index_value} fora dos limites do array '{array_name}'.")

            tipo_base = arr_var["tipo"][:-2]
            valor_convertido = self._verificar_tipo_e_converter(tipo_base, valor, f"{array_name}[{index_value}]")
            array_data[index_value] = valor_convertido
            self.tabela_simbolos.atualizar_variavel(array_name, array_data)
            return

        left_side_tokens = []
        i = 0
        while ctx.getChild(i).getText() != '=':
            left_side_tokens.append(ctx.getChild(i).getText())
            i += 1

        valor = self.visit(ctx.expression(0))

        if len(left_side_tokens) == 1:
            nome_var = left_side_tokens[0]
            variavel = self.tabela_simbolos.obter_variavel(nome_var, verificar_inicializacao=False)
            tipo_variavel = variavel["tipo"]

            if tipo_variavel.startswith("union"):
                raise Exception("Atribuição direta de union não permitida; use a atribuição de campo (ex.: u.campo = valor).")

            valor_convertido = self._verificar_tipo_e_converter(tipo_variavel, valor, nome_var)
            self.tabela_simbolos.atualizar_variavel(nome_var, valor_convertido)
        else:
            identifiers = [token for token in left_side_tokens if token != '.']
            nome_var = identifiers[0]
            variavel = self.tabela_simbolos.obter_variavel(nome_var, verificar_inicializacao=True)
            tipo_variavel = variavel["tipo"]

            if tipo_variavel.startswith("struct"):
                struct_value = variavel["valor"]
                if not isinstance(struct_value, dict) or "campos" not in struct_value:
                    raise Exception(f"Tentando acessar campo de algo que não é struct: '{nome_var}'.")
                campos = struct_value["campos"]
                for idx in range(1, len(identifiers)):
                    nome_campo = identifiers[idx]
                    if idx == len(identifiers) - 1:
                        if nome_campo not in campos:
                            raise Exception(f"O campo '{nome_campo}' não existe na struct '{struct_value['__struct_name__']}'.")
                        tipo_campo = campos[nome_campo]["tipo"]
                        valor_convertido = self._verificar_tipo_e_converter(tipo_campo, valor, f"{nome_var}.{nome_campo}")
                        campos[nome_campo]["valor"] = valor_convertido
                    else:
                        if nome_campo not in campos:
                            raise Exception(f"O campo '{nome_campo}' não existe na struct '{struct_value['__struct_name__']}'.")
                        subvalor = campos[nome_campo]["valor"]
                        if not (isinstance(subvalor, dict) and "campos" in subvalor):
                            raise Exception(f"O campo '{nome_campo}' não é um sub-struct.")
                        struct_value = subvalor
                        campos = subvalor["campos"]

            elif tipo_variavel.startswith("union"):
                union_value = variavel["valor"]
                if not (isinstance(union_value, dict) and "fields" in union_value and "active_field" in union_value):
                    raise Exception(f"Tentando acessar campo de algo que não é union: '{nome_var}'.")
                if len(identifiers) != 2:
                    raise Exception("Acesso a sub-campos de union não suportado.")
                nome_campo = identifiers[1]
                fields = union_value["fields"]
                if nome_campo not in fields:
                    raise Exception(f"O campo '{nome_campo}' não existe na union '{union_value['__union_name__']}'.")
                tipo_campo = fields[nome_campo]["tipo"]
                valor_convertido = self._verificar_tipo_e_converter(tipo_campo, valor, f"{nome_var}.{nome_campo}")
                fields[nome_campo]["valor"] = valor_convertido
                union_value["active_field"] = nome_campo

            else:
                raise Exception("Atribuição inválida: acesso a campo apenas para structs e unions.")

    def visitExpression(self, ctx):
        child_count = ctx.getChildCount()

        if child_count == 1 and ctx.getChild(0).__class__.__name__ == "FunctionCallContext":
            return self.visit(ctx.getChild(0))
    
        if ctx.getChildCount() == 1 and ctx.Identifier():
            ident = ctx.Identifier().getText()
            macro_val = self.tabela_simbolos.obter_macro(ident)
            if macro_val is not None:
                return macro_val
            return self.tabela_simbolos.obter_variavel(ident, verificar_inicializacao=True)["valor"]

        if child_count == 3 and ctx.getChild(1).getText() == '.':
            left_value = self.visit(ctx.getChild(0))
            field_name = ctx.getChild(2).getText()
            if isinstance(left_value, dict):
                if "campos" in left_value:
                    campos = left_value["campos"]
                    if field_name not in campos:
                        raise Exception(f"O campo '{field_name}' não existe na struct '{left_value['__struct_name__']}'.")
                    return campos[field_name]["valor"]
                elif "fields" in left_value and "active_field" in left_value:
                    if left_value["active_field"] is None:
                        raise Exception(f"Union '{left_value['__union_name__']}' não foi inicializada (nenhum campo atribuído).")
                    if field_name != left_value["active_field"]:
                        raise Exception(f"Tentando acessar o campo '{field_name}' de union '{left_value['__union_name__']}' que não é o campo ativo.")
                    return left_value["fields"][field_name]["valor"]
                else:
                    raise Exception(f"Tentando acessar campo '{field_name}' de algo que não é struct ou union.")
            else:
                raise Exception("Operação de acesso a campo em valor não estruturado.")

        if child_count == 3:
            op = ctx.getChild(1).getText()
            if op in ['+', '-', '*', '/', '%', '&&', '||', '>', '<', '>=', '<=', '==', '!=']:
                left = self.visit(ctx.expression(0))
                right = self.visit(ctx.expression(1))
                if op == '+':
                    return left + right
                elif op == '-':
                    return left - right
                elif op == '*':
                    return left * right
                elif op == '/':
                    return left / right
                elif op == '%':
                    return left % right
                elif op == '&&':
                    return bool(left and right)
                elif op == '||':
                    return bool(left or right)
                elif op == '>':
                    return left > right
                elif op == '<':
                    return left < right
                elif op == '>=':
                    return left >= right
                elif op == '<=':
                    return left <= right
                elif op == '==':
                    return left == right
                elif op == '!=':
                    return left != right

        if (child_count == 4 and ctx.getChild(0).getSymbol() is not None 
            and ctx.getChild(1).getText() == '[' and ctx.getChild(3).getText() == ']'):
            array_name = ctx.getChild(0).getText()
            index_value = self.visit(ctx.getChild(2))
            arr_var = self.tabela_simbolos.obter_variavel(array_name, verificar_inicializacao=True)
            if not arr_var["tipo"].endswith("[]"):
                raise Exception(f"Variável '{array_name}' não é um array, mas foi usada como array.")
            if not isinstance(index_value, int):
                raise Exception(f"Índice do array '{array_name}' não é inteiro: {index_value}")
            array_data = arr_var["valor"]
            if index_value < 0 or index_value >= len(array_data):
                raise Exception(f"Índice {index_value} fora dos limites do array '{array_name}'.")
            return array_data[index_value]

        if ctx.Number():
            valor = ctx.Number().getText()
            return float(valor) if '.' in valor else int(valor)

        if ctx.StringLiteral():
            s = ctx.StringLiteral().getText().strip('"')
            return bytes(s, "utf-8").decode("unicode_escape")

        if ctx.CharLiteral():
            return ctx.CharLiteral().getText().strip("'")

        if child_count == 3 and ctx.getChild(0).getText() == '(' and ctx.getChild(2).getText() == ')':
            return self.visit(ctx.getChild(1))

        if child_count == 2:
            first_char = ctx.getChild(0).getText()
            if first_char == '!':
                return not self.visit(ctx.getChild(1))
            elif first_char == '-':
                return -self.visit(ctx.getChild(1))

        if child_count == 1 and ctx.Identifier():
            return self.tabela_simbolos.obter_variavel(ctx.Identifier().getText(), verificar_inicializacao=True)["valor"]
        return None

    def visitIfStatement(self, ctx):
        condicao = self.visit(ctx.expression()) 

        if condicao:
            self.visit(ctx.statement(0))
        elif ctx.statement(1):
            self.visit(ctx.statement(1))

    def visitSwitchStatement(self, ctx):
        valor_switch = self.visit(ctx.expression()) 

        caso_executado = False

        for case in ctx.caseBlock():
            case_expr = self.visit(case.caseLabel().expression())  
            if valor_switch == case_expr:
                caso_executado = True  

                try:
                    for stmt in case.statement():
                        self.visit(stmt)
                except BreakException:
                    return  

        if not caso_executado:
            for default in ctx.defaultBlock():
                for stmt in default.statement():
                    self.visit(stmt)

    def visitWhileStatement(self, ctx):

        while True:
            condicao = self.visit(ctx.expression())  

            if not condicao:  
                break

            try:
                self.visit(ctx.statement())
            except BreakException:
                break

    def visitBreakStatement(self, ctx):
        raise BreakException()

    def visitDoWhileStatement(self, ctx):
        while True:
            try:
                self.visit(ctx.statement())
            except BreakException:
                break

            condicao = self.visit(ctx.expression())

            if not condicao:
                break

    def visitForHeaderAssignment(self, ctx):
            var_name = ctx.Identifier().getText()
            valor = self.visit(ctx.expression())
            self.tabela_simbolos.atualizar_variavel(var_name, valor)

    def visitForStatement(self, ctx):
        if ctx.varDecl() is not None:
            self.visit(ctx.varDecl())
        elif ctx.forHeaderAssignment() is not None:
            inits = ctx.forHeaderAssignment()
            if isinstance(inits, list):
                self.visit(inits[0])
            else:
                self.visit(inits)
        
        if ctx.expression() is not None:
            condition = self.visit(ctx.expression())
        else:
            condition = True  

        update_assignment = None
        if ctx.forHeaderAssignment() is not None:
            headers = ctx.forHeaderAssignment()
            if isinstance(headers, list) and len(headers) >= 2:
                update_assignment = headers[1]
        
        while condition:
            try:
                self.visit(ctx.statement())
            except BreakException:
                break

            if update_assignment is not None:
                self.visit(update_assignment)

            if ctx.expression() is not None:
                condition = self.visit(ctx.expression())
            else:
                condition = True

    def visitInputOutputStatement(self, ctx):
        comando = ctx.getChild(0).getText()
        
        if comando == "printf":
            string_literal = ctx.StringLiteral()
            if string_literal is None:
                raise Exception("Erro: Nenhum literal de string encontrado no printf.")
            
            formato = string_literal.getText().strip('"')
            formato = bytes(formato, "utf-8").decode("unicode_escape")
            
            argumentos = [self.visit(expr_ctx) for expr_ctx in ctx.expression()]
            for i, arg in enumerate(argumentos):
                if isinstance(arg, list) and len(arg) > 0 and all(isinstance(ch, str) and len(ch) == 1 for ch in arg):
                    argumentos[i] = "".join(arg)
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
            num_especificadores = len(formato.split("%")) - 1
            parametros = ctx.scanfParam()
            if not isinstance(parametros, list):
                parametros = [parametros]
            if len(parametros) != num_especificadores:
                raise Exception("Erro: Número de variáveis não corresponde ao formato.")
            
            for param in parametros:
                if param.getChildCount() == 1:
                    nome = param.getChild(0).getText()
                    var = self.tabela_simbolos.obter_variavel(nome, verificar_inicializacao=False)
                    tipo = var["tipo"]
                    if tipo.endswith("[]"):
                        base_tipo = tipo[:-2]
                        tamanho = len(var["valor"])
                        if base_tipo == "char":
                            entrada = input()
                            if len(entrada) > tamanho:
                                raise Exception(f"A string digitada excede o tamanho do array '{nome}'.")
                            novo_valor = list(entrada) + ['\0'] * (tamanho - len(entrada))
                            self.tabela_simbolos.atualizar_variavel(nome, novo_valor)
                        else:
                            entrada = input()
                            tokens = entrada.split()
                            if len(tokens) != tamanho:
                                raise Exception(f"Erro: Esperados {tamanho} valores para o array '{nome}', mas foram recebidos {len(tokens)}.")
                            novo_array = []
                            for j, token in enumerate(tokens):
                                try:
                                    if base_tipo == "int":
                                        valor_elem = int(token)
                                    elif base_tipo in ["float", "double"]:
                                        valor_elem = float(token)
                                    else:
                                        raise Exception(f"Tipo '{base_tipo}' não suportado para entrada.")
                                except ValueError:
                                    raise Exception(f"Erro: Valor '{token}' incompatível com o tipo '{base_tipo}'.")
                                novo_array.append(valor_elem)
                            self.tabela_simbolos.atualizar_variavel(nome, novo_array)
                    else:
                        entrada = input()
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
                else:
                    nome = param.getChild(0).getText()
                    var = self.tabela_simbolos.obter_variavel(nome, verificar_inicializacao=False)
                    tipo = var["tipo"]
                    if not tipo.endswith("[]"):
                        raise Exception(f"Variável '{nome}' não é um array, mas foi usada com indexação no scanf.")
                    index_expr = param.getChild(2)
                    index_value = self.visit(index_expr)
                    base_tipo = tipo[:-2]
                    entrada = input()
                    try:
                        if base_tipo == "int":
                            valor = int(entrada)
                        elif base_tipo in ["float", "double"]:
                            valor = float(entrada)
                        elif base_tipo == "char":
                            valor = entrada[0]
                        else:
                            raise Exception(f"Tipo '{base_tipo}' não suportado para entrada.")
                        array_data = var["valor"]
                        if index_value < 0 or index_value >= len(array_data):
                            raise Exception(f"Índice {index_value} fora dos limites do array '{nome}'.")
                        array_data[index_value] = valor
                        self.tabela_simbolos.atualizar_variavel(nome, array_data)
                    except ValueError:
                        raise Exception(f"Erro: Valor '{entrada}' incompatível com o tipo '{base_tipo}'.")
        
        elif comando == "gets":
            ids = ctx.Identifier()
            if isinstance(ids, list):
                nome = ids[0].getText()
            else:
                nome = ids.getText()
            var = self.tabela_simbolos.obter_variavel(nome, verificar_inicializacao=False)
            if not var["tipo"].endswith("[]") or not var["tipo"].startswith("char"):
                raise Exception(f"Erro: Variável '{nome}' não é um array de char para o comando gets.")
            entrada = input()
            tamanho = len(var["valor"])
            if len(entrada) > tamanho:
                entrada = entrada[:tamanho]
            else:
                entrada = entrada + '\0' * (tamanho - len(entrada))
            self.tabela_simbolos.atualizar_variavel(nome, list(entrada))
        
        elif comando == "puts":
            s = self.visit(ctx.expression(0))
            if isinstance(s, list) and len(s) > 0 and all(isinstance(ch, str) and len(ch)==1 for ch in s):
                s = "".join(s)
            if not isinstance(s, str):
                raise Exception("Erro: Valor passado para puts não é uma string.")
            print(s)
