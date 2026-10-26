import pandas as pd
from tabuleiro import Tabuleiro

def carregar_sudokus_csv(diretorio: str, quantidade = None, coluna_jogo: str = "puzzle",
                         coluna_dificuldade: str = "difficulty") -> list[Tabuleiro]:
    """Carrega tabuleiros de Sudoku a partir de um arquivo CSV.

    Lê o arquivo CSV informado e converte cada registro válido em uma
    instância da classe `Tabuleiro`.

    Args:
        diretorio: Caminho para o arquivo CSV contendo os dados dos sudokus.
        quantidade: Quantidade máxima de linhas a serem lidas do arquivo.
            Se for None, carrega todas as linhas.
        coluna_jogo: Nome da coluna contendo a representação em texto
            do tabuleiro (81 caracteres).
        coluna_dificuldade: Nome da coluna contendo a dificuldade do jogo.

    Returns:
        Lista de instâncias de `Tabuleiro` criadas a partir do CSV.
    """
    df = pd.read_csv(diretorio)

    if quantidade is not None:
        df = df.head(quantidade)

    permitidos = set(".123456789")

    tabuleiros: list[Tabuleiro] = []
    for _, linha in df.iterrows():
        jogo = str(linha[coluna_jogo]).strip()

        if len(jogo) == 81 and set(jogo).issubset(permitidos):
            dificuldade = -1.0
            if coluna_dificuldade in df.columns:
                try:
                    dificuldade = float(linha[coluna_dificuldade])
                except (ValueError, TypeError):
                    dificuldade = -1.0

            tabuleiro = Tabuleiro.de_texto(jogo, dificuldade=dificuldade)
            tabuleiros.append(tabuleiro)

    return tabuleiros

def carregar_sudokus_txt(diretorio: str, quantidade = None) -> list[Tabuleiro]:
    """Carrega tabuleiros de Sudoku a partir de um arquivo de texto (.txt).

    Lê o arquivo linha a linha e converte cada linha válida (com 81 caracteres
    formados por '.' e dígitos de 1 a 9) em uma instância de `Tabuleiro`.

    Args:
        diretorio: Caminho para o arquivo de texto (.txt).
        quantidade: Quantidade máxima de tabuleiros a serem carregados.
            Se for None, carrega todos os tabuleiros válidos.

    Returns:
        Lista de instâncias de `Tabuleiro` carregadas do arquivo.
    """
    tabuleiros: list[Tabuleiro] = []

    with open(diretorio, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            if quantidade is not None and len(tabuleiros) >= quantidade:
                break
            linha = linha.strip()
            permitidos = set(".123456789")
            if set(linha).issubset(permitidos) and len(linha) == 81:
                tabuleiro = Tabuleiro.de_texto(linha)
                tabuleiros.append(tabuleiro)
            else:
                print(f"Linha inválida no arquivo {arquivo.name}:", linha)
    return tabuleiros

def limpar_sudokus_csv(origem: str, destino: str, quantidade = None, coluna_jogo: str = "puzzle", coluna_dificuldade: str = "difficulty"):
    """Filtra um arquivo CSV mantendo apenas as colunas especificadas e salva o resultado.

    Lê o arquivo CSV original, seleciona apenas as colunas do jogo e da dificuldade,
    filtra a quantidade desejada de linhas e grava os dados em um novo arquivo CSV de destino.

    Args:
        origem: Caminho do arquivo CSV de origem.
        destino: Caminho do arquivo CSV de destino onde os dados filtrados serão salvos.
        quantidade: Quantidade de linhas que devem restar
        coluna_jogo: Nome da coluna de jogo.
        coluna_dificuldade: Nome da coluna de dificuldade.
    """
    df = pd.read_csv(origem)

    df = df[[coluna_jogo, coluna_dificuldade]].copy()

    if quantidade is not None:
        df = df.head(quantidade)

    df.to_csv(destino, index=False)