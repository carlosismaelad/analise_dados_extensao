# =====================================
# Script de Automação - Análise CSAT
# =====================================

param(
    [Parameter(Position=0)]
    [string]$Command = "run"
)

$VENV = ".venv"
$PYTHON_VENV = "$VENV\Scripts\python.exe"
$PIP_VENV = "$VENV\Scripts\pip.exe"

function Show-Help {
    Write-Host ""
    Write-Host "==================================================" -ForegroundColor Cyan
    Write-Host "  Análise de Dados CSAT - Comandos Disponíveis  " -ForegroundColor Cyan
    Write-Host "==================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  .\run.ps1          - Executa a análise (padrão)" -ForegroundColor Green
    Write-Host "  .\run.ps1 run      - Executa a análise de dados" -ForegroundColor White
    Write-Host "  .\run.ps1 env      - Cria o ambiente virtual" -ForegroundColor White
    Write-Host "  .\run.ps1 install  - Instala as dependências" -ForegroundColor White
    Write-Host "  .\run.ps1 clean    - Remove arquivos gerados" -ForegroundColor White
    Write-Host "  .\run.ps1 clean-all - Remove tudo (incluindo venv)" -ForegroundColor White
    Write-Host "  .\run.ps1 all      - Setup completo e execução" -ForegroundColor White
    Write-Host "  .\run.ps1 check    - Verifica a configuração" -ForegroundColor White
    Write-Host "  .\run.ps1 list     - Lista bibliotecas instaladas" -ForegroundColor White
    Write-Host "  .\run.ps1 help     - Mostra esta mensagem" -ForegroundColor White
    Write-Host ""
}

function List-Packages {
    Write-Host ""
    Write-Host "Bibliotecas instaladas no ambiente virtual:" -ForegroundColor Cyan
    Write-Host ""
    
    if (-not (Test-Path $PYTHON_VENV)) {
        Write-Host "✗ Ambiente virtual não encontrado!" -ForegroundColor Red
        Write-Host "Execute: .\run.ps1 install" -ForegroundColor Yellow
        exit 1
    }
    
    & $PIP_VENV list
    Write-Host ""
}

function Create-Env {
    Write-Host "Criando ambiente virtual..." -ForegroundColor Yellow
    if (Test-Path $VENV) {
        Write-Host "✓ Ambiente virtual já existe" -ForegroundColor Green
    } else {
        python -m venv $VENV
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Ambiente virtual criado: $VENV" -ForegroundColor Green
        } else {
            Write-Host "✗ Erro ao criar ambiente virtual" -ForegroundColor Red
            exit 1
        }
    }
}

function Install-Dependencies {
    Write-Host "Instalando dependências..." -ForegroundColor Yellow
    
    if (-not (Test-Path $VENV)) {
        Write-Host "Ambiente virtual não encontrado. Criando..." -ForegroundColor Yellow
        Create-Env
    }
    
    # Verifica se o pip do venv existe
    if (-not (Test-Path $PIP_VENV)) {
        Write-Host "✗ Erro: pip do ambiente virtual não encontrado!" -ForegroundColor Red
        Write-Host "Recriando ambiente virtual..." -ForegroundColor Yellow
        if (Test-Path $VENV) {
            Remove-Item $VENV -Recurse -Force
        }
        Create-Env
    }
    
    Write-Host "Atualizando pip no ambiente virtual..." -ForegroundColor Cyan
    & $PIP_VENV install --upgrade pip --quiet
    
    Write-Host "Instalando pacotes no ambiente virtual..." -ForegroundColor Cyan
    & $PIP_VENV install -r requirements.txt --quiet
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Dependências instaladas com sucesso no ambiente virtual" -ForegroundColor Green
        Write-Host "✓ Localização: $VENV" -ForegroundColor Green
    } else {
        Write-Host "✗ Erro ao instalar dependências" -ForegroundColor Red
        exit 1
    }
}

function Run-Analysis {
    Write-Host ""
    Write-Host "=====================================" -ForegroundColor Cyan
    Write-Host "  Executando Análise de Dados CSAT  " -ForegroundColor Cyan
    Write-Host "=====================================" -ForegroundColor Cyan
    Write-Host ""
    
    # Se o ambiente virtual não existir, criar e instalar tudo
    if (-not (Test-Path $VENV)) {
        Write-Host "Ambiente virtual não encontrado. Configurando..." -ForegroundColor Yellow
        Create-Env
        Install-Dependencies
    }
    
    # Verifica se o Python do venv existe
    if (-not (Test-Path $PYTHON_VENV)) {
        Write-Host "✗ Erro: Python do ambiente virtual não encontrado!" -ForegroundColor Red
        Write-Host "Execute: .\run.ps1 install" -ForegroundColor Yellow
        exit 1
    }
    
    if (-not (Test-Path "analise_suporte.xlsx")) {
        Write-Host "✗ Arquivo analise_suporte.xlsx não encontrado!" -ForegroundColor Red
        exit 1
    }
    
    & $PYTHON_VENV main.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✓ Análise concluída com sucesso!" -ForegroundColor Green
        Write-Host "✓ Verifique os gráficos gerados na pasta do projeto" -ForegroundColor Green
        Write-Host ""
    } else {
        Write-Host ""
        Write-Host "✗ Erro ao executar a análise" -ForegroundColor Red
        exit 1
    }
}

function Clean-Files {
    Write-Host "Limpando arquivos gerados..." -ForegroundColor Yellow
    
    # Remove gráficos
    if (Test-Path "grafico_*.png") {
        Remove-Item "grafico_*.png" -Force
        Write-Host "✓ Gráficos removidos" -ForegroundColor Green
    }
    
    # Remove cache Python
    if (Test-Path "__pycache__") {
        Remove-Item "__pycache__" -Recurse -Force
        Write-Host "✓ Cache Python removido" -ForegroundColor Green
    }
    
    Get-ChildItem -Filter "*.pyc" -Recurse | Remove-Item -Force
    
    Write-Host "✓ Limpeza concluída" -ForegroundColor Green
}

function Clean-All {
    Clean-Files
    
    Write-Host "Removendo ambiente virtual..." -ForegroundColor Yellow
    if (Test-Path $VENV) {
        Remove-Item $VENV -Recurse -Force
        Write-Host "✓ Ambiente virtual removido" -ForegroundColor Green
    }
}

function Check-Setup {
    Write-Host ""
    Write-Host "Verificando configuração..." -ForegroundColor Cyan
    Write-Host ""
    
    $allOk = $true
    
    # Verifica Python
    try {
        $pythonVersion = python --version
        Write-Host "✓ Python instalado: $pythonVersion" -ForegroundColor Green
    } catch {
        Write-Host "✗ Python não encontrado" -ForegroundColor Red
        $allOk = $false
    }
    
    # Verifica ambiente virtual
    if (Test-Path $VENV) {
        Write-Host "✓ Ambiente virtual: OK" -ForegroundColor Green
    } else {
        Write-Host "✗ Ambiente virtual não encontrado" -ForegroundColor Red
        $allOk = $false
    }
    
    # Verifica requirements.txt
    if (Test-Path "requirements.txt") {
        Write-Host "✓ requirements.txt: OK" -ForegroundColor Green
    } else {
        Write-Host "✗ requirements.txt não encontrado" -ForegroundColor Red
        $allOk = $false
    }
    
    # Verifica main.py
    if (Test-Path "main.py") {
        Write-Host "✓ main.py: OK" -ForegroundColor Green
    } else {
        Write-Host "✗ main.py não encontrado" -ForegroundColor Red
        $allOk = $false
    }
    
    # Verifica planilha
    if (Test-Path "analise_suporte.xlsx") {
        Write-Host "✓ analise_suporte.xlsx: OK" -ForegroundColor Green
    } else {
        Write-Host "✗ analise_suporte.xlsx não encontrado" -ForegroundColor Red
        $allOk = $false
    }
    
    Write-Host ""
    if ($allOk) {
        Write-Host "✓ Configuração completa! Você pode executar: .\run.ps1 run" -ForegroundColor Green
    } else {
        Write-Host "✗ Configuração incompleta. Execute: .\run.ps1 install" -ForegroundColor Yellow
    }
    Write-Host ""
}

function Run-All {
    Write-Host "Executando setup completo..." -ForegroundColor Cyan
    Clean-All
    Create-Env
    Install-Dependencies
    Run-Analysis
}

# Executa o comando solicitado
switch ($Command.ToLower()) {
    "help" { Show-Help }
    "env" { Create-Env }
    "install" { Install-Dependencies }
    "run" { Run-Analysis }
    "clean" { Clean-Files }
    "clean-all" { Clean-All }
    "all" { Run-All }
    "check" { Check-Setup }
    "list" { List-Packages }
    default { Run-Analysis }
}
