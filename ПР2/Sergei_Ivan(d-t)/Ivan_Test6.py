import pytest
import importlib.util
import sys

# === Динамическая загрузка класса Matrix из 2prac.py ===
spec = importlib.util.spec_from_file_location("MatrixModule", "./Sergei_with_errors.py")
module = importlib.util.module_from_spec(spec)
sys.modules["MatrixModule"] = module
spec.loader.exec_module(module)
Matrix = module.Matrix


# === Тестирование конструктора ===

def test_constructor_with_data_sets_size_correctly():
    m = Matrix([[1, 2], [3, 4]])
    assert m.size == "2x2"
    assert m.matrix_v == [[1, 2], [3, 4]]


def test_constructor_with_empty_matrix_uses_default_size():
    m = Matrix()
    assert m.size == "1x1"
    assert m.matrix_v == []


# === Тестирование change_element ===

def test_change_element_changes_value_correctly():
    m = Matrix([[1, 2], [3, 4]])
    m.change_element(1, 0, 99)
    assert m.matrix_v[1][0] == 99


def test_change_element_raises_index_error_on_invalid_index():
    m = Matrix([[1, 2], [3, 4]])
    with pytest.raises(IndexError, match=r"вне границ матрицы"):
        m.change_element(3, 0, 10)


# === Тестирование create_matrix ===

def test_create_matrix_with_default_values_creates_correct_matrix():
    m = Matrix()
    created = m.create_matrix("2x3")
    assert created == [[1, 2, 3], [4, 5, 6]]
    assert m.size == "2x3"


def test_create_matrix_invalid_size_format_raises_value_error():
    m = Matrix()
    with pytest.raises(ValueError, match=r"Неверный формат размера"):
        m.create_matrix("2-3")


# === Тестирование _validate_size_format ===

@pytest.mark.parametrize("size,expected", [
    ("3x3", True),
    ("1x9", True),
    ("33", False),
    ("3xx", False),
    ("x3", False),
    ("3x", False),
])
def test_validate_size_format(size, expected):
    assert Matrix._validate_size_format(size) == expected


# === Тестирование transposition ===

def test_transposition_returns_transposed_matrix():
    m = Matrix([[1, 2, 3], [4, 5, 6]])
    t = m.transposition()
    assert t.matrix_v == [[1, 4], [2, 5], [3, 6]]
    assert isinstance(t, Matrix)


def test_transposition_raises_error_on_empty_matrix():
    m = Matrix([])
    with pytest.raises(ValueError, match=r"Матрица пуста"):
        m.transposition()


# === Тестирование sum ===

def test_sum_of_equal_matrices_returns_correct_result():
    m1 = Matrix([[1, 2], [3, 4]])
    m2 = Matrix([[5, 6], [7, 8]])
    result = Matrix.sum(m1, m2)
    assert result.matrix_v == [[6, 8], [10, 12]]


def test_sum_raises_error_for_different_sizes():
    m1 = Matrix([[1, 2], [3, 4]])
    m2 = Matrix([[1, 2, 3], [4, 5, 6]])
    with pytest.raises(ValueError, match=r"Размеры матриц не совпадают"):
        Matrix.sum(m1, m2)


def test_sum_raises_error_for_empty_matrix():
    m1 = Matrix([[1, 2], [3, 4]])
    m2 = Matrix()
    with pytest.raises(ValueError, match=r"Одна из матриц пуста"):
        Matrix.sum(m1, m2)


# === Тестирование multiplication ===

def test_multiplication_returns_correct_result():
    m1 = Matrix([[1, 2], [3, 4]])
    m2 = Matrix([[2, "0"], [1, 2]])
    result = Matrix.multiplication(m1, m2)
    assert result.matrix_v == [[4, 4], [10, 8]]


def test_multiplication_raises_value_error_for_incompatible_sizes():
    m1 = Matrix([[1, 2, 3]])
    m2 = Matrix([[1, 2], [3, 4]])
    with pytest.raises(ValueError, match=r"Несовместимые размеры"):
        Matrix.multiplication(m1, m2)


def test_multiplication_raises_type_error_for_invalid_elements():
    m1 = Matrix([[1, "a"], [3, 4]])
    m2 = Matrix([[1, 2], [3, 4]])
    with pytest.raises(TypeError, match=r"Элементы матриц должны быть числами"):
        Matrix.multiplication(m1, m2)