# ==========================================
# tests/test_conversor.py
# SUÍTE DE TESTES AUTOMATIZADOS (MÍN. 30 CASOS)
# ==========================================

import sys
import os
import unittest

# Adiciona a pasta 'src' ao path para o Python conseguir importar o conversor
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from conversor import (
    decimal_para_base_inteiro,
    base_para_decimal_inteiro,
    binario_para_agrupado,
    agrupado_para_binario,
    octal_hex_intermediario,
    fracionario_para_decimal,
    decimal_para_fracionario
)

class TestConversorUniversal(unittest.TestCase):

    def test_01_decimal_para_base_inteiro_F1(self):
        """[F1] Testa conversões de Decimal para Binário, Octal e Hexadecimal (10 casos)"""
        # Decimal -> Binário
        self.assertEqual(decimal_para_base_inteiro(0, 2), "0")
        self.assertEqual(decimal_para_base_inteiro(10, 2), "1010")
        self.assertEqual(decimal_para_base_inteiro(255, 2), "11111111")
        
        # Decimal -> Octal
        self.assertEqual(decimal_para_base_inteiro(0, 8), "0")
        self.assertEqual(decimal_para_base_inteiro(8, 8), "10")
        self.assertEqual(decimal_para_base_inteiro(64, 8), "100")
        self.assertEqual(decimal_para_base_inteiro(255, 8), "377")
        
        # Decimal -> Hexadecimal
        self.assertEqual(decimal_para_base_inteiro(0, 16), "0")
        self.assertEqual(decimal_para_base_inteiro(15, 16), "F")
        self.assertEqual(decimal_para_base_inteiro(255, 16), "FF")

    def test_02_base_para_decimal_inteiro_F2(self):
        """[F2] Testa conversões de Binário, Octal e Hexadecimal para Decimal (9 casos)"""
        # Binário -> Decimal
        self.assertEqual(base_para_decimal_inteiro("0", 2), 0)
        self.assertEqual(base_para_decimal_inteiro("1010", 2), 10)
        self.assertEqual(base_para_decimal_inteiro("11111111", 2), 255)
        
        # Octal -> Decimal
        self.assertEqual(base_para_decimal_inteiro("0", 8), 0)
        self.assertEqual(base_para_decimal_inteiro("10", 8), 8)
        self.assertEqual(base_para_decimal_inteiro("377", 8), 255)
        
        # Hexadecimal -> Decimal
        self.assertEqual(base_para_decimal_inteiro("0", 16), 0)
        self.assertEqual(base_para_decimal_inteiro("A", 16), 10)
        self.assertEqual(base_para_decimal_inteiro("FF", 16), 255)

    def test_03_agrupamento_direto_F3_F4(self):
        """[F3/F4] Testa conversões diretas por agrupamento de bits (7 casos)"""
        # F3: Binário -> Octal (Grupos de 3)
        self.assertEqual(binario_para_agrupado("1010", 3), "12")
        self.assertEqual(binario_para_agrupado("11111111", 3), "377")
        
        # F3: Binário -> Hexadecimal (Grupos de 4)
        self.assertEqual(binario_para_agrupado("1010", 4), "A")
        self.assertEqual(binario_para_agrupado("11111111", 4), "FF")
        
        # F4 Auxiliar: Octal/Hex -> Binário
        self.assertEqual(agrupado_para_binario("12", 3), "1010")
        self.assertEqual(agrupado_para_binario("FF", 4), "11111111")
        
        # F4: Octal <-> Hexadecimal
        self.assertEqual(octal_hex_intermediario("377", 8, 16), "FF")

    def test_04_fracionarios_F6(self):
        """[F6] Testa conversões de partes fracionárias e truncamento (6 casos)"""
        # Fração para Decimal (Float)
        self.assertEqual(fracionario_para_decimal("1", 2), 0.5)      # 0.1 bin -> 0.5 dec
        self.assertEqual(fracionario_para_decimal("A", 16), 0.625)   # 0.A hex -> 0.625 dec
        self.assertEqual(fracionario_para_decimal("625", 10), 0.625) # 0.625 dec -> 0.625 dec
        
        # Float para Fração Base
        resultado_bin, trunc_bin = decimal_para_fracionario(0.625, 2)
        self.assertEqual(resultado_bin, "101")
        self.assertFalse(trunc_bin)
        
        # Teste de truncamento (Dízima periódica em binário: 0.1 decimal)
        resultado_trunc, trunc = decimal_para_fracionario(0.1, 2, limite_casas=16)
        self.assertEqual(len(resultado_trunc), 16)
        self.assertTrue(trunc)

if __name__ == '__main__':
    print("="*45)
    print(" INICIANDO SUÍTE DE TESTES AUTOMATIZADOS")
    print("="*45)
    unittest.main(verbosity=2)
