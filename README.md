# EduFuture  

O **EduFuture** é um sistema de cursos online desenvolvido com **Django** e **Django Rest Framework**. O principal objetivo deste projeto foi colocar em prática tudo o que aprendi em cursos complementares, como a criação de **API Rest** utilizando **Django Rest Framework** e a implementação de autenticação JWT com **Django Simple JWT**.  

## 🚀 Tecnologias utilizadas  

- **Linguagem:** Python  
- **Framework:** Django  
- **API:** Django Rest Framework  
- **Autenticação:** Django Simple JWT  
- **Banco de Dados:** PostgreSQL (via psycopg2)  

## 📂 Estrutura do projeto  

O repositório contém os seguintes diretórios e arquivos principais:  

📁 `base_static/` – Arquivos estáticos do projeto  
📁 `base_template/` – Templates base do sistema  
📁 `courses/` – Módulo relacionado a cursos e disciplinas  
📁 `edufuture/` – Configuração principal do Django  
📁 `utils/` – Utilitários e funções auxiliares  
📄 `.gitignore` – Arquivos ignorados no versionamento  
📄 `README.md` – Documentação do projeto  
📄 `manage.py` – Comando de gerenciamento do Django  

## 🎯 Objetivo do projeto  

O **EduFuture** foi criado com o intuito de aplicar conceitos essenciais do desenvolvimento backend, como:  

✅ Criação e gerenciamento de APIs RESTful  
✅ Autenticação segura com JWT  
✅ Estruturação de um projeto Django  
✅ Boas práticas de desenvolvimento  

## 🛠️ Como rodar o projeto  

1. **Clone o repositório:**  
    ```bash
    git clone https://github.com/Tomazbr9/EduFuture.git

2. **Acesse o diretório do projeto:**
    ```bash
    cd EduFuture
3. **Crie e ative um ambiente virtual:**
    ``` bash
    python -m venv venv
    source venv/bin/activate  # No Windows, use: venv\Scripts\activate

4. **Instale as dependências:**
    ```bash
    pip install -r requirements.txt

5. **Configuração do Banco de Dados**  

    Por padrão, o projeto usa **SQLite**, que já vem integrado ao Django e não requer instalação adicional.  

    Caso queira usar **PostgreSQL**, defina as variáveis de ambiente corretamente.  

    ### 🔧 Como usar o PostgreSQL  

    1. Instale o **PostgreSQL** na sua máquina (se ainda não tiver).  
    2. Crie um banco de dados chamado `edufuture_db` (ou qualquer outro nome de sua escolha).  
    3. Configure as variáveis de ambiente:  

6. **Execute as migrações do banco de dados:**
   ```bash
    python manage.py migrate
7. **Inicie o servidor:**
   ```bash
    python manage.py runserver

8. **Acesse a API no navegador:**
   ```cpp
    http://127.0.0.1:8000/