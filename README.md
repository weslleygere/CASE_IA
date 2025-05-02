# 🔥 Sistema de Predições de Eficiência Energética

Este projeto foi desenvolvido com o objetivo de oferecer uma solução completa para predição de eficiência energética de edifícios, permitindo a estimativa das cargas de aquecimento e resfriamento a partir de características estruturais e de design. Todo o processo envolveu etapas bem definidas, desde a análise exploratória dos dados até a disponibilização de uma aplicação web interativa e responsiva.

Para esta *Proof of Concept* (PoC), propomos a criação de um sistema de regressão supervisionada utilizando o conjunto de dados público **UCI Energy Efficiency Dataset**, disponível em: [UCI Energy Dataset](https://archive.ics.uci.edu/ml/datasets/energy+efficiency).

## 🔎 Sobre o conjunto de dados

O *UCI Energy Efficiency Dataset* foi desenvolvido para avaliar as necessidades de carga térmica (aquecimento e resfriamento) de edifícios como uma função de seus parâmetros estruturais. Os dados foram gerados a partir de análises energéticas realizadas em 12 formatos diferentes de edifícios simulados no software **Ecotect**. As simulações variaram áreas de envidraçamento, distribuição do envidraçamento e orientação, entre outras características. 

O conjunto de dados contém:

- **768 amostras** simulando diferentes configurações de edifícios.
- **8 variáveis preditoras**:
    - Relative Compactness
    - Surface Area
    - Wall Area
    - Roof Area
    - Overall Height
    - Orientation
    - Glazing Area
    - Glazing Area Distribution
- **2 variáveis resposta contínuas**:
    - Carga de Aquecimento (*Heating Load*)
    - Carga de Resfriamento (*Cooling Load*)

As tarefas associadas incluem regressão e, opcionalmente, classificação se as respostas forem arredondadas.

## 📝 Etapas do projeto

1. **Análise exploratória**:
    - Análise estatística das variáveis.
    - Visualização das distribuições e correlações.

2. **Pré-processamento**:
    - Padronização das variáveis.
    - Seleção de features.

3. **Treinamento de modelos**:
    - Avaliação de algoritmos de regressão diversos.
    - Seleção baseada em métricas de erro e validação cruzada.
    - Armazenamento do modelo final (`model.pkl`) e dos pré-processadores (`scaler_baseline.pkl` e `encoder_baseline.pkl`).

4. **Desenvolvimento do sistema web**:
    - Interface web com Django.
    - Área de gerenciamento de usuários (cadastro, edição, redefinição de senha, exclusão).
    - Módulo de testes para o modelo de regressão.
    - Layout responsivo utilizando Bootstrap.

## 🚀 Tecnologias utilizadas

- Django
- PostgreSQL
- Scikit-learn
- Bootstrap
- HTML5 / CSS3

## 🔧 Como clonar o repositório

```bash
git clone https://github.com/weslleygere/CASE_IA.git
cd CASE_IA
```

## 🐍 Criar ambiente virtual

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## 📦 Instalar as dependências

```bash
pip install -r requirements.txt
```

## 🗄 Configurar as variáveis de ambiente

Você precisará criar um arquivo **.env** na raiz do projeto (ou definir as variáveis diretamente no ambiente).

**Exemplo de variáveis**:

```dotenv
SECRET_KEY=sua_chave_secreta_django

# Banco de dados PostgreSQL
DB_NAME=caseia_db
DB_USER=caseia_user
DB_PASSWORD=senha_segura
DB_HOST=localhost
DB_PORT=5432

# E-mail (para reset de senha)
EMAIL_HOST=smtp.seuprovedor.com
EMAIL_PORT=587
EMAIL_HOST_USER=seuemail@dominio.com
EMAIL_HOST_PASSWORD=sua_senha_email
DEFAULT_FROM_EMAIL=seuemail@dominio.com
```

## 🗄 Configurar o banco de dados (PostgreSQL)

Certifique-se que o banco já está criado:

```sql
CREATE DATABASE caseia_db;
CREATE USER caseia_user WITH PASSWORD 'senha_segura';
GRANT ALL PRIVILEGES ON DATABASE caseia_db TO caseia_user;
```

## 🏃 Rodar as migrações e iniciar a aplicação Django

```bash
python manage.py migrate
python manage.py runserver
```

Acesse no navegador:

```plaintext
http://127.0.0.1:8000/
```

## ✅ Funcionalidades principais

- Login e cadastro de usuários.
- Recuperação e alteração de senha.
- Listagem e edição de usuários.
- Exclusão com confirmação via modal.
- Predição de carga de aquecimento e resfriamento com entrada de variáveis customizadas.
- Validação de token para redefinição de senha.
- Interface padronizada e responsiva.
