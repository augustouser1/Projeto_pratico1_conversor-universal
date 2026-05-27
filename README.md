# Conversor Universal de Sistemas de Numeração

**Trabalho Prático 1** desenvolvido para a disciplina GCC241 - Introdução à Computação da Universidade Federal de Lavras (UFLA), sob a orientação do Prof. Dr. Rafael Serapilha Durelli.

Este projeto é um conversor de bases numéricas robusto, desenvolvido inteiramente em Python, respeitando a restrição central do trabalho: **nenhuma função ou método nativo da linguagem que efetue conversão entre bases foi utilizado** (como `bin()`, `oct()`, `hex()`, ou `int(s, base)`). Todo o processamento matemático foi implementado na raça, através de lógica posicional, agrupamento de bits e divisões/multiplicações sucessivas.

## Requisitos Funcionais Implementados

O sistema atende integralmente aos 10 requisitos funcionais (F1 a F10) exigidos na especificação:

* **F1 e F2 (Conversão de Inteiros):** Decimal para bases 2, 8 e 16 por divisões sucessivas, e o caminho inverso (qualquer base para Decimal) via somatório posicional.
* **F3 e F4 (Conversões Diretas):** Conversão rápida por agrupamento de bits (3 bits para octal, 4 bits para hexadecimal) sem passar pelo decimal, utilizando o binário como base intermediária.
* **F5 (Validação de Entrada):** Rejeição estrita de dígitos numéricos e alfabéticos inválidos para a base de origem selecionada, acompanhada de mensagens de erro claras ao usuário.
* **F6 (Fracionários e Proteção IEEE 754):** Suporte a números com vírgula em todas as bases. Limitado por segurança a 16 casas decimais para lidar com imprecisões de ponto flutuante, com indicação explícita em tela quando ocorre truncamento de dízimas periódicas.
* **F7 (Modo Passo-a-Passo):** Impressão do trace detalhado do algoritmo (tabela de divisões, restos, agrupamentos e somatório posicional), ideal para conferência manual de cálculos.
* **F8 (Modo Batch via CSV):** Leitura automática em lote de um arquivo `entrada.csv` e gravação direta dos resultados formatados no arquivo `saida.csv`.
* **F9 (Modo Quiz):** Modo interativo contendo 5 níveis de dificuldade crescente para o usuário testar cálculos mentais de conversão, com sistema de pontuação.
* **F10 (Calculadora de Limites):** Ferramenta que, dado um número de $k$ bits, calcula e exibe o maior valor representável simultaneamente nas quatro bases.

## Estrutura Modular do Projeto

Projeto_pratico1_conversor-universal/
├── src/
│   ├── parser.py       # Validação e tratamento de entradas do usuário (F5)
│   ├── conversor.py    # Núcleo de algoritmos matemáticos (F1 a F4, F6)
│   ├── formatador.py   # Formatação de saídas e exibição do trace (F7)
│   └── main.py         # Orquestrador e menus interativos (F8 a F10)
├── tests/
│   ├── test_conversor.py   # Suíte contendo 32 casos de teste automatizados
│   └── entrada.csv         # Arquivo modelo para execução do Modo Batch
└── README.md


## 💻 Como Executar o Projeto (Modo Interativo)

1. Clone o repositório e navegue até a pasta raiz:
   git clone https://github.com/augustouser1/Projeto_pratico1_conversor-universal.git
   cd Projeto_pratico1_conversor-universal
   
2. Execute o inicializador principal pelo terminal:
   python3 src/main.py

## Avaliação e Testes Automatizados

Conforme a especificação técnica, o projeto está preparado para correção massiva através de dois métodos:

### 1. Suíte de Testes Automatizados (32 Casos)
A suíte de testes (`test_conversor.py`) utiliza a biblioteca `pytest` e cobre as conversões fundamentais de inteiros e fracionários, incluindo os testes de borda para truncamento. Para executar todos os testes com um único comando, garantindo o reconhecimento do módulo `src`, execute na raiz do projeto:

python3 -m pytest

### 2. Modo Batch (Requisito F8)
Para testar o processamento em lote com novos dados, garanta que o arquivo de entrada obedece ao formato delimitado por ponto e vírgula:
1. Posicione o arquivo com o nome `entrada.csv` na raiz do projeto contendo o cabeçalho exato: `valor; base_origem; base_destino`.
2. Execute o menu principal (`python3 src/main.py`) e selecione a opção de Modo Batch CSV.
3. O sistema fará a leitura segura e exportará automaticamente o arquivo `saida.csv` na mesma pasta, contendo: `valor; base_origem; resultado; base_destino`.

## Autores

* **Augusto Corrêa Silva Bitencourt** (Ciência da Computação - 1º Período)
* **João Pedro** (Ciência da Computação - 1º Período)
