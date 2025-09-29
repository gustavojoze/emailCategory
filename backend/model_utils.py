import os
import re
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def limpar_texto(texto: str) -> str:
    texto = re.sub(r"\S+@\S+", " ", texto)
    texto = re.sub(r"http\S+", " ", texto)
    return re.sub(r"\s+", " ", texto).strip()

def gerar_json(original_email: str) -> dict:
    texto_limpo = limpar_texto(original_email)
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
    Email recebido:
    {texto_limpo}

    Você é um classificador e respondente automático de emails corporativos. 
    Sua tarefa é analisar o email recebido e produzir exatamente um objeto JSON válido. 
    Siga as regras estritamente:

    1. Classificação:
    - "Produtivo": Emails que exigem ação ou resposta específica (ex.: suporte técnico, atualização de casos em aberto, dúvidas sobre o sistema, questões financeiras, transações, faturas, informações de conta, pedidos de compras, aprovações). Seriam coisas relacionadas ao trabalho aos negocios, se for conversa fiada, informal, normalmente é improdutivo.
    - "Improdutivo": Emails que não requerem ação imediata (ex.: agradecimentos, felicitações como “Feliz Natal” ou mensagens sem relação com o negócio ou trabalho no geral, frases mal acabadas, promoções, spam, coisas como propaganda, vendas, qualquer coisa que não estaja relacionado ao trabalho).

    2. Resposta:
    - Se "Produtivo": responda de forma curta, cordial e objetiva, confirmando recebimento e informando que será analisado/encaminhado.
    - Se "Improdutivo": responda de forma educada e breve, agradecendo a mensagem.

    3. Retorno:
    - A saída deve ser SOMENTE JSON válido, sem explicações extras.  
    - O JSON deve ter exatamente as chaves: "email", "categoria", "resposta".

    ⚠️ IMPORTANTE:
    - Não use ```json ou ``` em volta.
    - Não adicione texto fora do JSON.

    Exemplo de saída:
    {{
    "email": "Gostaria de saber o status da minha requisição de suporte técnico.",
    "categoria": "Produtivo",
    "resposta": "Olá, obrigado pelo contato. Recebemos sua solicitação e retornaremos em breve."
    }}
    """

    response = model.generate_content(prompt)

    raw_text = ""
    if response.candidates and response.candidates[0].content.parts:
        raw_text = response.candidates[0].content.parts[0].text.strip()
        if raw_text.startswith("```"):
            raw_text = raw_text.strip("`")
            raw_text = raw_text.replace("json", "", 1).strip()
        match = re.search(r"\{[\s\S]*\}", raw_text)
        if match:
            raw_text = match.group(0)

    try:
        parsed = json.loads(raw_text)
        if all(k in parsed for k in ("email", "categoria", "resposta")):
            return parsed
        else:
            raise ValueError("JSON inválido")
    except Exception as e:
        print("Erro ao decodificar JSON:", e)
        return {
            "email": original_email,
            "categoria": "Erro",
            "resposta": "Falha ao analisar email. Verifique o log."
        }