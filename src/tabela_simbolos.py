class TabelaSimbolos:
    def __init__(self):
        self.variaveis = {}
        self.macros = {}

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
