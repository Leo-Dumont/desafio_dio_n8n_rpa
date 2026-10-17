"""
Script RPA de Extração de Clientes e Integração com Webhook N8N
Desafio Dio.me: Criando um Assistente de Investimentos com RPA e IA Generativa
"""

import sys
import json
import requests
from bs4 import BeautifulSoup

# Ajuste de encoding para terminais Windows (evita UnicodeEncodeError em cp1252)
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# URL da página de simulação de clientes (GitHub Pages da DIO)
URL_PAGINA = "https://digitalinnovationone.github.io/dio-lab-assistente-investimentos-rpa-n8n/"

# URL do Webhook do N8N (Altere para a URL do seu Webhook no N8N Cloud ou Local)
# Exemplo N8N Local: "http://localhost:5678/webhook/clientes"
# Exemplo N8N Cloud: "https://seu-usuario.app.n8n.cloud/webhook/clientes"
# Exemplo Webhook Test: "http://localhost:5678/webhook-test/clientes"
N8N_WEBHOOK = "http://localhost:5678/webhook/clientes"


def extrair_clientes(url: str):
    """
    RPA: Realiza web scraping da página HTML para coletar dados dos clientes.
    """
    print(f"[RPA] Conectando a pagina: {url}")
    response = requests.get(url, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    linhas = soup.select("#clientes tbody tr")

    clientes = []
    for linha in linhas:
        colunas = linha.find_all("td")
        if len(colunas) >= 4:
            cliente = {
                "nome": colunas[0].get_text(strip=True),
                "email": colunas[1].get_text(strip=True),
                "saldo": colunas[2].get_text(strip=True),
                "perfil": colunas[3].get_text(strip=True),
            }
            clientes.append(cliente)

    return clientes


def enviar_para_n8n(webhook_url: str, clientes: list):
    """
    Orquestração: Envia os dados dos clientes via HTTP POST para o Webhook do N8N.
    """
    print(f"\n[N8N] Enviando {len(clientes)} clientes para o Webhook: {webhook_url}")
    payload = {"clientes": clientes}

    try:
        response = requests.post(webhook_url, json=payload, timeout=30)
        print(f"[N8N] Status Code recebido: {response.status_code}")

        if response.status_code == 200:
            print("[N8N] [SUCESSO] O N8N processou o fluxo e retornou as recomendacoes:\n")
            try:
                dados_retorno = response.json()
                print(json.dumps(dados_retorno, indent=2, ensure_ascii=False))
            except Exception:
                print(response.text)
        else:
            print(f"[N8N] [AVISO] O Webhook respondeu com status {response.status_code}")
            print(response.text)

    except requests.exceptions.ConnectionError:
        print("\n[ERRO DE CONEXAO] Nao foi possivel conectar ao Webhook do N8N.")
        print("Dicas para solucionar:")
        print("1. Verifique se o N8N esta em execucao (n8n start ou Cloud ativo).")
        print("2. Certifique-se de que o no Webhook esta ativo ou ouvindo em modo de teste.")
        print(f"3. Atualize a variavel N8N_WEBHOOK no script com a sua URL valida (atual: '{webhook_url}').")


def main():
    webhook_url = sys.argv[1] if len(sys.argv) > 1 else N8N_WEBHOOK

    print("=" * 65)
    print("ASSISTENTE DE INVESTIMENTOS RPA + N8N (DIO.ME)")
    print("=" * 65)

    try:
        clientes = extrair_clientes(URL_PAGINA)
        print(f"[RPA] [OK] {len(clientes)} clientes extraidos com sucesso:")
        for idx, c in enumerate(clientes, start=1):
            print(f"  {idx:02d}. {c['nome']:<18} | Perfil: {c['perfil']:<11} | Saldo: {c['saldo']}")

        enviar_para_n8n(webhook_url, clientes)

    except Exception as e:
        print(f"[ERRO] Ocorreu uma falha no processo de RPA: {e}")


if __name__ == "__main__":
    main()
