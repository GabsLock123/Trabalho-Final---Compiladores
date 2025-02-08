class TabelaSimbolos:
    def __init__(self):
        self.variaveis = {}
        self.macros = {}
        self.structs = {}

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
        """
        Retorna os detalhes de uma variável.
        - Se verificar_inicializacao=True, valida se a variável foi inicializada.
        """
        if nome not in self.variaveis:
            raise Exception(f"Variável '{nome}' não foi declarada.")
        if verificar_inicializacao and not self.variaveis[nome]["inicializada"]:
            raise Exception(f"Erro: Variável '{nome}' não foi inicializada antes do uso.")
        return self.variaveis[nome]

    def atualizar_variavel(self, nome, valor):
        if nome not in self.variaveis:
            raise Exception(f"Variável '{nome}' não foi declarada.")
        self.variaveis[nome]["valor"] = valor
        self.variaveis[nome]["inicializada"] = True  # Marca como inicializada

    def adicionar_struct(self, nome_struct, campos):
        """
        Armazena a definição de uma struct (nome e dicionário de {campo: tipoCampo}).
        """
        if nome_struct in self.structs:
            raise Exception(f"A struct '{nome_struct}' já foi definida.")
        self.structs[nome_struct] = campos

    def obter_struct(self, nome_struct):
        """
        Retorna o dicionário de campos da struct ou None se não existir.
        """
        return self.structs.get(nome_struct, None)