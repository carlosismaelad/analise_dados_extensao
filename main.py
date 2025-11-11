import pandas as pd

# Carregar a planilha
df = pd.read_excel('analise_suporte.xlsx')

# Exibir as primeiras linhas para verificar os dados
print("=" * 80)
print("PRIMEIRAS LINHAS DA PLANILHA")
print("=" * 80)
print(df.head())
print("\n")

# Informações básicas sobre o dataset
print("=" * 80)
print("INFORMAÇÕES DO DATASET")
print("=" * 80)
print(f"Total de registros: {len(df)}")
print(f"Colunas: {list(df.columns)}")
print("\n")

# Calcular a média de CSAT por atendente
print("=" * 80)
print("MÉDIA DE CSAT POR ATENDENTE")
print("=" * 80)

# Agrupar por atendente e calcular a média
media_por_atendente = df.groupby('attendant').agg({
    'csat': ['mean', 'count', 'sum']
}).round(2)

# Renomear as colunas para melhor visualização
media_por_atendente.columns = ['Média CSAT', 'Total de Avaliações', 'Soma CSAT']

# Ordenar pela média (decrescente)
media_por_atendente = media_por_atendente.sort_values('Média CSAT', ascending=False)

print(media_por_atendente)
print("\n")

# Estatísticas gerais
print("=" * 80)
print("ESTATÍSTICAS GERAIS")
print("=" * 80)
print(f"Média geral de CSAT: {df['csat'].mean():.2f}")
print(f"Mediana de CSAT: {df['csat'].median():.2f}")
print(f"Desvio padrão: {df['csat'].std():.2f}")
print(f"Nota mínima: {df['csat'].min():.2f}")
print(f"Nota máxima: {df['csat'].max():.2f}")
print("\n")

# Análise por tipo de contato
print("=" * 80)
print("MÉDIA DE CSAT POR TIPO DE CONTATO")
print("=" * 80)
media_por_tipo = df.groupby('contact type').agg({
    'csat': ['mean', 'count']
}).round(2)
media_por_tipo.columns = ['Média CSAT', 'Total de Avaliações']
print(media_por_tipo)
print("\n")

# Análise por opportunity
print("=" * 80)
print("MÉDIA DE CSAT POR TIPO DE OPPORTUNITY")
print("=" * 80)
media_por_opportunity = df.groupby('opportunity').agg({
    'csat': ['mean', 'count']
}).round(2)
media_por_opportunity.columns = ['Média CSAT', 'Total de Avaliações']
print(media_por_opportunity)
print("\n")
