import os
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class CreditAssistant:
    def __init__(self, consolidated_data: pd.DataFrame):
        """
        Inicializa o assistente com os dados consolidados das empresas
        """
        self.data = consolidated_data
        self.data.set_index('Empresa', inplace=True)

        try:
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError(
                    "Chave de API do Google não encontrada. Verifique seu arquivo .env")
            genai.configure(api_key=api_key)

            self.model = genai.GenerativeModel(
                'models/gemini-1.5-flash-latest')
            print("Assistente de Crédito inicializado com sucesso.")
        except Exception as e:
            print(f"Erro ao inicializar o modelo de IA: {e}")
            self.model = None

    def analyze_company(self, company_name: str):
        """
        Analisa uma empresa específica e gera uma recomendação de crédito
        """
        if self.model is None:
            return "O modelo de IA não foi inicializado. Verifique a configuração da API."

        try:
            company_info = self.data.loc[company_name]
        except KeyError:
            return f"Empresa '{company_name}' não encontrada na base de dados."

        prompt = f"""
        Você é um experiente analista de crédito do Banese. Sua tarefa é realizar uma análise preliminar de crédito para a PME a seguir, com base nos dados fornecidos.

        **Dados da Empresa:**
        - **Nome:** {company_name}
        - **Setor de Atuação:** {company_info['Setor']}
        - **Receita Anual:** R$ {company_info['Receita Anual']:,.2f}
        - **Dívida Total:** R$ {company_info['Dívida Total']:,.2f}
        - **Prazo Médio de Pagamento (dias):** {company_info['Prazo de Pagamento (dias)']}
        - **Rating de Crédito Atual:** {company_info['Rating']}
        - **Notícias Recentes Relevantes:** "{company_info['Notícias Recentes']}"

        **Sua Análise Deve Conter:**

        1.  **Recomendação Preliminar:** (Aprovar, Recusar ou Análise Adicional Necessária). Seja direto.
        2.  **Justificativa da Recomendação:** Um parágrafo curto e objetivo explicando os motivos da sua decisão, conectando os dados fornecidos.
        3.  **Principais Riscos Identificados:** Liste em tópicos (bullet points) 2 ou 3 riscos potenciais (ex: alta dívida em relação à receita, notícias negativas, setor em retração, etc.).
        4.  **Principais Oportunidades/Pontos Fortes:** Liste em tópicos (bullet points) 2 ou 3 pontos positivos (ex: receita crescente, notícias de expansão, bom rating, etc.).

        Seja claro, profissional e baseie sua análise estritamente nos dados apresentados.
        """

        try:
            print(f"\nGerando análise para {company_name}...")
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Ocorreu um erro ao gerar a análise: {e}"
