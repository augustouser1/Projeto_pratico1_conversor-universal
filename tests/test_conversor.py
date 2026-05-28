import pytest

from src.conversor import (
    fracionario_para_decimal,
    decimal_para_fracionario,
    base_para_decimal_inteiro,
    decimal_para_base_inteiro
    
)

# ==========================================
# TESTES DO REQUISITO F6: FRACIONÁRIOS (20 CASOS)
# ==========================================

@pytest.mark.parametrize("fracao_str, base_origem, esperado", [
    ("625", 10, 0.625),
    ("5", 10, 0.5),
    ("101", 2, 0.625),
    ("1", 2, 0.5),
    ("01", 2, 0.25),
    ("11", 2, 0.75),
    ("4", 8, 0.5),
    ("2", 8, 0.25),
    ("8", 16, 0.5),
    ("4", 16, 0.25),
])
def test_fracionario_para_decimal(fracao_str, base_origem, esperado):
    """Garante que qualquer fração de entrada chega perfeitamente à base 10"""
    assert fracionario_para_decimal(fracao_str, base_origem) == esperado

@pytest.mark.parametrize("valor_dec, base_dest, esperado_str, esperado_trunc", [
    (0.625, 2, "101", False),
    (0.5, 2, "1", False),
    (0.25, 2, "01", False),
    (0.75, 2, "11", False),
    (0.1, 2, "0001100110011001", True), # Proteção contra loop infinito em dízima binária
    (0.5, 8, "4", False),
    (0.25, 8, "2", False),
    (0.125, 8, "1", False),
    (0.5, 16, "8", False),
    (0.25, 16, "4", False),
])
def test_decimal_para_fracionario(valor_dec, base_dest, esperado_str, esperado_trunc):
    """Garante que a saída fracionária está correta e o truncamento de 16 casas funciona"""
    resultado, truncado = decimal_para_fracionario(valor_dec, base_dest)
    assert resultado == esperado_str
    assert truncado == esperado_trunc

# ==========================================
# TESTES DOS REQUISITOS F1 e F2: INTEIROS (12 CASOS)
# ==========================================

@pytest.mark.parametrize("string_int, base_origem, esperado", [
    ("1010", 2, 10),
    ("1111", 2, 15),
    ("12", 8, 10),
    ("17", 8, 15),
    ("A", 16, 10),
    ("F", 16, 15),
])
def test_base_para_decimal_inteiro(string_int, base_origem, esperado):
    """Garante a conversão de inteiros de qualquer base para Decimal"""
    assert base_para_decimal_inteiro(string_int, base_origem) == esperado

@pytest.mark.parametrize("valor_dec, base_dest, esperado_str", [
    (10, 2, "1010"),
    (15, 2, "1111"),
    (10, 8, "12"),
    (15, 8, "17"),
    (10, 16, "A"),
    (15, 16, "F"),
])
def test_decimal_para_base_inteiro(valor_dec, base_dest, esperado_str):
    """Garante a conversão de inteiros do Decimal para qualquer base"""
    assert decimal_para_base_inteiro(valor_dec, base_dest) == esperado_str
