# Desafio Banese Labs - Assistente de Análise de Crédito

Este projeto implementa um Assistente de Análise de Crédito Inteligente usando IA Generativa para otimizar o processo de concessão de empréstimos a PMEs.

## Arquitetura da Solução

O diagrama abaixo ilustra a arquitetura e o fluxo de dados da aplicação:

```mermaid
graph TD;
    A["Fontes de Dados<br>(CSV, JSON, XML, Parquet)"] --> B["Módulo de Carga e Unificação<br>(data_loader.py)"];
    B --> C["Aplicação Principal<br>(main.py)"];
    C --> D["Assistente de Crédito<br>(credit_assistant.py)"];
    D --> E((API Google Gemini));

    style A fill:#f9f,stroke:#333,stroke-width:2px,color:#000
    style B fill:#ccf,stroke:#333,stroke-width:2px,color:#000
    style C fill:#ccf,stroke:#333,stroke-width:2px,color:#000
    style D fill:#ccf,stroke:#333,stroke-width:2px,color:#000
    style E fill:#cff,stroke:#333,stroke-width:2px,color:#000
```
