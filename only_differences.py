import pandas as pd

# Carregar os CSVs com ponto e vírgula como delimitador
csv1 = pd.read_csv('old.csv', delimiter=';')
csv2 = pd.read_csv('new.csv', delimiter=';')

# Remover colunas 'Unnamed'
csv1 = csv1.loc[:, ~csv1.columns.str.contains('^Unnamed')]
csv2 = csv2.loc[:, ~csv2.columns.str.contains('^Unnamed')]

# Verificar as colunas de cada DataFrame
print("Colunas do CSV novo:", csv1.columns)
print("Colunas do CSV antigo:", csv2.columns)

# Definir a chave de comparação
key_columns = ['DatabaseName', 'TABLE_SCHEMA', 'TABLE_NAME']

# Verificar se as colunas chave estão presentes em ambos os DataFrames
missing_columns_csv1 = [col for col in key_columns if col not in csv1.columns]
missing_columns_csv2 = [col for col in key_columns if col not in csv2.columns]

if missing_columns_csv1:
    print(f"Colunas ausentes no CSV novo: {missing_columns_csv1}")
if missing_columns_csv2:
    print(f"Colunas ausentes no CSV antigo: {missing_columns_csv2}")

if not missing_columns_csv1 and not missing_columns_csv2:
    # Mesclar os dois dataframes com base nas chaves de comparação
    merged_df = csv1.merge(csv2, on=key_columns, how='outer', suffixes=('_old', '_new'), indicator=True)

    # Filtrar apenas as diferenças
    differences = merged_df[merged_df['_merge'] != 'both']

    # Remove a coluna _merge
    differences = differences.drop(columns=['_merge'])

    # Salvar as diferenças em um novo CSV
    differences.to_csv('./output/differences.csv', index=False)

    print("Comparação concluída. As diferenças foram salvas em 'differences.csv'.")
else:
    print("Não foi possível comparar os CSVs devido a colunas ausentes.")