# ==========================================
# src/formatador.py
# MÓDULO DE FORMATAÇÃO E TRACE (REQUISITO F7)
# ==========================================

def exibir_resultado_simples(entrada, base_origem, resultado, base_destino, truncado=False):
    """
    Exibe o resultado final da conversão de forma limpa e organizada.
    """
    print("\n" + "="*45)
    print(" RESULTADO DA CONVERSÃO".center(45))
    print("="*45)
    print(f" Valor original  : {entrada} (Base {base_origem})")
    print(f" Valor convertido: {resultado} (Base {base_destino})")
    if truncado:
        print("\n [!] ATENÇÃO: A parte fracionária excedeu 16 casas")
        print("              e foi truncada conforme a regra do F6.")
    print("="*45 + "\n")


def exibir_trace_divisao(valor_decimal, base_destino):
    """
    [F7] Exibe o passo-a-passo (trace) do método de divisões sucessivas.
    Reconstrói a matemática apenas para fins de exibição visual.
    """
    print("\n--- TRACE: Divisões Sucessivas ---")
    valor = int(valor_decimal)
    
    if valor == 0:
        print(f"{valor} / {base_destino} = 0 (Resto 0)")
        return
        
    passo = 1
    while valor > 0:
        resto = valor % base_destino
        quociente = valor // base_destino
        
        # Formatação de chave de divisão
        print(f"Passo {passo}:")
        print(f"  {valor:^5} |__ {base_destino}")
        print(f" -      {quociente}")
        print(f"  {resto:^5} (Resto)")
        print("-" * 20)
        
        valor = quociente
        passo += 1
    print("Leitura do resultado final: restos de baixo para cima.\n")


def exibir_trace_somatorio(string_valor, base_origem):
    """
    [F7] Exibe o passo-a-passo do somatório posicional.
    """
    print("\n--- TRACE: Somatório Posicional ---")
    tamanho = len(string_valor)
    partes = []
    
    # Monta a equação visual para o usuário conferir no caderno
    for i in range(tamanho):
        char = string_valor[i]
        potencia = tamanho - 1 - i
        partes.append(f"({char} * {base_origem}^{potencia})")
        
    equacao = " + ".join(partes)
    print("Equação montada:")
    print(f"n = {equacao}")
    print("-" * 20 + "\n")


def exibir_trace_fracionario(string_fracionaria, base_origem):
    """
    [F7] Exibe o trace da conversão da parte fracionária para decimal.
    """
    print("\n--- TRACE: Somatório Posicional (Fracionário) ---")
    partes = []
    
    for i in range(len(string_fracionaria)):
        char = string_fracionaria[i]
        potencia_negativa = -(i + 1)
        partes.append(f"({char} * {base_origem}^{potencia_negativa})")
        
    equacao = " + ".join(partes)
    print("Equação fracionária montada:")
    print(f"n = {equacao}")
    print("-" * 20 + "\n")


def exibir_trace_agrupamento(valor_str, base_origem, base_destino):
    """
    [F7] Exibe o trace visual do agrupamento de bits (F3 e F4).
    """
    print("\n--- TRACE: Agrupamento / Expansão de Bits ---")
    
    if base_origem == 2:
        bits = 3 if base_destino == 8 else 4
        print(f"Convertendo Binário -> Base {base_destino} (Agrupando de {bits} em {bits} bits)")
        
        # Simula o preenchimento de zeros à esquerda para a exibição visual
        faltam = len(valor_str) % bits
        bin_str = ("0" * (bits - faltam)) + valor_str if faltam != 0 else valor_str
        
        for i in range(0, len(bin_str), bits):
            grupo = bin_str[i:i+bits]
            print(f"  Grupo: {grupo} -> Convertido")
            
    elif base_destino == 2:
        bits = 3 if base_origem == 8 else 4
        print(f"Convertendo Base {base_origem} -> Binário (Expandindo cada dígito para {bits} bits)")
        for char in valor_str:
            print(f"  Dígito: {char} -> Expandido")
            
    else:
        print(f"Convertendo Base {base_origem} -> Base {base_destino} (Usando o binário como ponte intermediária)")
        
    print("-" * 20 + "\n")
