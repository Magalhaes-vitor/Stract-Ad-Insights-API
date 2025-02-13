from flask import Flask, Response
import requests
import csv
from io import StringIO
import logging

app = Flask(__name__)

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Token de autorização
API_TOKEN = "ProcessoSeletivoStract2025"
API_URL = "https://sidebar.stract.to/api"

# Headers para as requisições
headers = {
    'Authorization': f'Bearer {API_TOKEN}',
}

def fetch_all_pages(endpoint, params=None):
    """Função para buscar todas as páginas de um endpoint paginado."""
    results = []
    page = 1
    while True:
        if params is None:
            params = {}
        params['page'] = page
        url = f"{API_URL}/{endpoint}"
        logger.info(f"Fazendo requisição para: {url} com parâmetros: {params}")
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            logger.error(f"Erro na requisição: {response.status_code} - {response.text}")
            break
        data = response.json()
        logger.info(f"Resposta recebida: {data}")
        if 'data' in data:
            results.extend(data['data'])
        elif 'platforms' in data:
            results.extend(data['platforms'])  # Para o endpoint /platforms
        elif 'accounts' in data:
            results.extend(data['accounts'])  # Para o endpoint /accounts
        elif 'fields' in data:
            results.extend(data['fields'])  # Para o endpoint /fields
        elif 'insights' in data:
            results.extend(data['insights'])  # Para o endpoint /insights
        else:
            logger.error(f"Resposta inesperada: {data}")
            break
        if page >= data.get('pagination', {}).get('total', 1):
            break
        page += 1
    return results

@app.route('/')
def index():
    """Endpoint raiz que retorna informações pessoais."""
    return {
        "name": "Vitor De Toledo Magalhaes",
        "email": "vitor.de.toledo.magalhaes@gmail.com",
        "linkedin": "https://www.linkedin.com/in/magalhaes-vitor/"
    }

@app.route('/<platform>')
def platform_ads(platform):
    """Endpoint que retorna todos os anúncios de uma plataforma específica."""
    logger.info(f"Coletando dados para a plataforma: {platform}")
    accounts = fetch_all_pages(f"accounts?platform={platform}")
    fields = fetch_all_pages(f"fields?platform={platform}")
    field_values = [field['value'] for field in fields]
    insights = []
    for account in accounts:
        account_insights = fetch_all_pages(f"insights?platform={platform}&account={account['id']}&token={account['token']}&fields={','.join(field_values)}")
        for insight in account_insights:
            insight['account_name'] = account['name']
            insights.append(insight)
    
    # Geração dinâmica dos cabeçalhos do CSV
    all_fields = set()
    for insight in insights:
        all_fields.update(insight.keys())
    headers = ['Platform', 'Account Name'] + list(all_fields - {'platform', 'account_name'})

    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=headers)
    writer.writeheader()
    for insight in insights:
        row = {'Platform': platform, 'Account Name': insight['account_name']}
        row.update({field: insight.get(field, '') for field in headers if field not in ['Platform', 'Account Name']})
        writer.writerow(row)
    output.seek(0)
    return Response(output, mimetype="text/csv")

@app.route('/<platform>/resumo')
def platform_summary(platform):
    """Endpoint que retorna um resumo dos anúncios de uma plataforma específica."""
    logger.info(f"Coletando resumo para a plataforma: {platform}")
    accounts = fetch_all_pages(f"accounts?platform={platform}")
    fields = fetch_all_pages(f"fields?platform={platform}")
    field_values = [field['value'] for field in fields]
    insights = []
    for account in accounts:
        account_insights = fetch_all_pages(f"insights?platform={platform}&account={account['id']}&token={account['token']}&fields={','.join(field_values)}")
        for insight in account_insights:
            insight['account_name'] = account['name']
            insights.append(insight)
    
    # Agregação por conta
    summary = {}
    for insight in insights:
        account_name = insight['account_name']
        if account_name not in summary:
            summary[account_name] = {field: 0 for field in field_values if isinstance(insight.get(field), (int, float))}
            summary[account_name]['account_name'] = account_name
        for field in field_values:
            if isinstance(insight.get(field), (int, float)):
                summary[account_name][field] += insight.get(field, 0)
    
    # Geração dinâmica dos cabeçalhos do CSV
    headers = ['Platform', 'Account Name'] + field_values

    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=headers)
    writer.writeheader()
    for account_name, data in summary.items():
        row = {'Platform': platform, 'Account Name': account_name}
        row.update({field: data.get(field, '') for field in field_values})
        writer.writerow(row)
    output.seek(0)
    return Response(output, mimetype="text/csv")

@app.route('/geral')
def general_ads():
    """Endpoint que retorna todos os anúncios de todas as plataformas."""
    logger.info("Coletando dados para todas as plataformas")
    platforms = fetch_all_pages("platforms")
    all_insights = []
    for platform in platforms:
        platform_value = platform['value']
        accounts = fetch_all_pages(f"accounts?platform={platform_value}")
        fields = fetch_all_pages(f"fields?platform={platform_value}")
        field_values = [field['value'] for field in fields]
        for account in accounts:
            account_insights = fetch_all_pages(f"insights?platform={platform_value}&account={account['id']}&token={account['token']}&fields={','.join(field_values)}")
            for insight in account_insights:
                insight['platform'] = platform['text']
                insight['account_name'] = account['name']
                all_insights.append(insight)
    
    # Geração dinâmica dos cabeçalhos do CSV
    all_fields = set()
    for insight in all_insights:
        all_fields.update(insight.keys())
    headers = ['Platform', 'Account Name'] + list(all_fields - {'platform', 'account_name'})

    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=headers)
    writer.writeheader()
    for insight in all_insights:
        row = {'Platform': insight['platform'], 'Account Name': insight['account_name']}
        row.update({field: insight.get(field, '') for field in headers if field not in ['Platform', 'Account Name']})
        writer.writerow(row)
    output.seek(0)
    return Response(output, mimetype="text/csv")

@app.route('/geral/resumo')
def general_summary():
    """Endpoint que retorna um resumo de todos os anúncios de todas as plataformas."""
    logger.info("Coletando resumo para todas as plataformas")
    platforms = fetch_all_pages("platforms")
    all_insights = []
    field_values = set()  # Usamos um conjunto para armazenar todos os campos únicos

    for platform in platforms:
        platform_value = platform['value']
        accounts = fetch_all_pages(f"accounts?platform={platform_value}")
        fields = fetch_all_pages(f"fields?platform={platform_value}")
        platform_field_values = [field['value'] for field in fields]
        field_values.update(platform_field_values)  # Adiciona os campos da plataforma ao conjunto

        for account in accounts:
            account_insights = fetch_all_pages(f"insights?platform={platform_value}&account={account['id']}&token={account['token']}&fields={','.join(platform_field_values)}")
            for insight in account_insights:
                insight['platform'] = platform['text']
                insight['account_name'] = account['name']
                all_insights.append(insight)
    
    # Agregação por plataforma
    summary = {}
    for insight in all_insights:
        platform_name = insight['platform']
        if platform_name not in summary:
            summary[platform_name] = {field: 0 for field in field_values if isinstance(insight.get(field), (int, float))}
            summary[platform_name]['platform'] = platform_name
        for field in field_values:
            if isinstance(insight.get(field), (int, float)):
                summary[platform_name][field] += insight.get(field, 0)
    
    # Geração dinâmica dos cabeçalhos do CSV
    headers = ['Platform'] + list(field_values)

    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=headers)
    writer.writeheader()
    for platform_name, data in summary.items():
        row = {'Platform': platform_name}
        row.update({field: data.get(field, '') for field in field_values})
        writer.writerow(row)
    output.seek(0)
    return Response(output, mimetype="text/csv")

if __name__ == '__main__':
    app.run(debug=True)
