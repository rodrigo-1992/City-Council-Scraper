import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
import os
import re

class CamaraRioGrandeScraper:
    """
    Scraper for the Câmara Municipal de Rio Grande website.
    """
    
    def __init__(self):
        self.base_url = "https://www.riogrande.rs.leg.br"
        self.url_vereadores = f"{self.base_url}/processo-legislativo/parlamentares"
        self.session = requests.Session()
        self.session.headers.update({ 
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def extrair_vereadores(self):
        """
        Extrai todos os vereadores da Tabela
        """
        print(f"Acessando: {self.url_vereadores}")

        try:
            response = self.session.get(self.url_vereadores, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            
            #Encontrar a tabela de vereadores
            tabela = soup.find('table', class_='listing')
            
            if not tabela:
                print("Tabela de vereadores não encontrada.")
                return
            
            #Encontrar todas as linhas da tabela
            linhas = tabela.find_all('tr')[1:]  # Ignorar o cabeçalho

            vereadores = []

            for linha in linhas:
               vereador = self._extrair_dados_linhas(linha)
               if vereador:
                   vereadores.append(vereador)

            print(f"Total de vereadores extraídos: {len(vereadores)}")
            return vereadores
        
        except Exception as e:
            print(f"Erro ao extrair vereadores: {e}")
            return []
    
    def _extrair_dados_linhas(self, linha):
        """
        Extrai dados de uma linha da tabela de vereadores.
        """
        colunas = linha.find_all('td')
            
        if len(colunas) < 4:
            return None
            
        nome_coluna = colunas[0]
        link_vereador = nome_coluna.find('a')

        nome = link_vereador.get_text().strip() if link_vereador else ''
        url = link_vereador['href'] if link_vereador and link_vereador.has_attr('href') else ''

        #Garantir URL completa
        if url and not url.startswith('http'):
            url = self.base_url + url

        #Coluna 1 - Autor
        autor_coluna = colunas[1]
        link_autor = autor_coluna.find('a')
        autor = link_autor.get_text().strip() if link_autor else ''

        #Coluna 2 - Tipo (Sempre "Parlamentar")
        tipo = colunas[2].get_text().strip()

        #Coluna 3 - Data de Modificação
        data_modificacao = colunas[3].get_text().strip()

        #Extrair título/nome limpo
        titulo_limpo = self._limpar_nome(nome)

        return {
            'nome_completo': nome,
            'nome_limpo': titulo_limpo,
            'url_perfil': url,
            'autor_publicacao': autor,
            'tipo': tipo,
            'data_modificacao': data_modificacao,
            'timestamp': datetime.now().isoformat()
        }
    
    def _limpar_nome(self, nome):
        """
        Remove Títulos (Vereador, Vereadora) do nome dos parlamentares para padronização
        """
        nome_limpo = re.sub(r'^(Vereador|Vereadora)\s+', '', nome, flags=re.IGNORECASE)
        return nome_limpo.strip()

    def salvar_json(self, dados, nome_arquivo=None):
        """
        Salva os dados em um arquivo JSON.
        """

        if nome_arquivo is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"vereadores_{timestamp}.json"

        #Garente que a pasta existe
        os.makedirs('data/raw', exist_ok=True)

        caminho = os.path.join('data/raw', nome_arquivo)
        
        with open(caminho, 'w', encoding='utf-8') as f:
           json.dump(dados, f, ensure_ascii=False, indent=2)

        print(f"Dados salvos em: {caminho}")
        return caminho
    
    def salvar_csv(self, dados, nome_arquivo=None):
        """
        Salva os dados em um arquivo CSV.
        """
        try:
            import pandas as pd
            import numpy as np
        
            if nome_arquivo is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                nome_arquivo = f'vereadores_{timestamp}.csv'

            #Verifica se dados é uma lista
            if isinstance(dados, list):
                    #Converter para DataFrame
                    df = pd.DataFrame(dados)
            elif isinstance(dados, dict) and 'dados' in dados:
                #Se for um dicionário com chave 'dados', tenta converter essa parte
                df =  pd.DataFrame(dados['dados'])
            else:
                print("Formato de dados não reconhecido para conversão em CSV.")
                return None

            #Garente que a pasta existe
            os.makedirs('data/processed', exist_ok=True)

            caminho = os.path.join('data/processed', nome_arquivo)

            #Salvar CSV
            df.to_csv(caminho, index=False, encoding='utf-8-sig')

            print(f"Dados salvos em: {caminho}")
            return caminho
        
        except ImportError:
            print("Pandas não está instalado. Instale com 'pip install pandas' para salvar em CSV.")
            return None

# Visualizar dados no terminal
def visualizar_vereadores(vereadores):
    """
    Exibe os vereadores em formato de tabela no terminal.
    """
    if not vereadores:
        print("Nenhum vereador encontrado para exibir.")
        return
    
    print("\n" + "="*80)
    print(f"{'Nº':<3} {'Nome':<40} {'URL':<30}")
    print("="*80)

    for i, v in enumerate(vereadores,1):
        # Mostrar apenas os primeiros 40 caracteres do nome
        nome_curto = v['nome_completo'][:40]
        url_curta = v['url_perfil'][:30] if v['url_perfil'] else 'Sem URL'
        print(f"{i:<3} {nome_curto:<40} {url_curta:<30}")
    print("="*80)

              
    # Executar se for o script principal
if __name__ == "__main__":
    
    scraper = CamaraRioGrandeScraper()
    
    print("=" * 60)
    print("Scraper Câmara de Vereadores de Rio Grande/RS")
    print("=" * 60)

    #Extrair vereadores
    vereadores = scraper.extrair_vereadores()

    if vereadores:
        #Mostrar Visualização
        visualizar_vereadores(vereadores)
        
        #Salvar JSON
        arquivo_json = scraper.salvar_json(vereadores)

        #Salvar CSV
        arquivo_csv = scraper.salvar_csv(vereadores)
        
        print(f"\n Dados de {len(vereadores)} vereadores coletados com sucesso!")
        print(f"JSON: {arquivo_json}")
        if arquivo_csv:
            print(f"CSV: {arquivo_csv}")
        else:
            print("\n Falha na coleta de dados.")