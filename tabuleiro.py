class Tabuleiro:
    """Representa um tabuleiro de Sudoku 9x9 e sua dificuldade associada.

    Attributes:
        cores: Mapeamento de coordenadas (linha, coluna) para os valores
            preenchidos das células (1 a 9).
        dificuldade: Grau de dificuldade do tabuleiro.
    """

    _adjacencias = {}

    def __init__(self, cores, dificuldade):
        self.cores = cores
        self.dificuldade = dificuldade

    @classmethod
    def obter_adjacencias(cls) -> dict[tuple[int, int], set[tuple[int, int]]]:
        """
        Retorna o mapa fixo de vizinhos. Se ainda não existir, ele constrói
        uma única vez para toda a classe e guarda em cache.
        """
        if len(cls._adjacencias) == 0:
            cls._adjacencias = {}
            for r1 in range(9):
                for c1 in range(9):
                    vizinhos = set()
                    for r2 in range(9):
                        for c2 in range(9):
                            # Se não for a própria célula, checa as regras do Sudoku
                            if (r1, c1) != (r2, c2):
                                mesma_linha = (r1 == r2)
                                mesma_coluna = (c1 == c2)
                                mesmo_bloco = (r1 // 3 == r2 // 3) and (c1 // 3 == c2 // 3)

                                if mesma_linha or mesma_coluna or mesmo_bloco:
                                    vizinhos.add((r2, c2))

                    cls._adjacencias[(r1, c1)] = vizinhos

        return cls._adjacencias

    @classmethod
    def de_texto(cls, texto: str, dificuldade: float = -1.0):
        """Cria uma instância de Tabuleiro a partir de uma string de 81 caracteres.

        Args:
            texto: Sequência de 81 caracteres representando o tabuleiro, onde
                dígitos de '1' a '9' indicam células preenchidas e '.' células vazias.
            dificuldade: Nível de dificuldade do tabuleiro.

        Returns:
            Nova instância do tabuleiro configurada a partir do texto.

        Raises:
            TypeError: Se `texto` não for do tipo string.
            ValueError: Se `texto` não tiver exatamente 81 caracteres ou contiver
                caracteres inválidos.
        """
        if not isinstance(texto, str):
            raise TypeError("texto deve ser uma string.")

        if len(texto) != 81:
            raise ValueError(f"texto deve ter exatamente 81 caracteres, mas tem {len(texto)}.")

        for i, caractere in enumerate(texto):
            if caractere not in ".123456789":
                raise ValueError(
                    f"Caractere inválido '{caractere}' na posição {i}: "
                    "apenas dígitos de 1 a 9 ou '.' são permitidos."
                )

        cores: dict[tuple[int, int], int] = {}

        for i, caractere in enumerate(texto):
            if caractere != ".":
                linha = i // 9
                coluna = i % 9
                cores[(linha, coluna)] = int(caractere)

        return cls(cores, dificuldade)

    @classmethod
    def de_matriz(cls, matriz, dificuldade: float = -1.0):
        """Cria uma instância de Tabuleiro a partir de uma matriz 9x9.

        Args:
            matriz: Matriz bidimensional 9x9 contendo valores inteiros, onde 0
                representa células vazias e valores de 1 a 9 representam
                células preenchidas.
            dificuldade: Nível de dificuldade do tabuleiro.

        Returns:
            Nova instância do tabuleiro configurada a partir da matriz.

        Raises:
            ValueError: Se a matriz não possuir 9 linhas, se alguma linha não possuir
                9 colunas ou se algum valor não for um inteiro entre 0 e 9.
        """
        if len(matriz) != 9:
            raise ValueError(
                f"matriz deve ter exatamente 9 linhas, mas tem {len(matriz)}."
            )

        for i, linha in enumerate(matriz):
            if len(linha) != 9:
                raise ValueError(
                    f"Linha {i} deve ter exatamente 9 colunas, mas tem {len(linha)}."
                )
            for j, numero in enumerate(linha):
                if not isinstance(numero, int) or not (0 <= numero <= 9):
                    raise ValueError(
                        f"Valor inválido {numero!r} na posição ({i}, {j}): "
                        "deve ser um inteiro de 0 a 9."
                    )

        cores: dict[tuple[int, int], int] = {}

        for i, linha in enumerate(matriz):
            for j, numero in enumerate(linha):
                if numero != 0:
                    cores[(i, j)] = numero

        return cls(cores, dificuldade)

    def obter_vazias(self) -> list[tuple[int, int]]:
        """
        Lê o estado atual do jogo e retorna a lista de coordenadas
        das células sem cor.
        """
        vazias = []
        for i in range(9):
            for j in range(9):
                # Se a coordenada não está preenchida, ela precisa ser visitada
                if (i, j) not in self.cores:
                    vazias.append((i, j))
        return vazias

    def validar(self) -> bool:
        """Verifica se a configuração atual do tabuleiro é válida segundo as regras do Sudoku.

        Verifica se não há dígitos repetidos em nenhuma linha, em nenhuma
        coluna e em nenhuma das subgrades (seções) 3x3. Células vazias são ignoradas.

        Returns:
            True se o tabuleiro for válido, False caso contrário.
        """
        # Verificar linhas
        for i in range(9):
            vistos: set[int] = set()
            for j in range(9):
                valor = self.cores.get((i, j))
                if valor is None:
                    continue
                if valor in vistos:
                    return False
                vistos.add(valor)

        # Verificar colunas
        for j in range(9):
            vistos: set[int] = set()
            for i in range(9):
                valor = self.cores.get((i, j))
                if valor is None:
                    continue
                if valor in vistos:
                    return False
                vistos.add(valor)

        # Verificar seções 3×3
        for secao_linha in range(3):
            for secao_coluna in range(3):
                vistos: set[int] = set()
                for i in range(3):
                    for j in range(3):
                        linha = secao_linha * 3 + i
                        coluna = secao_coluna * 3 + j
                        valor = self.cores.get((linha, coluna))
                        if valor is None:
                            continue
                        if valor in vistos:
                            return False
                        vistos.add(valor)

        return True

    def __str__(self):
        resultado = ""

        for i in range(9):
            # Separação de seções por linha
            if i % 3 == 0 and i != 0:
                resultado += "- - - - - - - - - - - - - \n"

            for j in range(9):
                # Separação de seções por colunas
                if j % 3 == 0 and j != 0:
                    resultado += " | "

                valor = self.cores.get((i, j))
                resultado += str(valor) if valor is not None else "."
                resultado += " "

            # Quebra de linha ao fim de cada linha da matriz
            resultado += "\n"

        return resultado
