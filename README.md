# Teste Técnico utilizando FastAPI

API desenvolvida como teste técnico com o objetivo de realizar o gerenciamento de **clientes**, **produtos** e **pedidos**, incluindo autenticação com JWT e documentação automática via Swagger.

---

## 🚀 Funcionalidades

- ✅ CRUD de Clientes
- ✅ CRUD de Produtos
- ✅ CRUD de Pedidos
- ✅ Filtros de busca (ex.: por nome, email, categoria, seção, valores, disponibilidade)
- ✅ Autenticação com JWT
- ✅ Testes de integração com `pytest` para as rotas de clientes e produtos
- ✅ Documentação automática da API no Swagger (`/docs`)

---

## 🧰 Tecnologias utilizadas

- **Python 3.10**
- **FastAPI**
- **SQLAlchemy**
- **PostgreSQL**
- **Docker + Docker Compose**
- **PgAdmin4**
- **Pytest**

---

## 🔥 Como rodar o projeto localmente

### ✔️ Pré-requisitos

- Python 3.10+
- Docker e Docker Compose
- Git

---

## ⚙️ Rodando com Docker (Recomendado)

1. Clone o repositório:

```bash
git clone https://github.com/crramires/fastapi_teste_de_codificacao.git
cd seu-repositorio
```

2. Suba os containers:
```bash
docker-compose up --build
```

3. Acesso a API:
```bash
http://localhost:8000/docs
```

4. Acesso a interface do banco de dados via pgAdmin4:
```bash
http://localhost/8080
```
Ao acessar pela primeira vez use as credenciais definidas no docker-compose.yml.
Configure um novo servidor apontando para:
Host:db
Porta:5432
Usário e senha: Conforme definido no docker-compose.yml


🏗️ Rodando localmente (sem Docker)

Clone o repositório:
git clone https://github.com/seu-usuario/seu-repositorio.git

cd seu-repositorio

Crie e ative um ambiente virtual:

python -m venv venv

source venv/bin/activate  # Mac/Linux

venv\Scripts\activate     # Windows

Instale as dependências:

pip install -r requirements.txt

Configure o banco PostgreSQL localmente (ou use SQLite para testes rápidos).

Execute as migrações (se houver) e rode o projeto:

uvicorn main:app --reload

📑 Documentação da API

Acesse via navegador:

http://localhost:8000/docs


✅ Como rodar os testes

Execute os testes de integração utilizando pytest:

pytest

Caso queira rodar os testes com verbose para mais detalhes:

pytest -v
