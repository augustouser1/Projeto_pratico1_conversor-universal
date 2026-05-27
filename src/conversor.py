# ==========================================
# src/conversor.py
# NÚCLEO DE CONVERSÃO MATEMÁTICA
# ==========================================

def caractere_para_valor(c):
    """Mapeia um caractere (0-9, A-F, a-f) para seu valor numerico usando tabela ASCII."""
    ord_c = ord(c.upper())
    if 48 <= ord_c <= 57: return ord_c - 48    # 0-9
    if 65 <= ord_c <= 70: return ord_c - 55    # A-F
    return -1

def valor_para_caractere(v):
    """Mapeia um valor numerico (0-15) para seu caractere correspondente."""
    if 0 <= v <= 9: return chr(v + 48)
    if 10 <= v <= 15: return chr(v + 55)
    return '?'

# ==========================================
# REQUISITOS F1 e F2: PARTE INTEIRA
# ==========================================

def decimal_para_base_inteiro(valor_decimal, base_destino):
    """
    [F1] Converte Decimal para qualquer base usando divisoes sucessivas.
    """
    if valor_decimal == 0:
        return "0"
    
    resultado = ""
    while valor_decimal > 0:
        resto = valor_decimal % base_destino
        resultado = valor_para_caractere(resto) + resultado
        valor_decimal = valor_decimal // base_destino
        
    return resultado

def base_para_decimal_inteiro(string_valor, base_origem):
    """
    [F2] Converte qualquer base para Decimal usando somatorio posicional.
    """
    resultado = 0
    potencia = 0
    
    for i in range(len(string_valor) - 1, -1, -1):
        valor = caractere_para_valor(string_valor[i])
        
        mult = 1
        for _ in range(potencia):
            mult *= base_origem
            
        resultado += valor * mult
        potencia += 1
        
    return resultado

# ==========================================
# REQUISITOS F3 e F4: AGRUPAMENTO DE BITS 
# ==========================================

def binario_para_agrupado(bin_str, bits_por_grupo):
    """
    [F3] Converte Binario para Octal ou Hexadecimal mapeando por dicionarios.
    """
    faltam = len(bin_str) % bits_por_grupo
    if faltam != 0:
        bin_str = ("0" * (bits_por_grupo - faltam)) + bin_str
        
    resultado = ""
    
    if bits_por_grupo == 3: # Rota Octal
        tabela_bin_oct = {
            '000': '0', '001': '1', '010': '2', '011': '3',
            '100': '4', '101': '5', '110': '6', '111': '7'
        }
        for i in range(0, len(bin_str), 3):
            grupo = bin_str[i:i+3]
            resultado += tabela_bin_oct.get(grupo, '')
            
    else: # Rota Hexadecimal
        tabela_bin_hex = {
            '0000': '0', '0001': '1', '0010': '2', '0011': '3',
            '0100': '4', '0101': '5', '0110': '6', '0111': '7',
            '1000': '8', '1001': '9', '1010': 'A', '1011': 'B',
            '1100': 'C', '1101': 'D', '1110': 'E', '1111': 'F'
        }
        for i in range(0, len(bin_str), 4):
            grupo = bin_str[i:i+4]
            resultado += tabela_bin_hex.get(grupo, '')
            
    return resultado

def agrupado_para_binario(valor_str, bits_por_grupo):
    """
    [F4 Auxiliar] Converte Octal/Hexadecimal para Binario mapeando por dicionarios.
    """
    resultado = ""
    
    if bits_por_grupo == 3: # Rota Octal
        tabela_oct_bin = {
            '0': '000', '1': '001', '2': '010', '3': '011',
            '4': '100', '5': '101', '6': '110', '7': '111'
        }
        for char in valor_str.upper():
            resultado += tabela_oct_bin.get(char, '')
            
    else: # Rota Hexadecimal
        tabela_hex_bin = {
            '0': '0000', '1': '0001', '2': '0010', '3': '0011',
            '4': '0100', '5': '0101', '6': '0110', '7': '0111',
            '8': '1000', '9': '1001', 'A': '1010', 'B': '1011',
            'C': '1100', 'D': '1101', 'E': '1110', 'F': '1111'
        }
        for char in valor_str.upper():
            resultado += tabela_hex_bin.get(char, '')
            
    resultado = resultado.lstrip('0')
    return resultado if resultado else "0"

def octal_hex_intermediario(valor_str, base_origem, base_destino):
    """
    [F4] Converte Octal <-> Hexadecimal usando o binario como ponte.
    """
    bits_origem = 3 if base_origem == 8 else 4
    bits_destino = 3 if base_destino == 8 else 4
    
    # Passo 1: Vai para binario usando o seu mapeamento
    binario_ponte = agrupado_para_binario(valor_str, bits_origem)
    
    # Passo 2: Vai do binario para o destino usando o seu mapeamento
    return binario_para_agrupado(binario_ponte, bits_destino)

# ==========================================
# REQUISITO F6: PARTE FRACIONÁRIA
# ==========================================

def fracionario_para_decimal(string_fracionaria, base_origem):
    """Passo 1 do F6: Parte fracionaria para decimal."""
    resultado_decimal = 0.0
    for i in range(len(string_fracionaria)):
        digito = string_fracionaria[i]
        valor = caractere_para_valor(digito)
        
        potencia = 1.0
        for _ in range(i + 1):
            potencia /= base_origem
            
        resultado_decimal += valor * potencia
        
    return resultado_decimal

def decimal_para_fracionario(valor_float, base_destino, limite_casas=16):
    """Passo 2 do F6: Float decimal para base de destino por multiplicacoes sucessivas."""
    resultado_str = ""
    truncado = False
    contador = 0
    
    while valor_float > 0 and contador < limite_casas:
        valor_float *= base_destino
        parte_inteira = int(valor_float)
        
        resultado_str += valor_para_caractere(parte_inteira)
        valor_float -= parte_inteira
        contador += 1
        
    if valor_float > 0:
        truncado = True
        
    return resultado_str if resultado_str else "0", truncado
