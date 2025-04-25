"""
- Marcelo Wzorek Filho
"""

class AnalisadorSintatico:
    def __init__(self, lexador):
        self.lexador = lexador
        self.token_atual = None
        self.avancar_token()

    def avancar_token(self):
        try:
            self.token_atual = self.lexador.obter_proximo_token()
        except ValueError as e:
            self.token_atual = None
            raise e

    def analisar(self):
        try:
            self.analisar_formula()
            if self.token_atual is not None:
                raise ValueError("Tokens extras após a fórmula")
            return True
        except ValueError:
            return False

    def analisar_formula(self):
        if self.token_atual is None:
            raise ValueError("Fórmula incompleta")

        tipo_token, _ = self.token_atual

        if tipo_token in ["CONSTANTE", "PROPOSICAO"]:
            self.avancar_token()
        elif tipo_token == "ABRE_PARENTESE":
            self.avancar_token()
            if self.token_atual is None:
                raise ValueError("Fórmula incompleta após '('")

            tipo_op = self.token_atual[0]
            if tipo_op == "OPERATOR_UNARIO":
                self.avancar_token()
                self.analisar_formula()
            elif tipo_op == "OPERATOR_BINARIO":
                self.avancar_token()
                self.analisar_formula()
                self.analisar_formula()
            else:
                raise ValueError(f"Operador inválido após '(': {self.token_atual}")

            if self.token_atual is None or self.token_atual[0] != "FECHA_PARENTESE":
                raise ValueError("Esperado ')'")
            self.avancar_token()
        else:
            raise ValueError(f"Token inesperado: {self.token_atual}")
