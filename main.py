
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import matplotlib.pyplot as plt
import bcrypt
import os
import uuid

app = Flask(__name__)
CORS(app, origins=[
    "https://preview--escala-4me-dashboard.lovable.app",
    "https://preview--ad-insights-analyzer.lovable.app"
])

@app.route("/", methods=["POST"])
def analisar_csv():
    if "arquivo" not in request.files:
        return jsonify({"erro": "Arquivo não encontrado"}), 400

    arquivo = request.files["arquivo"]

    try:
        df = pd.read_csv(arquivo)
        mensagem = f"Arquivo com {len(df)} linhas carregado com sucesso."
        resumo = "Resumo da campanha gerado com sucesso."
        graficos = []

        for i, coluna in enumerate(df.select_dtypes(include=["number"]).columns[:3]):
            plt.figure()
            df[coluna].plot(kind="hist", title=coluna)
            nome_grafico = f"grafico_{uuid.uuid4().hex}.png"
            caminho_grafico = os.path.join("/tmp", nome_grafico)
            plt.savefig(caminho_grafico)
            graficos.append(f"https://escala4me-backend.onrender.com/grafico/{nome_grafico}")
            plt.close()

        return jsonify({
            "mensagem": mensagem,
            "resumo": resumo,
            "graficos": graficos
        })

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route("/grafico/<nome>")
def servir_grafico(nome):
    caminho = os.path.join("/tmp", nome)
    if os.path.exists(caminho):
        return send_file(caminho, mimetype="image/png")
    return "Gráfico não encontrado", 404

@app.route("/baixar_historico")
def baixar():
    return "Histórico indisponível temporariamente."

if __name__ == "__main__":
    app.run()
