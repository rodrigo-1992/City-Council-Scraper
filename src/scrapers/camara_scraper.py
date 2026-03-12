import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
import os

class CamaraRioGrandeScraper:
    """Scraper for the Câmara Municipal de Rio Grande website."""
    
    def __init__(self):
        self.base_url = "https://www.camarariogrande.rs.gov.br"
        self.session = requests.Session()
        self.session.headers.update({ 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.dados = {
            'vereadores': [],
            'metadata': {
                'ultima_atualizacao': datetime.now().isoformat(),
                'fonte': self.base_url
            }
        }

    def explorar_site(self):
        """Explora o site para coletar dados dos vereadores."""
        print ("Explorando o site da Câmara Municipal de Rio Grande...")

        paginas = [
            '/vereadores',
            '/transparencia',
            '/legislativo/proposicoes',
            '/sessoes',
            '/vereadores/atual'
        ]

        resultados = []
        for pagina in paginas:
            url = self.base_url + pagina
            try:
                print(f"Verificando: {pagina}")
                response = self.session.get(url, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                info = {
                    'url': url,
                    'status_code': response.status_code,
                    'titulo': soup.title.string if soup.title else 'Sem título',
                    'tem_tabelas': len(soup.find_all('table')) > 0,
                    'quantidade_links': len(soup.find_all('a')),
                    'vereadores_encontrados': self._contar_vereadores(soup)
                }
                resultados.append(info)

            except Exception as e:
                print (f"Erro ao acessar {pagina}: {e}")
            time.sleep(1)  # Respeitar o tempo entre requisições

        self.dados['mapeamento'] = resultados
        return resultados

    def _contar_vereadores(self, soup):
        """Contar o número de vereadores encontrados na página."""
        # Este método pode ser aprimorado para identificar vereadores de forma mais precisa
        texto = soup.get_text().lower()
        palavras_chave = ['vereador', 'vereadores', 'vereadora', 'vereadoras']
        
        total = 0
        for palavra in palavras:
            total += texto.count(palavra)
        
        #Procura em link
        links = soup.find_all('a', href=True)
        for link in links:
            href = link['href'].lower()
            if 'vereador' in link.text.lower() or 'vereador' in link['href'].lower():
                total += 1