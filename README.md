# 📧 EmailCategory

Aplicação web para **classificação automática de emails** em **Produtivos** ou **Improdutivos**, com resposta automática gerada pela API do **Google Gemini**.

---

## 🗂 Estrutura do Projeto

```
.
├── backend/
│   ├── app.py               # Servidor Flask (API)
│   ├── model_utils.py       # Lógica de classificação usando Gemini
│   ├── requirements.txt     # Dependências do backend
│   └── historicoEmails.json # Histórico de classificações (ignorado no git)
│
├── frontend/
│   ├── index.html           # Interface web
│   ├── script.js            # Lógica de interação com o backend
│   ├── style.css            # Estilos da aplicação
│   └── assets/              # Ícones e imagens
│
├── .env                     # Variáveis de ambiente (NÃO subir no git)
├── .gitignore
└── README.md
```

---

## ⚙️ Funcionalidades

- Upload de arquivos **TXT** ou **PDF** contendo emails.  
- Classificação do email em:
  - **Produtivo** → quando requer ação (suporte, compras, faturas, etc.).  
  - **Improdutivo** → mensagens de cortesia, sem ação imediata.  
- Geração de resposta automática cordial.  
- Histórico de classificações.  
- Interface web simples com modais para **resultado** e **histórico**.

---

## 🚀 Como Rodar Localmente

### 1. Clonar o repositório
```bash
git clone https://github.com/SEU_USUARIO/EmailCategory.git
cd EmailCategory
```

### 2. Backend
1. Criar ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

2. Instalar dependências:
   ```bash
   pip install -r backend/requirements.txt
   ```

3. Criar arquivo `.env` na raiz do projeto:
   ```
   GEMINI_API_KEY=sua_chave_aqui
   ```

4. Rodar o servidor:
   ```bash
   cd backend
   python app.py
   ```

Servidor rodará em: [http://127.0.0.1:5000](http://127.0.0.1:5000)

### 3. Frontend
Basta abrir o arquivo `frontend/index.html` no navegador.  
(Ou usar a extensão **Live Server** do VSCode para abrir em `http://127.0.0.1:5500`)

---

## 🛠 Tecnologias Usadas

- **Backend**: Python, Flask, Flask-CORS, PyPDF2  
- **Frontend**: HTML, CSS, JavaScript puro  
- **IA**: Google Gemini API  
- **Persistência**: JSON simples para histórico  

---

