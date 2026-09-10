# 🏍️ Sistema de Vendas e Gestão - Oficina Mecânica

> ⚠️ **Aviso:** O sistema ainda está em desenvolvimento.

> **Objetivo do Projeto:** Automatizar e organizar a gestão de vendas, estoque de peças e serviços da oficina do meu pai, substituindo controles manuais por um sistema simples, ágil e eficiente.

---

## 📷 Demonstração do Sistema

| Telas Principais | Visualização |
| :--- | :--- |
| **Login / Autenticação** | <img width="1917" height="910" alt="Tela_Login" src="https://github.com/user-attachments/assets/91a78810-37e5-48ac-9787-b7e4d08a399f" /> |
| **Listagem de Vendas** | <img width="1917" height="909" alt="Tela_Vendas" src="https://github.com/user-attachments/assets/aea5896c-c7b2-4b1e-9fe6-07e63b82e6e0" /> |

---

## 🛠️ Tecnologias Utilizadas

**Backend & Banco de Dados:**
* **Python 3**
* **FastAPI**
* **PostgreSQL**
* **`psycopg2`**
* **`python-dotenv`**

**Frontend:**
* **HTML5, CSS3, Bootstrap** (Estrutura e estilização)
* **JavaScript**

---

## 🏗️ Arquitetura do Banco de Dados

A tabela principal de vendas (`vendas`) no PostgreSQL foi modelada com a seguinte estrutura:

* `id_venda`: Chave Primária (SERIAL)
* `cliente`: Nome do cliente (VARCHAR)
* `moto_modelo`: Modelo da motocicleta (VARCHAR)
* `moto_placa`: Placa do veículo (VARCHAR)
* `servico_produto`: Peça trocada ou serviço realizado (TEXT)
* `valor`: Valor da transação (NUMERIC)
* `data_venda`: Data/hora do registro (TIMESTAMP)

---

## 👨‍💻 Desenvolvedor
Desenvolvido por Pedro Magalhães.

Projeto focado em consolidação de conhecimentos em Engenharia de Dados e API em Python.
