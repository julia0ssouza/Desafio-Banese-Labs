from src.data_loader import load_all_data
from src.credit_assistant import CreditAssistant


def main():
    print("Iniciando o Assistente de Análise de Crédito Inteligente Banese...")

    dados_empresas = load_all_data()

    if dados_empresas.empty:
        print("\nNão foi possível carregar os dados das empresas. Encerrando o programa.")
        return

    assistant = CreditAssistant(dados_empresas)

    print("\nAssistente pronto. Digite o nome de uma empresa para analisar.")
    print("Para sair, digite 'sair' a qualquer momento.")

    while True:
        nome_empresa = input("\nNome da Empresa: ")

        if nome_empresa.lower() == 'sair':
            print("Encerrando o assistente. Até logo!")
            break

        resultado_analise = assistant.analyze_company(nome_empresa)

        print("-" * 50)
        print(f"Análise de Crédito para: {nome_empresa}")
        print("-" * 50)
        print(resultado_analise)
        print("-" * 50)


if __name__ == "__main__":
    main()
