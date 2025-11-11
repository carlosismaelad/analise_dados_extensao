.DEFAULT_GOAL := run
.PHONY: help env install clean run test format lint all

# Variáveis
PYTHON := python
VENV := .venv
VENV_BIN := $(VENV)/Scripts
PIP := $(VENV_BIN)/pip
PYTHON_VENV := $(VENV_BIN)/python

# Detectar se o ambiente virtual está ativo
ifdef VIRTUAL_ENV
	PYTHON_CMD := python
	PIP_CMD := pip
else
	PYTHON_CMD := $(PYTHON_VENV)
	PIP_CMD := $(PIP)
endif

## help: Mostra esta mensagem de ajuda
help:
	@echo "Comandos disponíveis:"
	@echo "  make          - Configura o ambiente e executa o projeto (padrão)"
	@echo "  make run      - Executa a análise de dados"
	@echo "  make env      - Cria o ambiente virtual Python"
	@echo "  make install  - Instala as dependências do projeto"
	@echo "  make clean    - Remove arquivos gerados e cache"
	@echo "  make all      - Configura tudo do zero e executa"
	@echo "  make format   - Formata o código com black"
	@echo "  make lint     - Verifica o código com flake8"
	@echo ""

## env: Cria o ambiente virtual Python
env:
	@echo "Criando ambiente virtual..."
	@if not exist $(VENV) ($(PYTHON) -m venv $(VENV))
	@echo "✓ Ambiente virtual criado: $(VENV)"

## install: Instala/atualiza as dependências
install: env
	@echo "Instalando dependências..."
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements.txt
	@echo "✓ Dependências instaladas com sucesso"

## run: Executa a análise de dados
run:
	@echo "Executando análise de dados CSAT..."
	@if not exist $(VENV) (echo "Ambiente virtual não encontrado. Execute 'make install' primeiro." && exit 1)
	@$(PYTHON_CMD) main.py
	@echo ""
	@echo "✓ Análise concluída! Verifique os gráficos gerados."

## clean: Remove arquivos gerados e cache
clean:
	@echo "Limpando arquivos gerados..."
	@if exist grafico_*.png (del /Q grafico_*.png)
	@if exist __pycache__ (rmdir /S /Q __pycache__)
	@if exist *.pyc (del /Q *.pyc)
	@echo "✓ Arquivos limpos"

## clean-all: Remove tudo incluindo o ambiente virtual
clean-all: clean
	@echo "Removendo ambiente virtual..."
	@if exist $(VENV) (rmdir /S /Q $(VENV))
	@echo "✓ Ambiente virtual removido"

## all: Configura tudo do zero e executa
all: clean-all env install run

## format: Formata o código com black (opcional)
format:
	@echo "Formatando código..."
	@$(PYTHON_CMD) -m black main.py 2>nul || echo "Black não instalado. Execute: pip install black"

## lint: Verifica o código com flake8 (opcional)
lint:
	@echo "Verificando código..."
	@$(PYTHON_CMD) -m flake8 main.py 2>nul || echo "Flake8 não instalado. Execute: pip install flake8"

## check: Verifica se o ambiente está configurado
check:
	@echo "Verificando configuração..."
	@if not exist $(VENV) (echo "✗ Ambiente virtual não encontrado" && exit 1) else (echo "✓ Ambiente virtual OK")
	@if not exist requirements.txt (echo "✗ requirements.txt não encontrado" && exit 1) else (echo "✓ requirements.txt OK")
	@if not exist main.py (echo "✗ main.py não encontrado" && exit 1) else (echo "✓ main.py OK")
	@if not exist analise_suporte.xlsx (echo "✗ analise_suporte.xlsx não encontrado" && exit 1) else (echo "✓ analise_suporte.xlsx OK")
	@echo "✓ Configuração OK!"

# Atalhos convenientes
.PHONY: setup start
setup: install
start: run