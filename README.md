# 📊 Análise de Dados CSAT - Satisfação do Cliente

Projeto educacional para análise de dados, probabilidades e estatísticas aplicado a métricas de satisfação do cliente (CSAT) em um time de suporte.

## 📋 Descrição

Este projeto analisa dados de avaliação CSAT (Customer Satisfaction Score) de atendentes de suporte, identificando:

- ✅ Resultados individuais de cada atendente
- 📈 Ranking de desempenho por média CSAT
- 📊 Tipos de contato com melhores e piores avaliações
- 🎯 Pontos fortes e fracos de cada atendente
- ⚠️ Processos com mais notas baixas
- 📉 Probabilidade de cada atendente receber nota baixa
- 💡 Recomendações estratégicas para treinamento e melhoria

## 🎓 Objetivo Educacional

Demonstrar conceitos práticos de:

- Análise exploratória de dados
- Estatística descritiva (média, mediana, desvio padrão)
- Probabilidades
- Visualização de dados com gráficos
- Tomada de decisão baseada em dados

## 🚀 Como Executar o Projeto

### ⚡ Execução Rápida (Recomendado)

Ambos os métodos abaixo criam automaticamente o ambiente virtual, instalam todas as dependências dentro dele e executam o projeto:

#### **Windows (PowerShell)**

```powershell
.\run.ps1
```

#### **Linux/macOS (com Make instalado)**

```bash
make
```

Pronto! O script faz tudo automaticamente:

1. ✅ Cria o ambiente virtual Python (.venv)
2. ✅ Instala todas as dependências dentro do ambiente virtual
3. ✅ Executa a análise completa
4. ✅ Gera todos os gráficos

---

## 📦 Requisitos

- Python 3.8 ou superior
- Arquivo `analise_suporte.xlsx` (planilha de dados)

### Dependências Python

Todas instaladas automaticamente:

```
pandas
openpyxl
matplotlib
seaborn
numpy
```

---

## 🎮 Comandos Disponíveis

### Windows (PowerShell)

```powershell
.\run.ps1           # Executa o projeto (cria venv automaticamente)
.\run.ps1 help      # Mostra todos os comandos disponíveis
.\run.ps1 install   # Apenas instala as dependências
.\run.ps1 list      # Lista bibliotecas instaladas no venv
.\run.ps1 check     # Verifica se tudo está configurado
.\run.ps1 clean     # Remove gráficos gerados
.\run.ps1 clean-all # Remove tudo incluindo ambiente virtual
.\run.ps1 all       # Setup completo do zero
```

### Linux/macOS (Make)

```bash
make              # Executa o projeto (cria venv automaticamente)
make help         # Mostra todos os comandos disponíveis
make install      # Apenas instala as dependências
make check        # Verifica se tudo está configurado
make clean        # Remove gráficos gerados
make clean-all    # Remove tudo incluindo ambiente virtual
make all          # Setup completo do zero
```

### Execução Manual (Opcional)

Se preferir fazer manualmente:

**Windows:**

```powershell
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
.\.venv\Scripts\Activate.ps1

# Instalar dependências
pip install -r requirements.txt

# Executar análise
python main.py
```

**Linux/macOS:**

```bash
# Criar ambiente virtual
python3 -m venv .venv

# Ativar ambiente virtual
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Executar análise
python main.py
```

---

## 📊 Estrutura do Projeto

```
analise_dados_extensao/
├── main.py                    # Script principal de análise
├── analise_suporte.xlsx       # Dados de entrada (planilha)
├── requirements.txt           # Dependências Python
├── run.ps1                    # Script de automação Windows
├── Makefile                   # Script de automação Linux/macOS
├── README.md                  # Este arquivo
├── .venv/                     # Ambiente virtual (criado automaticamente)
└── grafico_*.png              # Gráficos gerados (saída)
```

---

## 📈 Saídas Geradas

Após a execução, os seguintes arquivos serão criados:

### Gráficos (PNG)

1. **grafico_1_resultados_individuais.png** - Média e distribuição por atendente
2. **grafico_2_ranking_atendentes.png** - Ranking de desempenho
3. **grafico_3_ranking_tipos_contato.png** - Análise por tipo de contato
4. **grafico_4_heatmap_desempenho.png** - Heatmap de desempenho completo
5. **grafico_6_processos_problematicos.png** - Processos com mais problemas
6. **grafico_8_probabilidade_nota_baixa.png** - Análise de risco
7. **grafico_9_dashboard_recomendacoes.png** - Dashboard executivo completo

### Console

- Relatório detalhado com todas as análises
- Estatísticas por atendente
- Recomendações estratégicas

---

## 📊 Estrutura dos Dados

A planilha `analise_suporte.xlsx` deve conter as seguintes colunas:

| Coluna         | Descrição                | Exemplo                                                  |
| -------------- | ------------------------ | -------------------------------------------------------- |
| `attendant`    | Nome do atendente        | "João Silva"                                             |
| `contact type` | Tipo de atendimento      | "coletagem", "tributação", etc.                          |
| `csat`         | Nota de satisfação (1-5) | 4                                                        |
| `opportunity`  | Contexto da avaliação    | "fluxo do processo", "cliente resistente", "operacional" |

---

## 🛠️ Solução de Problemas

### Windows: "run.ps1 cannot be loaded because running scripts is disabled"

Execute no PowerShell como Administrador:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Linux/macOS: "make: command not found"

Instale o Make:

```bash
# Ubuntu/Debian
sudo apt-get install make

# macOS
xcode-select --install

# Ou use diretamente:
python3 main.py
```

### "analise_suporte.xlsx not found"

Certifique-se de que o arquivo de dados está na pasta raiz do projeto.

---

## 🎯 Análises Realizadas

1. **Resultados Individuais** - Estatísticas completas por atendente (média, mediana, desvio padrão)
2. **Ranking de Atendentes** - Ordenação por desempenho (melhor → pior)
3. **Análise de Tipos de Contato** - Quais tipos recebem melhores/piores avaliações
4. **Pontos Fortes** - Onde cada atendente se destaca
5. **Pontos Fracos** - Onde cada atendente tem dificuldades
6. **Processos Problemáticos** - Top 5 processos com mais notas baixas (<3)
7. **Análise Detalhada Individual** - Breakdown completo por atendente
8. **Probabilidade de Risco** - Chance de receber nota baixa por atendente
9. **Recomendações Estratégicas** - Ações de melhoria baseadas em dados

---

## 👨‍🎓 Uso em Aulas

Este projeto é ideal para:

- Aulas de análise de dados
- Workshops de Python para dados
- Ensino de estatística aplicada
- Demonstração de visualização de dados
- Cases de tomada de decisão baseada em dados

---

## 📝 Licença

Projeto educacional de código aberto.

---

## 👤 Autor

Carlos Dourado

- GitHub: [@carlosismaelad](https://github.com/carlosismaelad)

---

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:

- Reportar bugs
- Sugerir novas análises
- Melhorar a documentação
- Adicionar novos gráficos

---

**⭐ Se este projeto foi útil, deixe uma estrela no repositório!**
