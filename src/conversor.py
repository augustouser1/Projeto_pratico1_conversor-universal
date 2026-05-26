# ==========================================
# src/conversor.py
# NÚCLEO DE CONVERSÃO MATEMÁTICA
# ==========================================

def caractere_para_valor(c):
    """Mapeia um caractere (0-9, A-F, a-f) para seu valor numérico usando tabela ASCII."""
    ord_c = ord(c.upper())
    if 48 <= ord_c <= 57: return ord_c - 48    # 0-9
    if 65 <= ord_c <= 70: return ord_c - 55    # A-F
    return -1

def valor_para_caractere(v):
    """Mapeia um valor numérico (0-15) para seu caractere correspondente."""
    if 0 <= v <= 9: return chr(v + 48)
    if 10 <= v <= 15: return chr(v + 55)
    return '?'

# ==========================================
# REQUISITOS F1 e F2: PARTE INTEIRA
# ==========================================

def decimal_para_base_inteiro(valor_decimal, base_destino):
    """
    [F1] Converte Decimal para qualquer base usando divisões sucessivas.
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
    [F2] Converte qualquer base para Decimal usando somatório posicional.
    """
    resultado = 0
    potencia = 0
    
    # Percorre a string de trás para frente
    for i in range(len(string_valor) - 1, -1, -1):
        valor = caractere_para_valor(string_valor[i])
        
        # Calcula base^potencia manualmente para evitar funções prontas complexas
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
    [F3] Converte Binário para Octal (3 bits) ou Hexadecimal (4 bits) por agrupamento.
    """
    # Preenche com zeros à esquerda para fechar os grupos perfeitamente
    faltam = len(bin_str) % bits_por_grupo
    if faltam != 0:
        bin_str = ("0" * (bits_por_grupo - faltam)) + bin_str
        
    resultado = ""
    for i in range(0, len(bin_str), bits_por_grupo):
        grupo = bin_str[i:i+bits_por_grupo]
        # Calcula o valor do pequeno grupo
        val_grupo = base_para_decimal_inteiro(grupo, 2)
        resultado += valor_para_caractere(val_grupo)
        
    return resultado

def agrupado_para_binario(valor_str, bits_por_grupo):
    """
    [F4 Auxiliar] Converte Octal/Hexadecimal para Binário expandindo cada dígito.
    """
    resultado = ""
    for char in valor_str:
        val_dec = caractere_para_valor(char)
        bin_grupo = decimal_para_base_inteiro(val_dec, 2)
        
        # Preenche com zeros à esquerda para manter o tamanho do grupo (ex: 3 vira 011)
        bin_grupo = ("0" * (bits_por_grupo - len(bin_grupo))) + bin_grupo
        resultado += bin_grupo
        
    # Remove zeros à esquerda desnecessários no resultado final
    resultado = resultado.lstrip('0')
    return resultado if resultado else "0"

def octal_hex_intermediario(valor_str, base_origem, base_destino):
    """
    [F4] Converte Octal <-> Hexadecimal usando o binário como ponte.
    """
    bits_origem = 3 if base_origem == 8 else 4
    bits_destino = 3 if base_destino == 8 else 4
    
    # Passo 1: Vai para binário
    binario_ponte = agrupado_para_binario(valor_str, bits_origem)
    
    # Passo 2: Vai do binário para o destino
    return binario_para_agrupado(binario_ponte, bits_destino)

# ==========================================
# REQUISITO F6: PARTE FRACIONÁRIA
# ==========================================

def fracionario_para_decimal(string_fracionaria, base_origem):
    """Passo 1 do F6: Parte fracionária para decimal."""
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
    """Passo 2 do F6: Float decimal para base de destino por multiplicações sucessivas."""
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
