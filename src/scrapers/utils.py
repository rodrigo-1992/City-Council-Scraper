import pandas as pd
import json
import os
from datetime import datetime

def carregar_dados_json(caminho_arquivo):
    
    """Carrega dados de um arquivo JSON."""   
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def json_para_dataframe(caminho_json):
    """Converte JSON para DataFrame do Pandas."""
    dados = carregar_dados_json(caminho_json)

    # Se tiver lista de vereadores, converte
    if 'vereadores' in dados and dados['vereadores']:
        return pd.DataFrame(dados['vereadores'])
    
    # Se tiver mapeamento, converte
    if 'mapeamento' in dados:
        return pd.DataFrame(dados['mapeamento'])
    
    return pd.DataFrame()

def listar_arquivos_coletados():
    """Lista os arquivos JSON coletados na pasta data/raw."""
    caminho_pasta = 'data/raw'
    if not os.path.exists(caminho_pasta):
        return []
    
    arquivos = [f for f in os.listdir(caminho_pasta) if f.endswith('.json')]
    return sorted(arquivos, reverse=True)  # Ordena do mais recente para o mais antigo

def limpar_text():
    """Limpa e padroniza o texto para facilitar a análise."""
    if not texto:
        return ""
    return ' '.join(texto.lower().split())