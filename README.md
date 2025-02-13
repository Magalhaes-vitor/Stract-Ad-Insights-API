# API de Insights de Anúncios do Stract

Este repositório contém a implementação de um servidor local em Python (Flask) para consumir dados de uma API de publicidade do cliente Stract imaginária. O servidor fornece relatórios em tempo real no formato CSV, extraindo dados de plataformas de anúncios, contas e insights de campanha. Por meio de endpoints específicos, o sistema organiza os dados de forma tabular e agregada, permitindo o acesso a relatórios detalhados ou resumidos para cada plataforma de publicidade. O código foi desenvolvido com foco na simplicidade e eficiência, usando dependências mínimas.

---

## Funcionalidades

- **Coleta de dados de anúncios**: Extrai dados de plataformas de publicidade, contas e insights de campanha.
- **Relatórios em CSV**: Gera relatórios detalhados e resumidos em formato CSV.
- **Endpoints flexíveis**: Permite acessar dados específicos de uma plataforma ou de todas as plataformas.
- **Agregação de dados**: Fornece resumos agregados por plataforma ou conta.

---

## Requisitos

- Python 3.8 ou superior
- Flask
- Requests

---

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/nome-do-repositorio.git
   cd nome-do-repositorio
   ```

2. Crie um ambiente virtual e ative-o:

   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows use `venv\Scripts\activate`
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

---

## Configuração

Antes de executar a API, certifique-se de que o token de autorização está configurado corretamente no script:

```python
API_TOKEN = "ProcessoSeletivoStract2025"
```

---

## Executando a API

Para iniciar a API, execute o seguinte comando:

```bash
python app.py
```

A API estará disponível em `http://127.0.0.1:5000/`.

---

## Endpoints

### `GET /`

Retorna informações pessoais do desenvolvedor.

**Exemplo de Resposta:**

```json
{
  "name": "Vitor De Toledo Magalhaes",
  "email": "vitor.de.toledo.magalhaes@gmail.com",
  "linkedin": "https://www.linkedin.com/in/magalhaes-vitor/"
}
```

---

### `GET /<platform>`

Retorna todos os anúncios de uma plataforma específica em formato CSV.

**Parâmetros:**

- `platform`: Nome da plataforma (ex: `meta_ads`, `ga4`).

**Exemplo de Uso:**

```bash
curl -o ads.csv http://127.0.0.1:5000/ga4
```

---

### `GET /<platform>/resumo`

Retorna um resumo dos anúncios de uma plataforma específica em formato CSV.

**Parâmetros:**

- `platform`: Nome da plataforma (ex: `meta_ads`, `ga4`).

**Exemplo de Uso:**

```bash
curl -o summary.csv http://127.0.0.1:5000/meta_ads/resumo
```

---

### `GET /geral`

Retorna todos os anúncios de todas as plataformas em formato CSV.

**Exemplo de Uso:**

```bash
curl -o all_ads.csv http://127.0.0.1:5000/geral
```

---

### `GET /geral/resumo`

Retorna um resumo de todos os anúncios de todas as plataformas em formato CSV.

**Exemplo de Uso:**

```bash
curl -o all_summary.csv http://127.0.0.1:5000/geral/resumo
```

---

## Logs

A API utiliza o módulo `logging` para registrar informações e erros. Os logs são exibidos no console onde a API está sendo executada.

---

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

---

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

--- 

## Contato

- **Nome**: Vitor De Toledo Magalhaes  
- **Email**: vitor.de.toledo.magalhaes@gmail.com  
- **LinkedIn**: [https://www.linkedin.com/in/magalhaes-vitor/](https://www.linkedin.com/in/magalhaes-vitor/)  

--- 

Este projeto foi desenvolvido com o objetivo de demonstrar habilidades técnicas e boas práticas de programação. Sinta-se à vontade para explorar, utilizar e contribuir! 🚀
