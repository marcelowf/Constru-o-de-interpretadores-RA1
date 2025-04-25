"""
- Marcelo Wzorek Filho
"""

class Lexador:
    def __init__(self, cadeia_entrada):
        self.cadeia_entrada = cadeia_entrada
        self.posicao = 0
        self.char_atual = (
            self.cadeia_entrada[self.posicao]
            if self.posicao < len(self.cadeia_entrada)
            else None
        )

    def avancar(self):
        self.posicao += 1
        if self.posicao < len(self.cadeia_entrada):
            self.char_atual = self.cadeia_entrada[self.posicao]
        else:
            self.char_atual = None

    def ignorar_espaco(self):
        while self.char_atual is not None and self.char_atual.isspace():
            self.avancar()

    def obter_proximo_token(self):
        while self.char_atual is not None:
            if self.char_atual.isspace():
                self.ignorar_espaco()
                continue

            if self.char_atual == "(":
                self.avancar()
                return ("ABRE_PARENTESE", "(")
            elif self.char_atual == ")":
                self.avancar()
                return ("FECHA_PARENTESE", ")")
            elif self.char_atual == "\\":
                return self.processar_operador()
            elif self.char_atual == "t":
                return self.processar_true()
            elif self.char_atual == "f":
                return self.processar_false()
            elif self.char_atual == "P":
                return self.processar_proposicao()
            else:
                raise ValueError(f"Caractere inválido: {self.char_atual}")
        return None

    def processar_operador(self):
        self.avancar()
        operador = []
        while self.char_atual is not None and self.char_atual.isalpha():
            operador.append(self.char_atual)
            self.avancar()
        operador_str = "".join(operador)

        unarios = {"neg": "OPERATOR_UNARIO"}
        binarios = {
            "wedge": "OPERATOR_BINARIO",
            "vee": "OPERATOR_BINARIO",
            "rightarrow": "OPERATOR_BINARIO",
            "leftrightarrow": "OPERATOR_BINARIO",
        }

        if operador_str in unarios:
            return (unarios[operador_str], f"\\{operador_str}")
        elif operador_str in binarios:
            return (binarios[operador_str], f"\\{operador_str}")
        else:
            raise ValueError(f"Operador inválido: \\{operador_str}")

    def processar_true(self):
        self.avancar()
        for c in "rue":
            if self.char_atual != c:
                raise ValueError("Constante 'true' inválida")
            self.avancar()
        return ("CONSTANTE", "true")

    def processar_false(self):
        self.avancar()
        for c in "alse":
            if self.char_atual != c:
                raise ValueError("Constante 'false' inválida")
            self.avancar()
        return ("CONSTANTE", "false")

    def processar_proposicao(self):
        self.avancar()
        if self.char_atual is None or not self.char_atual.isdigit():
            raise ValueError(
                "Proposição inválida: deve haver pelo menos um dígito após 'P'"
            )
        proposicao = ["P"]
        while self.char_atual is not None and self.char_atual.isdigit():
            proposicao.append(self.char_atual)
            self.avancar()
        return ("PROPOSICAO", "".join(proposicao))
