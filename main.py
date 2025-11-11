import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configurações de visualização
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

# ============================================================================
# ANÁLISE DE DADOS - SATISFAÇÃO DO CLIENTE (CSAT)
# Projeto educacional: Probabilidade, Estatística e Análise de Dados
# ============================================================================

def carregar_dados():
    """Carrega a planilha de análise de suporte"""
    df = pd.read_excel('analise_suporte.xlsx')
    print("=" * 80)
    print("DADOS CARREGADOS COM SUCESSO")
    print("=" * 80)
    print(f"Total de registros: {len(df)}")
    print(f"Colunas: {list(df.columns)}")
    print(f"\nPrimeiras linhas:")
    print(df.head())
    print("\n" * 2)
    return df


def analise_1_resultados_individuais(df):
    """1 - Avaliar os resultados individuais de cada atendente"""
    print("=" * 80)
    print("1. RESULTADOS INDIVIDUAIS DE CADA ATENDENTE")
    print("=" * 80)
    
    resultados = df.groupby('attendant').agg({
        'csat': ['mean', 'median', 'std', 'count', 'min', 'max', 'sum']
    }).round(2)
    
    resultados.columns = ['Média', 'Mediana', 'Desvio Padrão', 'Total Avaliações', 'Nota Mín', 'Nota Máx', 'Soma']
    
    print(resultados)
    print("\n" * 2)
    
    # Gráfico 1: Média CSAT por atendente com barras de erro (desvio padrão)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    resultados_sorted = resultados.sort_values('Média', ascending=True)
    ax1.barh(resultados_sorted.index, resultados_sorted['Média'], 
             xerr=resultados_sorted['Desvio Padrão'], capsize=5, alpha=0.7)
    ax1.set_xlabel('Média CSAT')
    ax1.set_title('Média CSAT por Atendente (com desvio padrão)')
    ax1.axvline(df['csat'].mean(), color='red', linestyle='--', label='Média Geral')
    ax1.legend()
    ax1.grid(axis='x', alpha=0.3)
    
    # Gráfico 2: Distribuição de notas por atendente (boxplot)
    df_sorted_attendants = df.copy()
    df_sorted_attendants['attendant'] = pd.Categorical(
        df_sorted_attendants['attendant'],
        categories=resultados_sorted.index,
        ordered=True
    )
    df_sorted_attendants = df_sorted_attendants.sort_values('attendant')
    
    sns.boxplot(data=df_sorted_attendants, y='attendant', x='csat', ax=ax2)
    ax2.set_xlabel('CSAT')
    ax2.set_ylabel('')
    ax2.set_title('Distribuição de Notas por Atendente')
    ax2.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('grafico_1_resultados_individuais.png', dpi=300, bbox_inches='tight')
    print("📊 Gráfico salvo: grafico_1_resultados_individuais.png")
    plt.close()
    
    return resultados


def analise_2_ranking_atendentes(df):
    """2 - Mapear os atendentes com melhores resultados em ordem decrescente"""
    print("=" * 80)
    print("2. RANKING DE ATENDENTES (Maior para Menor Média)")
    print("=" * 80)
    
    ranking = df.groupby('attendant').agg({
        'csat': ['mean', 'count']
    }).round(2)
    
    ranking.columns = ['Média CSAT', 'Total Avaliações']
    ranking = ranking.sort_values('Média CSAT', ascending=False)
    ranking['Posição'] = range(1, len(ranking) + 1)
    ranking = ranking[['Posição', 'Média CSAT', 'Total Avaliações']]
    
    print(ranking)
    print("\n" * 2)
    
    # Gráfico 2: Ranking de Atendentes
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Gráfico de barras horizontais
    colors = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(ranking)))
    ax1.barh(range(len(ranking)), ranking['Média CSAT'], color=colors)
    ax1.set_yticks(range(len(ranking)))
    ax1.set_yticklabels(ranking.index)
    ax1.set_xlabel('Média CSAT')
    ax1.set_title('Ranking de Atendentes por Média CSAT')
    ax1.invert_yaxis()
    ax1.axvline(df['csat'].mean(), color='red', linestyle='--', label='Média Geral')
    ax1.legend()
    ax1.grid(axis='x', alpha=0.3)
    
    # Adicionar valores nas barras
    for i, (idx, row) in enumerate(ranking.iterrows()):
        ax1.text(row['Média CSAT'] + 0.05, i, f"{row['Média CSAT']:.2f}", 
                va='center', fontsize=9)
    
    # Gráfico de barras com total de avaliações
    ax2.bar(range(len(ranking)), ranking['Total Avaliações'], color='skyblue', alpha=0.7)
    ax2.set_xticks(range(len(ranking)))
    ax2.set_xticklabels(ranking.index, rotation=45, ha='right')
    ax2.set_ylabel('Total de Avaliações')
    ax2.set_title('Volume de Avaliações por Atendente')
    ax2.grid(axis='y', alpha=0.3)
    
    # Adicionar valores nas barras
    for i, (idx, row) in enumerate(ranking.iterrows()):
        ax2.text(i, row['Total Avaliações'] + 1, f"{int(row['Total Avaliações'])}", 
                ha='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('grafico_2_ranking_atendentes.png', dpi=300, bbox_inches='tight')
    print("📊 Gráfico salvo: grafico_2_ranking_atendentes.png")
    plt.close()
    
    return ranking


def analise_3_ranking_tipos_contato(df):
    """3 - Mapear os tipos de contato em ordem decrescente por avaliação"""
    print("=" * 80)
    print("3. RANKING DE TIPOS DE CONTATO (Melhores para Piores Notas)")
    print("=" * 80)
    
    ranking_tipos = df.groupby('contact type').agg({
        'csat': ['mean', 'count']
    }).round(2)
    
    ranking_tipos.columns = ['Média CSAT', 'Total Avaliações']
    ranking_tipos = ranking_tipos.sort_values('Média CSAT', ascending=False)
    
    print(ranking_tipos)
    print("\n" * 2)
    
    # Gráfico 3: Ranking de Tipos de Contato
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    
    x = range(len(ranking_tipos))
    width = 0.35
    
    # Barras para média
    bars1 = ax.bar([i - width/2 for i in x], ranking_tipos['Média CSAT'], 
                   width, label='Média CSAT', alpha=0.8, color='coral')
    
    # Criar segundo eixo Y para total de avaliações
    ax2 = ax.twinx()
    bars2 = ax2.bar([i + width/2 for i in x], ranking_tipos['Total Avaliações'], 
                    width, label='Total Avaliações', alpha=0.8, color='steelblue')
    
    ax.set_xlabel('Tipo de Contato')
    ax.set_ylabel('Média CSAT', color='coral')
    ax2.set_ylabel('Total de Avaliações', color='steelblue')
    ax.set_title('Ranking de Tipos de Contato por Média CSAT e Volume')
    ax.set_xticks(x)
    ax.set_xticklabels(ranking_tipos.index, rotation=45, ha='right')
    ax.tick_params(axis='y', labelcolor='coral')
    ax2.tick_params(axis='y', labelcolor='steelblue')
    
    # Adicionar valores nas barras
    for i, (idx, row) in enumerate(ranking_tipos.iterrows()):
        ax.text(i - width/2, row['Média CSAT'] + 0.05, f"{row['Média CSAT']:.2f}", 
               ha='center', fontsize=8)
        ax2.text(i + width/2, row['Total Avaliações'] + 1, f"{int(row['Total Avaliações'])}", 
                ha='center', fontsize=8)
    
    # Legendas
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
    
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('grafico_3_ranking_tipos_contato.png', dpi=300, bbox_inches='tight')
    print("📊 Gráfico salvo: grafico_3_ranking_tipos_contato.png")
    plt.close()
    
    return ranking_tipos


def analise_4_melhores_tipos_contato_por_atendente(df):
    """4 - Identificar os tipos de contato onde os atendentes se saem melhor"""
    print("=" * 80)
    print("4. TIPOS DE CONTATO ONDE CADA ATENDENTE SE SAI MELHOR")
    print("=" * 80)
    
    pivot = df.groupby(['attendant', 'contact type'])['csat'].mean().round(2)
    
    # Para cada atendente, encontrar o melhor tipo de contato
    melhores = []
    for atendente in df['attendant'].unique():
        dados_atendente = pivot[atendente]
        melhor_tipo = dados_atendente.idxmax()
        melhor_media = dados_atendente.max()
        total = len(df[(df['attendant'] == atendente) & (df['contact type'] == melhor_tipo)])
        melhores.append({
            'Atendente': atendente,
            'Melhor Tipo de Contato': melhor_tipo,
            'Média CSAT': melhor_media,
            'Qtd Avaliações': total
        })
    
    df_melhores = pd.DataFrame(melhores).sort_values('Média CSAT', ascending=False)
    print(df_melhores.to_string(index=False))
    print("\n" * 2)
    
    # Gráfico 4: Heatmap de desempenho por atendente e tipo de contato
    pivot_table = df.pivot_table(values='csat', index='attendant', 
                                  columns='contact type', aggfunc='mean')
    
    fig, ax = plt.subplots(figsize=(14, 8))
    sns.heatmap(pivot_table, annot=True, fmt='.2f', cmap='RdYlGn', 
                center=df['csat'].mean(), ax=ax, cbar_kws={'label': 'Média CSAT'})
    ax.set_title('Heatmap: Desempenho por Atendente e Tipo de Contato')
    ax.set_xlabel('Tipo de Contato')
    ax.set_ylabel('Atendente')
    plt.tight_layout()
    plt.savefig('grafico_4_heatmap_desempenho.png', dpi=300, bbox_inches='tight')
    print("📊 Gráfico salvo: grafico_4_heatmap_desempenho.png")
    plt.close()
    
    return df_melhores


def analise_5_piores_tipos_contato_por_atendente(df):
    """5 - Identificar os tipos de contato em que os atendentes se saem pior"""
    print("=" * 80)
    print("5. TIPOS DE CONTATO ONDE CADA ATENDENTE TEM MAIS DIFICULDADE")
    print("=" * 80)
    
    pivot = df.groupby(['attendant', 'contact type'])['csat'].mean().round(2)
    
    # Para cada atendente, encontrar o pior tipo de contato
    piores = []
    for atendente in df['attendant'].unique():
        dados_atendente = pivot[atendente]
        pior_tipo = dados_atendente.idxmin()
        pior_media = dados_atendente.min()
        total = len(df[(df['attendant'] == atendente) & (df['contact type'] == pior_tipo)])
        piores.append({
            'Atendente': atendente,
            'Pior Tipo de Contato': pior_tipo,
            'Média CSAT': pior_media,
            'Qtd Avaliações': total
        })
    
    df_piores = pd.DataFrame(piores).sort_values('Média CSAT')
    print(df_piores.to_string(index=False))
    print("\n" * 2)
    return df_piores


def analise_6_processos_notas_baixas(df):
    """6 - Mapear os 5 processos com mais notas baixas (abaixo de 3) devido fluxo do processo"""
    print("=" * 80)
    print("6. TOP 5 PROCESSOS COM MAIS NOTAS BAIXAS (<3) - FLUXO DO PROCESSO")
    print("=" * 80)
    
    # Filtrar notas baixas e opportunity = "fluxo do processo"
    notas_baixas = df[(df['csat'] < 3) & (df['opportunity'] == 'fluxo do processo')]
    
    # Contar por tipo de contato
    processos_problematicos = notas_baixas.groupby('contact type').agg({
        'csat': ['count', 'mean']
    }).round(2)
    
    processos_problematicos.columns = ['Qtd Notas Baixas', 'Média Dessas Notas']
    processos_problematicos = processos_problematicos.sort_values('Qtd Notas Baixas', ascending=False).head(5)
    
    print(processos_problematicos)
    print("\n" * 2)
    
    # Gráfico 6: Processos com mais notas baixas
    if len(processos_problematicos) > 0:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Gráfico de barras para quantidade de notas baixas
        ax1.barh(range(len(processos_problematicos)), 
                processos_problematicos['Qtd Notas Baixas'], 
                color='crimson', alpha=0.7)
        ax1.set_yticks(range(len(processos_problematicos)))
        ax1.set_yticklabels(processos_problematicos.index)
        ax1.set_xlabel('Quantidade de Notas Baixas (CSAT < 3)')
        ax1.set_title('Top 5 Processos com Mais Notas Baixas\n(Fluxo do Processo)')
        ax1.invert_yaxis()
        ax1.grid(axis='x', alpha=0.3)
        
        # Adicionar valores
        for i, (idx, row) in enumerate(processos_problematicos.iterrows()):
            ax1.text(row['Qtd Notas Baixas'] + 0.2, i, 
                    f"{int(row['Qtd Notas Baixas'])}", va='center')
        
        # Análise por tipo de opportunity
        opportunity_stats = df.groupby('opportunity').agg({
            'csat': ['mean', 'count']
        }).round(2)
        opportunity_stats.columns = ['Média', 'Qtd']
        
        colors_opp = ['crimson' if x < 3 else 'gold' if x < 4 else 'green' 
                     for x in opportunity_stats['Média']]
        
        ax2.bar(range(len(opportunity_stats)), opportunity_stats['Média'], 
               color=colors_opp, alpha=0.7)
        ax2.set_xticks(range(len(opportunity_stats)))
        ax2.set_xticklabels(opportunity_stats.index, rotation=45, ha='right')
        ax2.set_ylabel('Média CSAT')
        ax2.set_title('Média CSAT por Tipo de Opportunity')
        ax2.axhline(3, color='red', linestyle='--', alpha=0.5, label='Limite Nota Baixa')
        ax2.axhline(4, color='orange', linestyle='--', alpha=0.5, label='Limite Nota Média')
        ax2.legend()
        ax2.grid(axis='y', alpha=0.3)
        
        # Adicionar valores
        for i, (idx, row) in enumerate(opportunity_stats.iterrows()):
            ax2.text(i, row['Média'] + 0.1, f"{row['Média']:.2f}", ha='center')
        
        plt.tight_layout()
        plt.savefig('grafico_6_processos_problematicos.png', dpi=300, bbox_inches='tight')
        print("📊 Gráfico salvo: grafico_6_processos_problematicos.png")
        plt.close()
    
    return processos_problematicos


def analise_7_destaque_dificuldade_por_atendente(df):
    """7 - Entender onde cada atendente de suporte mais se destaca e onde tem mais dificuldade"""
    print("=" * 80)
    print("7. ANÁLISE DETALHADA: DESTAQUES E DIFICULDADES POR ATENDENTE")
    print("=" * 80)
    
    for atendente in sorted(df['attendant'].unique()):
        dados_atendente = df[df['attendant'] == atendente]
        
        print(f"\n{'─' * 80}")
        print(f"ATENDENTE: {atendente}")
        print(f"{'─' * 80}")
        
        # Estatísticas gerais
        print(f"Média Geral: {dados_atendente['csat'].mean():.2f}")
        print(f"Total de Avaliações: {len(dados_atendente)}")
        
        # Performance por tipo de contato
        print(f"\nPerformance por Tipo de Contato:")
        perf_tipo = dados_atendente.groupby('contact type').agg({
            'csat': ['mean', 'count']
        }).round(2)
        perf_tipo.columns = ['Média', 'Qtd']
        perf_tipo = perf_tipo.sort_values('Média', ascending=False)
        print(perf_tipo)
        
        # Performance por opportunity
        print(f"\nPerformance por Tipo de Opportunity:")
        perf_opp = dados_atendente.groupby('opportunity').agg({
            'csat': ['mean', 'count']
        }).round(2)
        perf_opp.columns = ['Média', 'Qtd']
        perf_opp = perf_opp.sort_values('Média', ascending=False)
        print(perf_opp)
        
        # Pontos fortes e fracos
        melhor_tipo = perf_tipo['Média'].idxmax()
        pior_tipo = perf_tipo['Média'].idxmin()
        print(f"\n✓ DESTAQUE: {melhor_tipo} (Média: {perf_tipo.loc[melhor_tipo, 'Média']})")
        print(f"✗ DIFICULDADE: {pior_tipo} (Média: {perf_tipo.loc[pior_tipo, 'Média']})")
    
    print("\n" * 2)


def analise_8_probabilidade_nota_baixa(df):
    """8 - Mapear qual o atendente tem probabilidade maior de receber uma nota baixa"""
    print("=" * 80)
    print("8. PROBABILIDADE DE NOTA BAIXA POR ATENDENTE (CSAT < 3)")
    print("=" * 80)
    
    # Definir nota baixa como < 3
    df['nota_baixa'] = df['csat'] < 3
    
    probabilidades = []
    for atendente in df['attendant'].unique():
        dados_atendente = df[df['attendant'] == atendente]
        total = len(dados_atendente)
        notas_baixas = dados_atendente['nota_baixa'].sum()
        probabilidade = (notas_baixas / total) * 100
        
        probabilidades.append({
            'Atendente': atendente,
            'Total Avaliações': total,
            'Notas Baixas': notas_baixas,
            'Probabilidade (%)': round(probabilidade, 2)
        })
    
    df_prob = pd.DataFrame(probabilidades).sort_values('Probabilidade (%)', ascending=False)
    print(df_prob.to_string(index=False))
    print("\n" * 2)
    
    # Gráfico 8: Probabilidade de nota baixa
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Gráfico de barras de probabilidade
    colors_prob = ['darkred' if x > 30 else 'orange' if x > 20 else 'yellowgreen' 
                   for x in df_prob['Probabilidade (%)']]
    
    ax1.barh(range(len(df_prob)), df_prob['Probabilidade (%)'], color=colors_prob, alpha=0.7)
    ax1.set_yticks(range(len(df_prob)))
    ax1.set_yticklabels(df_prob['Atendente'])
    ax1.set_xlabel('Probabilidade de Nota Baixa (%)')
    ax1.set_title('Probabilidade de Receber Nota Baixa (CSAT < 3) por Atendente')
    ax1.axvline(20, color='orange', linestyle='--', alpha=0.5, label='Limite Atenção (20%)')
    ax1.axvline(30, color='red', linestyle='--', alpha=0.5, label='Limite Crítico (30%)')
    ax1.legend()
    ax1.grid(axis='x', alpha=0.3)
    ax1.invert_yaxis()
    
    # Adicionar valores
    for i, (idx, row) in enumerate(df_prob.iterrows()):
        ax1.text(row['Probabilidade (%)'] + 1, i, f"{row['Probabilidade (%)']}%", 
                va='center', fontsize=9)
    
    # Distribuição geral de notas
    ax2.hist(df['csat'], bins=5, edgecolor='black', alpha=0.7, color='skyblue')
    ax2.axvline(df['csat'].mean(), color='red', linestyle='--', 
               linewidth=2, label=f'Média: {df["csat"].mean():.2f}')
    ax2.axvline(df['csat'].median(), color='green', linestyle='--', 
               linewidth=2, label=f'Mediana: {df["csat"].median():.2f}')
    ax2.set_xlabel('CSAT')
    ax2.set_ylabel('Frequência')
    ax2.set_title('Distribuição Geral de Notas CSAT')
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('grafico_8_probabilidade_nota_baixa.png', dpi=300, bbox_inches='tight')
    print("📊 Gráfico salvo: grafico_8_probabilidade_nota_baixa.png")
    plt.close()
    
    return df_prob


def analise_9_recomendacoes(df, prob_notas_baixas, ranking_atendentes):
    """9 - Recomendações para melhoria de processos e treinamentos"""
    print("=" * 80)
    print("9. RECOMENDAÇÕES ESTRATÉGICAS PARA MELHORIA")
    print("=" * 80)
    
    print("\n📊 ANÁLISE GERAL:")
    print(f"   • Média geral CSAT: {df['csat'].mean():.2f}")
    print(f"   • Total de avaliações: {len(df)}")
    print(f"   • Notas baixas (<3): {len(df[df['csat'] < 3])} ({(len(df[df['csat'] < 3])/len(df)*100):.1f}%)")
    print(f"   • Notas altas (>=4): {len(df[df['csat'] >= 4])} ({(len(df[df['csat'] >= 4])/len(df)*100):.1f}%)")
    
    print("\n🎯 RECOMENDAÇÕES DE TREINAMENTO:")
    
    # Identificar atendentes que precisam de treinamento (probabilidade de nota baixa > 20%)
    atendentes_treinamento = prob_notas_baixas[prob_notas_baixas['Probabilidade (%)'] > 20]
    
    if len(atendentes_treinamento) > 0:
        print(f"   • {len(atendentes_treinamento)} atendente(s) com alta probabilidade de notas baixas:")
        for _, row in atendentes_treinamento.iterrows():
            print(f"     - {row['Atendente']}: {row['Probabilidade (%)']}% de chance de nota baixa")
    
    # Identificar tipos de contato problemáticos
    print("\n🔧 PROCESSOS QUE NECESSITAM REVISÃO:")
    tipos_problematicos = df[df['csat'] < 3].groupby('contact type').size().sort_values(ascending=False).head(3)
    for tipo, qtd in tipos_problematicos.items():
        print(f"   • {tipo}: {qtd} notas baixas")
    
    # Identificar opportunities problemáticas
    print("\n⚠️ ANÁLISE POR TIPO DE OPPORTUNITY:")
    opp_stats = df.groupby('opportunity').agg({
        'csat': ['mean', 'count']
    }).round(2)
    opp_stats.columns = ['Média', 'Qtd']
    for opp, row in opp_stats.iterrows():
        print(f"   • {opp}: Média {row['Média']} ({row['Qtd']} avaliações)")
    
    # Melhores práticas
    print("\n⭐ MELHORES PRÁTICAS (Atendentes com melhor desempenho):")
    top_3 = ranking_atendentes.head(3)
    for idx, row in top_3.iterrows():
        print(f"   • {idx}: Média {row['Média CSAT']} - pode compartilhar conhecimento com a equipe")
    
    print("\n💡 AÇÕES RECOMENDADAS:")
    print("   1. Implementar programa de mentoria: atendentes top podem dar suporte aos com dificuldades")
    print("   2. Revisar fluxos de processo que geram mais insatisfação")
    print("   3. Criar treinamentos específicos para tipos de contato problemáticos")
    print("   4. Estabelecer metas individuais baseadas nas áreas de melhoria")
    print("   5. Realizar feedback contínuo com base nos dados de CSAT")
    print("   6. Investigar causas de notas baixas em 'cliente resistente'")
    print("   7. Documentar melhores práticas dos atendentes top performers")
    
    # Gráfico 9: Dashboard de Recomendações
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
    
    # 1. Pizza - Distribuição de notas
    ax1 = fig.add_subplot(gs[0, 0])
    bins = [0, 3, 4, 5.1]
    labels = ['Baixa (<3)', 'Média (3-4)', 'Alta (4-5)']
    colors_pie = ['crimson', 'gold', 'green']
    df['categoria'] = pd.cut(df['csat'], bins=bins, labels=labels, include_lowest=True)
    categoria_counts = df['categoria'].value_counts()
    ax1.pie(categoria_counts, labels=categoria_counts.index, autopct='%1.1f%%', 
           colors=colors_pie, startangle=90)
    ax1.set_title('Distribuição de Notas por Categoria')
    
    # 2. Comparação Top 3 vs Bottom 3
    ax2 = fig.add_subplot(gs[0, 1])
    top_3 = ranking_atendentes.head(3)
    bottom_3 = ranking_atendentes.tail(3)
    comparison = pd.concat([top_3, bottom_3])
    colors_comp = ['green']*3 + ['red']*3
    ax2.barh(range(len(comparison)), comparison['Média CSAT'], color=colors_comp, alpha=0.7)
    ax2.set_yticks(range(len(comparison)))
    ax2.set_yticklabels(comparison.index)
    ax2.set_xlabel('Média CSAT')
    ax2.set_title('Top 3 vs Bottom 3 Atendentes')
    ax2.axvline(df['csat'].mean(), color='black', linestyle='--', alpha=0.5)
    ax2.invert_yaxis()
    ax2.grid(axis='x', alpha=0.3)
    
    # 3. Notas por Opportunity
    ax3 = fig.add_subplot(gs[1, 0])
    opp_data = df.groupby('opportunity')['csat'].mean().sort_values()
    colors_opp = ['red' if x < 3 else 'gold' if x < 4 else 'green' for x in opp_data]
    ax3.barh(range(len(opp_data)), opp_data, color=colors_opp, alpha=0.7)
    ax3.set_yticks(range(len(opp_data)))
    ax3.set_yticklabels(opp_data.index)
    ax3.set_xlabel('Média CSAT')
    ax3.set_title('Média CSAT por Tipo de Opportunity')
    ax3.invert_yaxis()
    ax3.grid(axis='x', alpha=0.3)
    
    # 4. Volume de avaliações por atendente
    ax4 = fig.add_subplot(gs[1, 1])
    vol_data = df['attendant'].value_counts().sort_values(ascending=True)
    ax4.barh(range(len(vol_data)), vol_data, color='steelblue', alpha=0.7)
    ax4.set_yticks(range(len(vol_data)))
    ax4.set_yticklabels(vol_data.index)
    ax4.set_xlabel('Quantidade de Avaliações')
    ax4.set_title('Volume de Avaliações por Atendente')
    ax4.grid(axis='x', alpha=0.3)
    
    # 5. Tendência de probabilidade de nota baixa
    ax5 = fig.add_subplot(gs[2, :])
    prob_sorted = prob_notas_baixas.sort_values('Probabilidade (%)')
    x_pos = range(len(prob_sorted))
    bars = ax5.bar(x_pos, prob_sorted['Probabilidade (%)'], alpha=0.7)
    
    # Colorir barras baseado no nível de risco
    for i, (idx, row) in enumerate(prob_sorted.iterrows()):
        if row['Probabilidade (%)'] > 30:
            bars[i].set_color('darkred')
        elif row['Probabilidade (%)'] > 20:
            bars[i].set_color('orange')
        else:
            bars[i].set_color('green')
    
    ax5.set_xticks(x_pos)
    ax5.set_xticklabels(prob_sorted['Atendente'], rotation=45, ha='right')
    ax5.set_ylabel('Probabilidade (%)')
    ax5.set_title('Risco de Nota Baixa por Atendente (Verde: Baixo | Laranja: Médio | Vermelho: Alto)')
    ax5.axhline(20, color='orange', linestyle='--', alpha=0.5, linewidth=1)
    ax5.axhline(30, color='red', linestyle='--', alpha=0.5, linewidth=1)
    ax5.grid(axis='y', alpha=0.3)
    
    # Adicionar valores nas barras
    for i, (idx, row) in enumerate(prob_sorted.iterrows()):
        ax5.text(i, row['Probabilidade (%)'] + 1, f"{row['Probabilidade (%)']}%", 
                ha='center', fontsize=8)
    
    plt.suptitle('Dashboard Executivo - Análise CSAT e Recomendações', 
                fontsize=16, fontweight='bold', y=0.995)
    
    plt.savefig('grafico_9_dashboard_recomendacoes.png', dpi=300, bbox_inches='tight')
    print("📊 Gráfico salvo: grafico_9_dashboard_recomendacoes.png")
    plt.close()
    
    print("\n" * 2)


def main():
    """Função principal que executa todas as análises"""
    print("\n" * 2)
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "ANÁLISE DE SATISFAÇÃO - CSAT" + " " * 30 + "║")
    print("║" + " " * 15 + "Probabilidade, Estatística e Análise de Dados" + " " * 18 + "║")
    print("╚" + "=" * 78 + "╝")
    print("\n" * 2)
    
    # Carregar dados
    df = carregar_dados()
    
    # Executar todas as análises
    resultados_individuais = analise_1_resultados_individuais(df)
    ranking_atendentes = analise_2_ranking_atendentes(df)
    ranking_tipos_contato = analise_3_ranking_tipos_contato(df)
    melhores_tipos = analise_4_melhores_tipos_contato_por_atendente(df)
    piores_tipos = analise_5_piores_tipos_contato_por_atendente(df)
    processos_problematicos = analise_6_processos_notas_baixas(df)
    analise_7_destaque_dificuldade_por_atendente(df)
    prob_notas_baixas = analise_8_probabilidade_nota_baixa(df)
    analise_9_recomendacoes(df, prob_notas_baixas, ranking_atendentes)
    
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 25 + "ANÁLISE CONCLUÍDA COM SUCESSO" + " " * 24 + "║")
    print("╚" + "=" * 78 + "╝")
    print("\n")


if __name__ == "__main__":
    main()
