import pandas as pd
import os


def load_all_data(data_path="dados"):

    all_dfs = []

    print(f"Lendo arquivos do diretório: {data_path}")

    for filename in os.listdir(data_path):
        file_path = os.path.join(data_path, filename)
        file_ext = os.path.splitext(filename)[1]

        try:
            print(f"Lendo arquivo: {filename}...")
            if file_ext == '.csv':
                df = pd.read_csv(file_path)
            elif file_ext == '.json':
                df = pd.read_json(file_path, lines=True)
            elif file_ext == '.parquet':
                df = pd.read_parquet(file_path)
            elif file_ext == '.xml':
                df = pd.read_xml(file_path)
            else:
                continue

            all_dfs.append(df)
            print(f" -> Sucesso!")
        except Exception as e:
            print(f" -> Falha ao ler {filename}: {e}")

    if not all_dfs:
        print("Nenhum dado foi carregado. Verifique o diretório e os arquivos.")
        return pd.DataFrame()

    consolidated_df = pd.concat(all_dfs, ignore_index=True)

    column_mapping = {
        'Receita_Anual': 'Receita Anual',
        'Dívida_Total': 'Dívida Total',
        'Prazo_de_Pagamento_dias': 'Prazo de Pagamento (dias)',
        'Notícias_Recentes': 'Notícias Recentes',
        'Prazo Pagamento (dias)': 'Prazo de Pagamento (dias)'
    }
    consolidated_df.rename(columns=column_mapping, inplace=True)

    consolidated_df = consolidated_df.groupby(
        consolidated_df.columns, axis=1).first()

    final_df = consolidated_df.groupby('Empresa').first().reset_index()

    expected_columns = [
        'Empresa', 'Receita Anual', 'Dívida Total',
        'Prazo de Pagamento (dias)', 'Setor', 'Rating', 'Notícias Recentes'
    ]
    for col in expected_columns:
        if col not in final_df.columns:
            final_df[col] = None

    return final_df[expected_columns]


if __name__ == '__main__':
    dados_consolidados = load_all_data(data_path='dados')

    if not dados_consolidados.empty:
        print("\nVisualização dos 5 primeiros registros consolidados e limpos:")
        print(dados_consolidados.head())
        print(
            f"\nTotal de {len(dados_consolidados)} empresas únicas carregadas.")
        print("\nInformações do DataFrame final:")
        dados_consolidados.info()
