from tabuleiro import Tabuleiro

def backtracking(tabuleiro: Tabuleiro):
    vazias: list[tuple[int,int]] = tabuleiro.obter_vazias()
    dicionario_adjacencias: dict[tuple, set] = Tabuleiro.obter_adjacencias()
    total_vazias: int = len(vazias)

    def contar_candidatos(celula):
        cores_vizinhos = {tabuleiro.cores[v] for v in dicionario_adjacencias[celula] if v in tabuleiro.cores}
        return sum(1 for c in range(1, 10) if c not in cores_vizinhos)

    vazias.sort(key=contar_candidatos)

    i = 0
    while 0 <= i < total_vazias:
        celula = vazias[i]

        adjacentes: set[tuple[int, int]] = dicionario_adjacencias[celula]
        cores_adjacentes = {tabuleiro.cores[vizinho] for vizinho in adjacentes if vizinho in tabuleiro.cores}

        cores_adjacentes = set(cores_adjacentes)

        cor_atual = tabuleiro.cores.get(celula, 0)
        encontrou = False

        for cor in range(cor_atual + 1, 10):
            if cor not in cores_adjacentes:
                tabuleiro.cores[celula] = cor
                encontrou = True
                break

        if encontrou:
            i += 1
        else:
            tabuleiro.cores.pop(celula, None)
            i -= 1
