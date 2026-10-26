import pytest

from tabuleiro import Tabuleiro


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def empty_board():
    """Board with no cells filled."""
    return Tabuleiro(cores={})


@pytest.fixture
def sample_cores():
    """A small set of filled cells for reuse across tests."""
    return {
        (0, 0): 5,
        (0, 1): 3,
        (1, 0): 6,
        (4, 4): 9,
        (8, 8): 1,
    }


@pytest.fixture
def sample_board(sample_cores):
    return Tabuleiro(cores=sample_cores)


@pytest.fixture
def full_text():
    """81-character string representing a full 9×9 board (no dots)."""
    return (
        "534678912"
        "672195348"
        "198342567"
        "859761423"
        "426853791"
        "713924856"
        "961537284"
        "287419635"
        "345286179"
    )


@pytest.fixture
def full_matrix():
    """9×9 matrix (list of lists) matching `full_text`."""
    return [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9],
    ]


@pytest.fixture
def valid_board(full_text):
    """A fully solved, valid Sudoku board."""
    return Tabuleiro.de_texto(full_text)


# ---------------------------------------------------------------------------
# __init__
# ---------------------------------------------------------------------------

class TestInit:
    def test_stores_cores_dict(self, sample_cores):
        board = Tabuleiro(cores=sample_cores)
        assert board.cores is sample_cores

    def test_empty_cores(self):
        board = Tabuleiro(cores={})
        assert board.cores == {}


# ---------------------------------------------------------------------------
# de_texto (classmethod)
# ---------------------------------------------------------------------------

class TestDeTexto:
    def test_all_dots_produces_empty_board(self):
        text = "." * 81
        board = Tabuleiro.de_texto(text)
        assert board.cores == {}

    def test_single_nonzero(self):
        text = "5" + "." * 80
        board = Tabuleiro.de_texto(text)
        assert board.cores == {(0, 0): 5}

    def test_single_nonzero_middle(self):
        text = "." * 40 + "7" + "." * 40
        board = Tabuleiro.de_texto(text)
        assert board.cores == {(4, 4): 7}

    def test_last_position(self):
        text = "." * 80 + "1"
        board = Tabuleiro.de_texto(text)
        assert board.cores == {(8, 8): 1}

    def test_full_board(self, full_text):
        board = Tabuleiro.de_texto(full_text)
        assert len(board.cores) == 81

    def test_full_board_values(self, full_text):
        board = Tabuleiro.de_texto(full_text)
        assert board.cores[(0, 0)] == 5
        assert board.cores[(0, 8)] == 2
        assert board.cores[(8, 0)] == 3
        assert board.cores[(8, 8)] == 9

    def test_returns_tabuleiro_instance(self):
        board = Tabuleiro.de_texto("." * 81)
        assert isinstance(board, Tabuleiro)

    def test_row_col_mapping(self):
        """Verify that every index maps to the correct (row, col)."""
        text = "1" * 81
        board = Tabuleiro.de_texto(text)
        for idx in range(81):
            row, col = divmod(idx, 9)
            assert (row, col) in board.cores
            assert board.cores[(row, col)] == 1

    def test_mixed_dots_and_digits(self):
        row = "1.3.5.7.9"
        text = row + "." * 72
        board = Tabuleiro.de_texto(text)
        assert board.cores == {
            (0, 0): 1,
            (0, 2): 3,
            (0, 4): 5,
            (0, 6): 7,
            (0, 8): 9,
        }

    # --- Exception tests ---

    def test_rejects_non_string(self):
        with pytest.raises(TypeError, match="texto deve ser uma string"):
            Tabuleiro.de_texto(12345)

    def test_rejects_too_short(self):
        with pytest.raises(ValueError, match="81 caracteres"):
            Tabuleiro.de_texto("123")

    def test_rejects_too_long(self):
        with pytest.raises(ValueError, match="81 caracteres"):
            Tabuleiro.de_texto("." * 82)

    def test_rejects_empty_string(self):
        with pytest.raises(ValueError, match="81 caracteres"):
            Tabuleiro.de_texto("")

    def test_rejects_invalid_character(self):
        text = "." * 40 + "A" + "." * 40
        with pytest.raises(ValueError, match="Caractere inválido"):
            Tabuleiro.de_texto(text)

    def test_rejects_space_character(self):
        text = "." * 40 + " " + "." * 40
        with pytest.raises(ValueError, match="Caractere inválido"):
            Tabuleiro.de_texto(text)

    def test_rejects_zero_character(self):
        text = "." * 40 + "0" + "." * 40
        with pytest.raises(ValueError, match="Caractere inválido"):
            Tabuleiro.de_texto(text)


# ---------------------------------------------------------------------------
# de_matriz (classmethod)
# ---------------------------------------------------------------------------

class TestDeMatriz:
    def test_all_zeros_produces_empty_board(self):
        matrix = [[0] * 9 for _ in range(9)]
        board = Tabuleiro.de_matriz(matrix)
        assert board.cores == {}

    def test_single_nonzero(self):
        matrix = [[0] * 9 for _ in range(9)]
        matrix[2][3] = 8
        board = Tabuleiro.de_matriz(matrix)
        assert board.cores == {(2, 3): 8}

    def test_full_board(self, full_matrix):
        board = Tabuleiro.de_matriz(full_matrix)
        assert len(board.cores) == 81

    def test_full_board_values(self, full_matrix):
        board = Tabuleiro.de_matriz(full_matrix)
        assert board.cores[(0, 0)] == 5
        assert board.cores[(4, 4)] == 5
        assert board.cores[(8, 8)] == 9

    def test_returns_tabuleiro_instance(self, full_matrix):
        board = Tabuleiro.de_matriz(full_matrix)
        assert isinstance(board, Tabuleiro)

    def test_consistency_with_de_texto(self, full_text, full_matrix):
        """de_texto and de_matriz should produce identical boards."""
        from_text = Tabuleiro.de_texto(full_text)
        from_matrix = Tabuleiro.de_matriz(full_matrix)
        assert from_text.cores == from_matrix.cores

    def test_preserves_all_values(self, full_matrix):
        board = Tabuleiro.de_matriz(full_matrix)
        for i, row in enumerate(full_matrix):
            for j, val in enumerate(row):
                if val != 0:
                    assert board.cores[(i, j)] == val

    # --- Exception tests ---

    def test_rejects_too_few_rows(self):
        matrix = [[0] * 9 for _ in range(8)]
        with pytest.raises(ValueError, match="9 linhas"):
            Tabuleiro.de_matriz(matrix)

    def test_rejects_too_many_rows(self):
        matrix = [[0] * 9 for _ in range(10)]
        with pytest.raises(ValueError, match="9 linhas"):
            Tabuleiro.de_matriz(matrix)

    def test_rejects_empty_matrix(self):
        with pytest.raises(ValueError, match="9 linhas"):
            Tabuleiro.de_matriz([])

    def test_rejects_row_too_short(self):
        matrix = [[0] * 9 for _ in range(9)]
        matrix[3] = [0] * 8
        with pytest.raises(ValueError, match="9 colunas"):
            Tabuleiro.de_matriz(matrix)

    def test_rejects_row_too_long(self):
        matrix = [[0] * 9 for _ in range(9)]
        matrix[0] = [0] * 10
        with pytest.raises(ValueError, match="9 colunas"):
            Tabuleiro.de_matriz(matrix)

    def test_rejects_value_out_of_range(self):
        matrix = [[0] * 9 for _ in range(9)]
        matrix[0][0] = 10
        with pytest.raises(ValueError, match="Valor inválido"):
            Tabuleiro.de_matriz(matrix)

    def test_rejects_negative_value(self):
        matrix = [[0] * 9 for _ in range(9)]
        matrix[4][4] = -1
        with pytest.raises(ValueError, match="Valor inválido"):
            Tabuleiro.de_matriz(matrix)

    def test_rejects_non_integer_value(self):
        matrix = [[0] * 9 for _ in range(9)]
        matrix[0][0] = "5"
        with pytest.raises(ValueError, match="Valor inválido"):
            Tabuleiro.de_matriz(matrix)

    def test_rejects_float_value(self):
        matrix = [[0] * 9 for _ in range(9)]
        matrix[0][0] = 1.5
        with pytest.raises(ValueError, match="Valor inválido"):
            Tabuleiro.de_matriz(matrix)


# ---------------------------------------------------------------------------
# valido
# ---------------------------------------------------------------------------

class TestValido:
    # --- Valid boards ---

    def test_empty_board_is_valid(self, empty_board):
        assert empty_board.valido() is True

    def test_full_solved_board_is_valid(self, valid_board):
        assert valid_board.valido() is True

    def test_partial_board_no_conflicts_is_valid(self):
        """A partially filled board with no duplicates is valid."""
        cores = {
            (0, 0): 5, (0, 1): 3,
            (1, 0): 6,
            (4, 4): 9,
            (8, 8): 1,
        }
        board = Tabuleiro(cores=cores)
        assert board.valido() is True

    def test_single_cell_is_valid(self):
        board = Tabuleiro(cores={(0, 0): 1})
        assert board.valido() is True

    def test_full_row_no_duplicates_is_valid(self):
        """One row filled 1-9, rest empty."""
        cores = {(0, j): j + 1 for j in range(9)}
        board = Tabuleiro(cores=cores)
        assert board.valido() is True

    def test_full_column_no_duplicates_is_valid(self):
        """One column filled 1-9, rest empty."""
        cores = {(i, 0): i + 1 for i in range(9)}
        board = Tabuleiro(cores=cores)
        assert board.valido() is True

    def test_full_section_no_duplicates_is_valid(self):
        """One 3×3 section filled 1-9, rest empty."""
        cores = {}
        val = 1
        for i in range(3):
            for j in range(3):
                cores[(i, j)] = val
                val += 1
        board = Tabuleiro(cores=cores)
        assert board.valido() is True

    # --- Duplicate in row ---

    def test_duplicate_in_row_is_invalid(self):
        cores = {(0, 0): 5, (0, 4): 5}
        board = Tabuleiro(cores=cores)
        assert board.valido() is False

    def test_duplicate_in_row_adjacent(self):
        cores = {(3, 0): 7, (3, 1): 7}
        board = Tabuleiro(cores=cores)
        assert board.valido() is False

    def test_duplicate_in_last_row(self):
        cores = {(8, 0): 2, (8, 8): 2}
        board = Tabuleiro(cores=cores)
        assert board.valido() is False

    # --- Duplicate in column ---

    def test_duplicate_in_column_is_invalid(self):
        cores = {(0, 0): 3, (5, 0): 3}
        board = Tabuleiro(cores=cores)
        assert board.valido() is False

    def test_duplicate_in_column_adjacent(self):
        cores = {(0, 4): 8, (1, 4): 8}
        board = Tabuleiro(cores=cores)
        assert board.valido() is False

    def test_duplicate_in_last_column(self):
        cores = {(0, 8): 6, (8, 8): 6}
        board = Tabuleiro(cores=cores)
        assert board.valido() is False

    # --- Duplicate in 3×3 section ---

    def test_duplicate_in_top_left_section(self):
        """Two same numbers in the top-left 3×3 block."""
        cores = {(0, 0): 4, (2, 2): 4}
        board = Tabuleiro(cores=cores)
        assert board.valido() is False

    def test_duplicate_in_center_section(self):
        """Two same numbers in the center 3×3 block (rows 3-5, cols 3-5)."""
        cores = {(3, 3): 1, (5, 5): 1}
        board = Tabuleiro(cores=cores)
        assert board.valido() is False

    def test_duplicate_in_bottom_right_section(self):
        """Two same numbers in the bottom-right 3×3 block."""
        cores = {(6, 6): 9, (8, 8): 9}
        board = Tabuleiro(cores=cores)
        assert board.valido() is False

    def test_section_conflict_not_row_or_column(self):
        """Duplicate within a section but NOT on the same row or column."""
        cores = {(0, 0): 7, (1, 1): 7}
        board = Tabuleiro(cores=cores)
        assert board.valido() is False

    # --- Same value in different groups is OK ---

    def test_same_value_different_row_col_section_is_valid(self):
        """Same digit in different rows, columns, and sections is fine."""
        cores = {
            (0, 0): 1,  # section (0,0)
            (4, 4): 1,  # section (1,1)
            (8, 8): 1,  # section (2,2)
        }
        board = Tabuleiro(cores=cores)
        assert board.valido() is True

    def test_returns_bool(self, valid_board):
        assert isinstance(valid_board.valido(), bool)


# ---------------------------------------------------------------------------
# __str__
# ---------------------------------------------------------------------------

class TestStr:
    def test_empty_board_all_dots(self, empty_board):
        """An empty board should show dots for every position."""
        output = str(empty_board)
        lines = output.strip().split("\n")

        assert len(lines) == 11

        for line in lines:
            if line.startswith("-"):
                continue
            dots = line.replace(" ", "").replace("|", "")
            assert dots == "." * 9

    def test_separator_lines_present(self, empty_board):
        """Separator lines appear after rows 3 and 6 (indices 3, 7 in output)."""
        output = str(empty_board)
        lines = output.strip().split("\n")
        separator = "- - - - - - - - - - - - -"
        assert lines[3].strip() == separator.strip()
        assert lines[7].strip() == separator.strip()

    def test_column_separators(self, empty_board):
        """Each data line has two '|' column separators."""
        output = str(empty_board)
        lines = output.strip().split("\n")
        for line in lines:
            if line.startswith("-"):
                continue
            assert line.count("|") == 2

    def test_filled_cell_shows_digit(self, sample_board):
        """Filled cells should display their digit, not a dot."""
        output = str(sample_board)
        lines = [l for l in output.strip().split("\n") if not l.startswith("-")]

        first_data = lines[0].replace(" ", "").replace("|", "")
        assert first_data[0] == "5"
        assert first_data[1] == "3"

    def test_full_board_no_dots(self, full_text):
        """A fully filled board should contain no dots."""
        board = Tabuleiro.de_texto(full_text)
        output = str(board)
        assert "." not in output

    def test_str_is_string(self, empty_board):
        assert isinstance(str(empty_board), str)

    def test_output_has_trailing_newlines_per_row(self, empty_board):
        """Each row (including separators) ends with a newline."""
        output = str(empty_board)
        assert output.count("\n") == 11

    def test_round_trip_values(self):
        """Values placed via constructor should appear at the right spots."""
        cores = {(0, 0): 1, (0, 8): 2, (8, 0): 3, (8, 8): 4}
        board = Tabuleiro(cores=cores)
        output = str(board)
        lines = [l for l in output.strip().split("\n") if not l.startswith("-")]

        first_vals = lines[0].replace(" ", "").replace("|", "")
        assert first_vals[0] == "1"
        assert first_vals[-1] == "2"

        last_vals = lines[-1].replace(" ", "").replace("|", "")
        assert last_vals[0] == "3"
        assert last_vals[-1] == "4"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_de_texto_preserves_digit_types(self):
        """Values in cores should be int, not str."""
        text = "1" + "." * 80
        board = Tabuleiro.de_texto(text)
        assert isinstance(board.cores[(0, 0)], int)

    def test_de_matriz_works_with_tuples(self):
        """de_matriz should accept any iterable rows, including tuples."""
        matrix = [tuple([0] * 9) for _ in range(9)]
        board = Tabuleiro.de_matriz(matrix)
        assert board.cores == {}

    def test_cores_is_a_dict(self, sample_board):
        assert isinstance(sample_board.cores, dict)

    def test_de_texto_does_not_mutate_input(self):
        text = "5" + "." * 80
        original = text
        Tabuleiro.de_texto(text)
        assert text == original

    def test_de_matriz_does_not_mutate_input(self):
        matrix = [[0] * 9 for _ in range(9)]
        matrix[0][0] = 7
        import copy
        snapshot = copy.deepcopy(matrix)
        Tabuleiro.de_matriz(matrix)
        assert matrix == snapshot
