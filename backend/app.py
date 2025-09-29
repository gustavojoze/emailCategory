import os
import json
import tempfile
import PyPDF2
from flask import Flask, request, jsonify
from flask_cors import CORS
from model_utils import gerar_json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})

app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024
EXTENSOES_PERMITIDAS = {"txt", "pdf"}
HISTORICO_ARQUIVO = "historicoEmails.json"


def carregar_historico():
    if os.path.exists(HISTORICO_ARQUIVO):
        with open(HISTORICO_ARQUIVO, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict):
                    return [data]
            except json.JSONDecodeError:
                return []
    return []


def salvar_historico(historico):
    with open(HISTORICO_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=2)


def extensao_permitida(nome_arquivo: str) -> bool:
    return "." in nome_arquivo and nome_arquivo.rsplit(".", 1)[1].lower() in EXTENSOES_PERMITIDAS


def extrair_texto_de_arquivo(arquivo, extensao: str) -> str:
    fd, caminho_temp = tempfile.mkstemp(suffix="." + extensao)
    os.close(fd)

    try:
        arquivo.save(caminho_temp)
        if extensao == "txt":
            with open(caminho_temp, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        elif extensao == "pdf":
            with open(caminho_temp, "rb") as f:
                leitor = PyPDF2.PdfReader(f)
                return "\n".join([p.extract_text() or "" for p in leitor.pages])
    finally:
        os.remove(caminho_temp)


@app.route("/analisar", methods=["POST"])
def analisar():
    texto = request.form.get("email_texto", "").strip()
    arquivo = request.files.get("email_arquivo")

    if not texto and arquivo and extensao_permitida(arquivo.filename):
        extensao = arquivo.filename.rsplit(".", 1)[1].lower()
        texto = extrair_texto_de_arquivo(arquivo, extensao)

    if not texto.strip():
        return jsonify({"erro": "Nenhum texto enviado"}), 400

    resposta = gerar_json(texto)
    historico = carregar_historico()
    historico.append(resposta)
    salvar_historico(historico)

    return jsonify(resposta)


@app.route("/historico", methods=["GET"])
def historico():
    return jsonify(carregar_historico())


@app.route("/limpar_historico", methods=["POST"])
def limpar_historico():
    salvar_historico([])
    return jsonify({"status": "Histórico limpo com sucesso"})


if __name__ == "__main__":
    porta = int(os.getenv("PORTA", 5000))
    app.run(host="0.0.0.0", port=porta, debug=True)
