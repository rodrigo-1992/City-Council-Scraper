# Câmara de Rio Grande - RS - Análise de Dados dos Vereadores

Sobre o Projeto
Este projeto realiza web scraping, processamento e visualização de dados públicos da Câmara Municipal de Rio Grande - RS, 
criando um dashboard interativo para análise da atuação dos vereadores.

Objetivos
- Coletar dados de presenças, projetos e gastos dos vereadores
- Criar um pipeline de ETL (Extract, Transform, Load)
- Desenvolver um dashboard interativo com Streamlit
- Disponibilizar dados abertos para a comunidade

Tecnologias Utilizadas
- Python 3.x
- BeautifulSoup4 / Selenium (scraping)
- Pandas (análise de dados)
- Streamlit (dashboard)
- Plotly (visualizações)
- Git/GitHub (versionamento)

Estrutura do Projeto
src/
├── scrapers/ # Código para coleta de dados
├── data_pipeline/ # Processamento e limpeza
└── dashboard/ # Aplicação Streamlit
data/
├── raw/ # Dados brutos (não versionados)
└── processed/ # Dados processados
notebooks/ # Análises exploratórias


Como Executar
1. Clone o repositório
2. Crie ambiente virtual: `python -m venv venv`
3. Ative: `venv\Scripts\activate` (Windows)
4. Instale dependências: `pip install -r requirements.txt`
5. Execute o scraper: `python src/scrapers/camara_scraper.py`
6. Inicie o dashboard: `streamlit run src/dashboard/app.py`

Funcionalidades Planejadas
- [ ] Ranking de presenças em sessões
- [ ] Análise de produção legislativa
- [ ] Visualização de gastos por vereador
- [ ] Comparativo entre partidos
- [ ] Série histórica de projetos

Licença
Livre para Uso

Contribuição
Contribuições são bem-vindas! 
Abra uma issue ou envie um pull request.
