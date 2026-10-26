import time

from tabuleiro import Tabuleiro
import gerenciador_de_arquivos as ga
from backtracking import backtracking

if __name__ == "__main__":
    antes = time.time()
    tabuleiros_teste = ga.carregar_sudokus_csv("dados_limpos.csv", 100)
    print(time.time() - antes)
    antes = time.time()
    for tabuleiro in tabuleiros_teste:
        backtracking(tabuleiro)
    print(time.time() - antes)