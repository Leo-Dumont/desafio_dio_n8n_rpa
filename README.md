# desafio_dio_n8n_rpa
Assistente investimentos
dio-lab-assistente-investimentos-rpa-n8n/
├── README.md                           # Documentação completa com arquitetura e passo a passo
├── src/
│   ├── extrair_clientes.py            # Script Python executável standalone
│   └── extrair_clientes.ipynb         # Jupyter Notebook (com TODO resolvido para o Colab)
├── rpa/
│   ├── extrair_clientes.py            # Script Python compatível com a raiz original da DIO
│   └── extrair_clientes.ipynb         # Notebook original com envio ao Webhook implementado
├── n8n/
│   ├── workflow.json                  # 🎯 Entregável principal: fluxo mestre com roteamento (MVP / IA)
│   ├── workflow_mvp.json              # Versão MVP pura (100% autônoma, sem necessidade de API externa)
│   └── workflow_ia.json               # Versão com Agente de IA LangChain + Google Gemini
└── docs/
    ├── index.html                     # Página web dos clientes para simulação do RPA
    └── data.csv                       # Catálogo de opções de investimento por perfil
