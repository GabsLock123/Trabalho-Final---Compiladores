class TabelaSimbolos:
    def __init__(self, parent=None):
        self.variaveis = {}
        self.macros = {}
        self.structs = {}
        self.unions = {}
        self.parent = parent

    def adicionar_macro(self, nome, valor):
        self.macros[nome] = valor

    def obter_macro(self, nome):
        return self.macros.get(nome, None)

    def adicionar_variavel(self, nome, tipo, valor=None):
        if nome in self.variaveis:
            raise Exception(f"Variável '{nome}' já foi declarada.")
        self.variaveis[nome] = {
            "tipo": tipo,
            "valor": valor,
            "inicializada": valor is not None
        }

    def obter_variavel(self, nome, verificar_inicializacao=True):
        if nome in self.variaveis:
            var = self.variaveis[nome]
            if verificar_inicializacao and not var["inicializada"]:
                raise Exception(f"Erro: Variável '{nome}' não foi inicializada antes do uso.")
            return var
        elif self.parent is not None:
            return self.parent.obter_variavel(nome, verificar_inicializacao)
        else:
            raise Exception(f"Variável '{nome}' não foi declarada.")

    def atualizar_variavel(self, nome, valor):
        if nome in self.variaveis:
            self.variaveis[nome]["valor"] = valor
            self.variaveis[nome]["inicializada"] = True
        elif self.parent is not None:
            self.parent.atualizar_variavel(nome, valor)
        else:
            raise Exception(f"Variável '{nome}' não foi declarada.")

    def adicionar_struct(self, nome_struct, campos):
        if nome_struct in self.structs:
            raise Exception(f"A struct '{nome_struct}' já foi definida.")
        self.structs[nome_struct] = campos

    def obter_struct(self, nome_struct):
        return self.structs.get(nome_struct, None)
    
    def adicionar_union(self, nome_union, campos):
        if nome_union in self.unions:
            raise Exception(f"A union '{nome_union}' já foi definida.")
        self.unions[nome_union] = campos

    def obter_union(self, nome_union):
        return self.unions.get(nome_union, None)
