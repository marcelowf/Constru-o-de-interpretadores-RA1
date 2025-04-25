"""
- Marcelo Wzorek Filho
"""

import os
import sys

from Lexer import Lexador
from Parser import AnalisadorSintatico

def selecionar_arquivo():
    print(
        "(1) Arquivo de Teste 1 (Todo válido)\n"
        "(2) Arquivo de Teste 2 (Todo inválido)\n"
        "(3) Arquivo de Teste 3 (Arquivo misto)\n"
        "(4) Usar outro arquivo"
    )

    arquivos = {
        "1": "files/test_valid.txt",
        "2": "files/test_invalid.txt",
        "3": "files/test_mixed.txt",
    }

    opcao = input("Escolha uma opção: ")
    if opcao in arquivos:
        caminho = arquivos[opcao]
    else:
        nome_arquivo = input(
            "Digite o nome do arquivo (já na pasta files, inclua a extensão): "
        )
        caminho = f"files/{nome_arquivo}"
        if not os.path.exists(caminho):
            print("Arquivo não encontrado")
            sys.exit(1)

    return caminho

def main():
    caminho = selecionar_arquivo()
    print("Arquivo selecionado:", caminho)

    with open(caminho, "r", encoding="utf-8") as arquivo:
        linhas = arquivo.read().splitlines()

    quantidade = int(linhas[0])
    expressoes = linhas[1 : quantidade + 1]

    for expressao in expressoes:
        expressao = expressao.strip()
        valida = False
        try:
            lexador = Lexador(expressao)
            analisador = AnalisadorSintatico(lexador)
            valida = analisador.analisar()
        except ValueError:
            valida = False

        print("válida" if valida else "inválida")

if __name__ == "__main__":
    main()