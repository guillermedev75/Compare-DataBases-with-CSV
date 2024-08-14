import pandas as pd

# Carregar os CSVs com ponto e vírgula como delimitador
csv1 = pd.read_csv('new.csv', delimiter=';')
csv2 = pd.read_csv('old.csv', delimiter=';')

# Remover colunas 'Unnamed'
csv1 = csv1.loc[:, ~csv1.columns.str.contains('^Unnamed')]
csv2 = csv2.loc[:, ~csv2.columns.str.contains('^Unnamed')]


# Converter colunas de RecordCount para inteiros
csv1['RecordCount'] = pd.to_numeric(csv1['RecordCount'], downcast='integer')
csv2['RecordCount'] = pd.to_numeric(csv2['RecordCount'], downcast='integer')

# Verificar as colunas de cada DataFrame
print("Colunas do CSV novo:", csv1.columns)
print("Colunas do CSV antigo:", csv2.columns)

# Definir a chave de comparação
key_columns = ['DatabaseName', 'TABLE_SCHEMA', 'TABLE_NAME']

# Mesclar os dois dataframes com base nas chaves de comparação
merged_df = csv1.merge(csv2, on=key_columns, how='outer', suffixes=('_new', '_old'), indicator=True)

# Identificar diferenças e criar um DataFrame com todas as tabelas e suas contagens de registros
all_tables_comparison = merged_df[['DatabaseName', 'TABLE_SCHEMA', 'TABLE_NAME', 'RecordCount_new', 'RecordCount_old']]

# Salvar a comparação em um novo CSV
all_tables_comparison.to_csv('./output/all_tables_comparison.csv', index=False)

print("Comparação completa. As diferenças foram salvas em 'all_tables_comparison.csv'.")
