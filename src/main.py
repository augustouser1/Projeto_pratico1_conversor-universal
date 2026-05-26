# ==========================================
# src/main.py
# PONTO DE ENTRADA E GERENCIADOR DE FLUXO
# ==========================================

import sys
import csv

from parser import validar_base, validar_entrada
from conversor import (
    decimal_para_base_inteiro, base_para_decimal_inteiro,
    binario_para_agrupado, agrupado_para_binario, octal_hex_intermediario,
    fracionario_para_decimal, decimal_para_fracionario
)
from formatador import (
    exibir_resultado_simples, exibir_trace_divisao, 
    exibir_trace_somatorio, exibir_trace_fracionario,
    exibir_trace_agrupamento
)

def processar_parte_inteira(valor_str, origem, destino, trace):
    """Orquestra a conversão da parte inteira escolhendo a rota correta."""
    if origem == destino:
        return valor_str

    # [F3 e F4] Rotas diretas sem passar pelo decimal
    if origem == 2 and destino in (8, 16):
        if trace: exibir_trace_agrupamento(valor_str, origem, destino) # <-- Chamada do trace inserida
        bits = 3 if destino == 8 else 4
        return binario_para_agrupado(valor_str, bits)
    
    if origem in (8, 16) and destino == 2:
        if trace: exibir_trace_agrupamento(valor_str, origem, destino) # <-- Chamada do trace inserida
        bits = 3 if origem == 8 else 4
        return agrupado_para_binario(valor_str, bits)
        
    if origem in (8, 16) and destino in (8, 16):
        if trace: exibir_trace_agrupamento(valor_str, origem, destino) # <-- Chamada do trace inserida
        return octal_hex_intermediario(valor_str, origem, destino)

    # [F1 e F2] Rotas passando pelo decimal
    valor_decimal = int(valor_str) if origem == 10 else base_para_decimal_inteiro(valor_str, origem)
    
    if trace and origem != 10:
        exibir_trace_somatorio(valor_str, origem)

    if destino == 10:
        return str(valor_decimal)

    if trace and destino != 10:
        exibir_trace_divisao(valor_decimal, destino)

    return decimal_para_base_inteiro(valor_decimal, destino)
    
def processar_parte_fracionaria(valor_str, origem, destino, trace):
    """Orquestra a conversão da parte fracionária (F6)."""
    if not valor_str or valor_str == "0":
        return "", False

    if trace:
        exibir_trace_fracionario(valor_str, origem)

    # Vai para decimal
    dec_frac = fracionario_para_decimal(valor_str, origem)
    
    # Vai para o destino
    res_frac_str, truncado = decimal_para_fracionario(dec_frac, destino)
    
    return res_frac_str, truncado

def executar_conversao_interativa():
    """Modo principal de interação com o usuário via terminal."""
    print("="*45)
    print(" CONVERSOR UNIVERSAL DE BASES ".center(45))
    print("="*45)

    try:
        base_origem = int(input("Digite a base de origem (2, 8, 10, 16): "))
        if not validar_base(base_origem): return

        base_destino = int(input("Digite a base de destino (2, 8, 10, 16): "))
        if not validar_base(base_destino): return

        entrada_bruta = input("Digite o valor a ser convertido: ")
        
        # [F5] Validação de entrada
        valido, entrada_norm = validar_entrada(entrada_bruta, base_origem)
        if not valido: return

        # [F7] Pergunta sobre o trace
        resp_trace = input("Deseja ver o passo-a-passo (Trace)? (S/N): ").strip().upper()
        trace = (resp_trace == 'S')

        # Separa parte inteira e fracionária (se houver)
        if '.' in entrada_norm:
            partes = entrada_norm.split('.')
            parte_int_str = partes[0] if partes[0] != "" else "0"
            parte_frac_str = partes[1]
        else:
            parte_int_str = entrada_norm
            parte_frac_str = ""

        # Processa as metades
        resultado_inteiro = processar_parte_inteira(parte_int_str, base_origem, base_destino, trace)
        resultado_frac, truncado = processar_parte_fracionaria(parte_frac_str, base_origem, base_destino, trace)

        # Monta o resultado final
        resultado_final = resultado_inteiro
        if resultado_frac:
            resultado_final += f",{resultado_frac}"

        exibir_resultado_simples(entrada_norm, base_origem, resultado_final, base_destino, truncado)

    except ValueError:
        print("[ERRO] Entrada inválida. Por favor, digite números inteiros para as bases.")

def executar_modo_batch():
    """[F8] Modo batch: processa um arquivo CSV de entrada e gera um de saída."""
    print("\n--- MODO BATCH (PROCESSAMENTO EM LOTE) ---")
    caminho_entrada = input("Caminho do arquivo CSV (ex: tests/entrada_exemplo.csv): ")
    caminho_saida = "saida.csv"

    try:
        # Abre o arquivo de entrada para leitura e o de saída para escrita
        with open(caminho_entrada, mode='r', encoding='utf-8') as f_in, \
             open(caminho_saida, mode='w', encoding='utf-8', newline='') as f_out:
            
            leitor = csv.reader(f_in, delimiter=';')
            escritor = csv.writer(f_out, delimiter=';')
            
            # Pula o cabeçalho original e escreve o novo formato exigido no F8
            cabecalho = next(leitor, None)
            if cabecalho:
                escritor.writerow(['valor', 'base_origem', 'resultado', 'base_destino'])

            linhas_processadas = 0
            for linha in leitor:
                if len(linha) < 3: continue
                
                valor_bruto = linha[0].strip()
                b_origem_str = linha[1].strip()
                b_destino_str = linha[2].strip()
                
                try:
                    base_origem = int(b_origem_str)
                    base_destino = int(b_destino_str)
                    
                    # Valida a entrada daquela linha
                    valido, valor_norm = validar_entrada(valor_bruto, base_origem)
                    if not valido:
                        escritor.writerow([valor_bruto, base_origem, 'ERRO', base_destino])
                        continue
                    
                    # Separa inteiro e fracionário
                    if '.' in valor_norm:
                        partes = valor_norm.split('.')
                        parte_int = partes[0] if partes[0] != "" else "0"
                        parte_frac = partes[1]
                    else:
                        parte_int = valor_norm
                        parte_frac = ""
                        
                    # Realiza os cálculos silenciando o trace
                    res_int = processar_parte_inteira(parte_int, base_origem, base_destino, False)
                    res_frac, _ = processar_parte_fracionaria(parte_frac, base_origem, base_destino, False)
                    
                    resultado_final = f"{res_int},{res_frac}" if res_frac else res_int
                    
                    # Grava no novo arquivo
                    escritor.writerow([valor_bruto, base_origem, resultado_final, base_destino])
                    linhas_processadas += 1
                    
                except ValueError:
                    escritor.writerow([valor_bruto, b_origem_str, 'ERRO_BASE', b_destino_str])

        print(f"\n[SUCESSO] {linhas_processadas} conversões realizadas!")
        print(f"O arquivo com os resultados foi salvo na raiz do projeto como: {caminho_saida}")
        
    except FileNotFoundError:
        print(f"\n[ERRO] O arquivo '{caminho_entrada}' não foi encontrado.")

def menu_principal():
    """Loop principal do programa."""
    while True:
        print("\nEscolha um modo de operação:")
        print("1. Modo Interativo (F1 a F7)")
        print("2. Modo Batch CSV (F8)")
        print("0. Sair")
        
        opcao = input("Opção: ").strip()
        
        if opcao == '1':
            executar_conversao_interativa()
        elif opcao == '2':
            executar_modo_batch()
        elif opcao == '0':
            print("Encerrando o programa. Até logo!")
            sys.exit(0)
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n[!] Programa interrompido pelo usuário.")
        sys.exit(0)
        
      
