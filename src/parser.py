# ==========================================
# src/parser.py
# MÓDULO DE VALIDAÇÃO DE ENTRADA (REQUISITO F5)
# ==========================================

def validar_base(base):
    """
    Verifica se a base escolhida pelo usuário é suportada pelo sistema.
    """
    bases_validas = [2, 8, 10, 16]
    if base not in bases_validas:
        print(f"[ERRO] Base {base} inválida. O sistema suporta apenas as bases 2, 8, 10 e 16.")
        return False
    return True

def validar_entrada(entrada, base):
    """
    [F5] Valida a entrada de acordo com a base de origem.
    Rejeita dígitos inválidos (ex: 8 em octal, G em hexadecimal) e 
    exibe mensagens de erro claras.
    
    Retorna:
        tuple: (bool: sucesso na validação, str: entrada normalizada)
    """
    # Remove espaços em branco acidentais
    entrada = entrada.strip()
    
    # Normaliza o separador fracionário (aceita vírgula ou ponto)
    entrada_normalizada = entrada.replace(',', '.')

    # Verifica se há mais de um separador fracionário
    if entrada_normalizada.count('.') > 1:
        print("[ERRO] Formato numérico inválido: o número contém múltiplos separadores fracionários.")
        return False, ""

    # Remove o ponto temporariamente para validar apenas os dígitos
    entrada_sem_ponto = entrada_normalizada.replace('.', '')

    if not entrada_sem_ponto:
        print("[ERRO] Entrada vazia ou contendo apenas o separador fracionário.")
        return False, ""

    # Define os conjuntos de caracteres permitidos na unha
    caracteres_permitidos = ""
    if base == 2:
        caracteres_permitidos = "01"
    elif base == 8:
        caracteres_permitidos = "01234567"
    elif base == 10:
        caracteres_permitidos = "0123456789"
    elif base == 16:
        # Hexadecimal aceita maiúsculas e minúsculas
        caracteres_permitidos = "0123456789ABCDEFabcdef"

    # Itera sobre a string verificando caractere por caractere
    for char in entrada_sem_ponto:
        if char not in caracteres_permitidos:
            if base == 16:
                print(f"[ERRO] O caractere '{char}' é inválido para a base Hexadecimal (permitido apenas 0-9 e A-F).")
            else:
                print(f"[ERRO] O caractere '{char}' é inválido para a base {base}.")
            return False, ""

    # Retorna True e a string já com a vírgula trocada por ponto
    return True, entrada_normalizada
